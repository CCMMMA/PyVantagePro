#!/usr/bin/env python3
import argparse
import csv
import json
import logging
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path

from pyvantagepro import VantagePro2

LOGGER = logging.getLogger("pyvantagepro.examples.14_stream")


def load_config(path):
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def utc_hour_stamp(now_utc):
    return now_utc.strftime("%Y%m%dZ%H00")


def utc_partition(now_utc):
    return now_utc.strftime("%Y"), now_utc.strftime("%m"), now_utc.strftime("%d")


def csv_path(root, station_uuid, now_utc):
    year, month, day = utc_partition(now_utc)
    dirname = root / year / month / day
    filename = "%s_%s.csv" % (station_uuid, utc_hour_stamp(now_utc))
    return dirname / filename


def ensure_csv_header(path, headers):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp, delimiter=";")
        writer.writerow(headers)


def csv_row_values(headers, payload):
    return [payload.get(name, "") for name in headers]


def append_csv_row(path, headers, payload):
    with path.open("a", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp, delimiter=";")
        writer.writerow(csv_row_values(headers, payload))


def build_geojson_point(payload, name, latitude, longitude):
    properties = dict(payload)
    properties["name"] = name
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(longitude), float(latitude)],
        },
        "properties": properties,
    }


class DiskSpool(object):
    def __init__(self, path, max_messages, max_age_sec):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.max_messages = int(max_messages)
        self.max_age_sec = int(max_age_sec)
        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)
        self._items = deque()
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    if isinstance(row, dict) and "payload" in row and "ts" in row:
                        self._items.append(row)
                    else:
                        self._items.append({"ts": time.time(), "payload": line})
                except Exception:
                    self._items.append({"ts": time.time(), "payload": line})
        self._enforce_limits(time.time())
        self._rewrite_file()

    def _rewrite_file(self):
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as fp:
            for item in self._items:
                fp.write(json.dumps(item, separators=(",", ":")))
                fp.write("\n")
        tmp.replace(self.path)

    def _enforce_limits(self, now_ts):
        if self.max_age_sec > 0:
            min_ts = now_ts - self.max_age_sec
            while self._items and float(self._items[0].get("ts", now_ts)) < min_ts:
                self._items.popleft()
        if self.max_messages > 0:
            while len(self._items) > self.max_messages:
                self._items.popleft()

    def put(self, payload_json):
        now_ts = time.time()
        entry = {"ts": now_ts, "payload": payload_json}
        with self._cv:
            self._items.append(entry)
            self._enforce_limits(now_ts)
            self._rewrite_file()
            self._cv.notify()

    def peek_wait(self, timeout=1.0):
        with self._cv:
            if not self._items:
                self._cv.wait(timeout=timeout)
            if not self._items:
                return None
            self._enforce_limits(time.time())
            if not self._items:
                self._rewrite_file()
                return None
            return self._items[0]["payload"]

    def ack_first(self):
        with self._cv:
            if not self._items:
                return
            self._items.popleft()
            self._rewrite_file()


class MqttForwarder(threading.Thread):
    def __init__(self, mqtt_cfg, spool, stop_event):
        super(MqttForwarder, self).__init__(daemon=True)
        self.mqtt_cfg = mqtt_cfg
        self.spool = spool
        self.stop_event = stop_event
        self._connected = False
        self.client = None

    def _on_connect(self, client, userdata, flags, rc):
        self._connected = (rc == 0)

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False

    def _ensure_connected(self):
        if self._connected:
            return True
        try:
            self.client.connect(
                self.mqtt_cfg["host"],
                int(self.mqtt_cfg["port"]),
                keepalive=int(self.mqtt_cfg.get("keepalive", 30)),
            )
            for _ in range(20):
                if self._connected:
                    return True
                if self.stop_event.is_set():
                    return False
                time.sleep(0.1)
        except Exception:
            pass
        return self._connected

    def run(self):
        try:
            import paho.mqtt.client as mqtt
        except ImportError:
            raise SystemExit(
                "Missing dependency: paho-mqtt. Install with: python3 -m pip install paho-mqtt"
            )

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        if self.mqtt_cfg.get("username"):
            self.client.username_pw_set(
                self.mqtt_cfg["username"], self.mqtt_cfg.get("password")
            )
        self.client.loop_start()

        qos = int(self.mqtt_cfg.get("qos", 1))
        topic = self.mqtt_cfg["topic"]
        reconnect_sleep = float(self.mqtt_cfg.get("reconnect_sleep", 1.0))

        try:
            while not self.stop_event.is_set():
                payload_json = self.spool.peek_wait(timeout=1.0)
                if payload_json is None:
                    continue

                if not self._ensure_connected():
                    time.sleep(reconnect_sleep)
                    continue

                try:
                    info = self.client.publish(topic, payload_json, qos=qos, retain=False)
                    info.wait_for_publish(timeout=10.0)
                    if info.rc == mqtt.MQTT_ERR_SUCCESS and info.is_published():
                        self.spool.ack_first()
                    else:
                        self._connected = False
                        time.sleep(reconnect_sleep)
                except Exception:
                    self._connected = False
                    time.sleep(reconnect_sleep)
        finally:
            self.client.loop_stop()
            try:
                self.client.disconnect()
            except Exception:
                pass


def normalize_config(cfg):
    required = ("uuid", "name", "lat", "lon")
    for key in required:
        if key not in cfg:
            raise SystemExit("config.json must define %s" % key)

    source = "tcp:127.0.0.1:%s" % int(cfg.get("usbPort", 22222))
    root = Path(cfg["pathStorage"]) if cfg.get("pathStorage") else None

    mqtt_cfg = {
        "host": cfg.get("mqttBroker"),
        "port": cfg.get("mqttPort"),
        "username": cfg.get("mqttUser"),
        "password": cfg.get("mqttPass"),
        "qos": int(cfg.get("mqttQos", 1)),
        "topic": cfg.get("mqttTopic", "pyvantagepro/%s/live" % cfg["uuid"]),
        "keepalive": int(cfg.get("mqttKeepalive", 30)),
        "reconnect_sleep": float(cfg.get("delay", 1.0)),
    }

    return {
        "source": source,
        "root": root,
        "station_uuid": cfg["uuid"],
        "name": cfg["name"],
        "latitude": float(cfg["lat"]),
        "longitude": float(cfg["lon"]),
        "interval": float(cfg.get("usbPollInterval", 2.0)),
        "timeout": float(cfg.get("timeout", 10)),
        "mqtt": mqtt_cfg,
        "spool_path": Path(cfg.get("mqttSpoolFile", str((root or Path(".") ) / "mqtt_spool.jsonl"))),
        "offline_max_messages": int(cfg.get("offlineMaxMessages", 200000)),
        "offline_max_age_sec": int(cfg.get("offlineMaxAgeSec", 604800)),
    }


def is_mqtt_config_complete(mqtt_cfg):
    return bool(mqtt_cfg.get("host")) and bool(mqtt_cfg.get("port"))


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Stream station data to CSV and MQTT GeoJSON")
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to config JSON file (default: config.json)",
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Do not write CSV and do not connect MQTT; log CSV row and MQTT packet",
    )
    parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Disable CSV file writing",
    )
    parser.add_argument(
        "--no-mqtt",
        action="store_true",
        help="Disable MQTT publishing",
    )
    return parser


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    args = build_arg_parser().parse_args()
    cfg = normalize_config(load_config(Path(args.config)))

    no_csv = args.no_csv
    no_mqtt = args.no_mqtt
    dry = args.dry

    if cfg["root"] is None:
        no_csv = True
        LOGGER.warning("No pathStorage in config: CSV disabled (--no-csv behavior)")

    if not is_mqtt_config_complete(cfg["mqtt"]):
        dry = True
        LOGGER.warning("MQTT config missing/incomplete: forcing --dry behavior")

    if dry:
        no_csv = True
        no_mqtt = True
        LOGGER.info("Dry mode enabled: CSV and MQTT disabled")

    stop_event = threading.Event()
    forwarder = None
    spool = None

    if not no_mqtt:
        spool = DiskSpool(
            cfg["spool_path"],
            max_messages=cfg["offline_max_messages"],
            max_age_sec=cfg["offline_max_age_sec"],
        )
        forwarder = MqttForwarder(cfg["mqtt"], spool, stop_event)
        forwarder.start()

    device = VantagePro2.from_url(cfg["source"], timeout=cfg["timeout"])
    try:
        headers = [item["param"] for item in device.meta()]
        current_csv = None

        while True:
            now_utc = datetime.utcnow()
            payload = device.get_current_data_as_json()
            row = csv_row_values(headers, payload)

            if dry:
                LOGGER.info("CSV_ROW;%s", ";".join(str(v) if v is not None else "" for v in row))

            if not no_csv:
                target_csv = csv_path(cfg["root"], cfg["station_uuid"], now_utc)
                if target_csv != current_csv:
                    ensure_csv_header(target_csv, headers)
                    current_csv = target_csv
                append_csv_row(current_csv, headers, payload)

            point = build_geojson_point(
                payload,
                cfg["name"],
                cfg["latitude"],
                cfg["longitude"],
            )
            packet = json.dumps(point, separators=(",", ":"))

            if dry:
                LOGGER.info("MQTT_PACKET;%s", packet)
            elif not no_mqtt:
                spool.put(packet)

            time.sleep(cfg["interval"])
    finally:
        stop_event.set()
        if forwarder is not None:
            forwarder.join(timeout=3.0)
        device.close()


if __name__ == "__main__":
    main()
