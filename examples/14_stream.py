#!/usr/bin/env python3
import csv
import json
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path

from pyvantagepro import VantagePro2


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


def append_csv_row(path, headers, payload):
    with path.open("a", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp, delimiter=";")
        writer.writerow([payload.get(name, "") for name in headers])


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
        # Drop oldest by age first.
        if self.max_age_sec > 0:
            min_ts = now_ts - self.max_age_sec
            while self._items and float(self._items[0].get("ts", now_ts)) < min_ts:
                self._items.popleft()
        # Then cap queue length.
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
            # Expire stale items before handing out.
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
                int(self.mqtt_cfg.get("port", 1883)),
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
    source = cfg.get("source")
    if not source:
        usb_port = cfg.get("usbPort", 22222)
        source = "tcp:127.0.0.1:%s" % usb_port

    root = Path(cfg.get("root", cfg.get("pathStorage", "/tmp/pyvantagepro")))

    station_uuid = cfg.get("station_uuid", cfg.get("sstation_uuid", cfg.get("uuid")))
    if not station_uuid:
        raise SystemExit("config.json must define station_uuid/sstation_uuid/uuid")

    name = cfg["name"]
    latitude = cfg.get("latitude", cfg.get("lat"))
    longitude = cfg.get("longitude", cfg.get("lon"))
    if latitude is None or longitude is None:
        raise SystemExit("config.json must define latitude/longitude (or lat/lon)")

    interval = float(cfg.get("interval_seconds", cfg.get("usbPollInterval", 2.0)))
    timeout = float(cfg.get("timeout", 10))

    mqtt_nested = cfg.get("mqtt")
    if mqtt_nested:
        mqtt_cfg = {
            "host": mqtt_nested["host"],
            "port": int(mqtt_nested.get("port", 1883)),
            "topic": mqtt_nested["topic"],
            "username": mqtt_nested.get("username"),
            "password": mqtt_nested.get("password"),
            "qos": int(mqtt_nested.get("qos", 1)),
            "keepalive": int(mqtt_nested.get("keepalive", 30)),
            "reconnect_sleep": float(mqtt_nested.get("reconnect_sleep", 1.0)),
        }
    else:
        mqtt_cfg = {
            "host": cfg["mqttBroker"],
            "port": int(cfg.get("mqttPort", 1883)),
            "topic": cfg.get("mqttTopic", "pyvantagepro/live"),
            "username": cfg.get("mqttUser"),
            "password": cfg.get("mqttPass"),
            "qos": int(cfg.get("mqttQos", 1)),
            "keepalive": int(cfg.get("mqttKeepalive", 30)),
            "reconnect_sleep": float(cfg.get("delay", 1.0)),
        }

    spool_path = Path(
        cfg.get("mqtt_spool_file", str(root / "mqtt_spool.jsonl"))
    )

    offline_max_messages = int(cfg.get("offlineMaxMessages", 200000))
    offline_max_age_sec = int(cfg.get("offlineMaxAgeSec", 604800))

    return {
        "source": source,
        "root": root,
        "station_uuid": station_uuid,
        "name": name,
        "latitude": float(latitude),
        "longitude": float(longitude),
        "interval": interval,
        "timeout": timeout,
        "mqtt": mqtt_cfg,
        "spool_path": spool_path,
        "offline_max_messages": offline_max_messages,
        "offline_max_age_sec": offline_max_age_sec,
    }


def main():
    config_path = Path(__file__).with_name("config.json")
    cfg = normalize_config(load_config(config_path))

    stop_event = threading.Event()
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
            target_csv = csv_path(cfg["root"], cfg["station_uuid"], now_utc)
            if target_csv != current_csv:
                ensure_csv_header(target_csv, headers)
                current_csv = target_csv

            payload = device.get_current_data_as_json()
            append_csv_row(current_csv, headers, payload)

            point = build_geojson_point(
                payload,
                cfg["name"],
                cfg["latitude"],
                cfg["longitude"],
            )
            spool.put(json.dumps(point, separators=(",", ":")))
            time.sleep(cfg["interval"])
    finally:
        stop_event.set()
        forwarder.join(timeout=3.0)
        device.close()


if __name__ == "__main__":
    main()
