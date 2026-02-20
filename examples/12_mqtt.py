import argparse
import json
import time

from pyvantagepro import VantagePro2


def main():
    parser = argparse.ArgumentParser(
        description="Publish normalized live JSON payloads to an MQTT broker."
    )
    parser.add_argument("--source", default="tcp:127.0.0.1:22222")
    parser.add_argument("--host", required=True, help="MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--topic", default="pyvantagepro/live", help="MQTT topic")
    parser.add_argument("--username", default=None, help="MQTT username")
    parser.add_argument("--password", default=None, help="MQTT password")
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Seconds between samples (default: 2.0)",
    )
    args = parser.parse_args()

    try:
        import paho.mqtt.client as mqtt
    except ImportError:
        raise SystemExit(
            "Missing dependency: paho-mqtt. Install with: python3 -m pip install paho-mqtt"
        )

    mqtt_client = mqtt.Client()
    if args.username:
        mqtt_client.username_pw_set(args.username, args.password)
    mqtt_client.connect(args.host, args.port, keepalive=30)
    mqtt_client.loop_start()

    device = VantagePro2.from_url(args.source, timeout=10)
    try:
        while True:
            payload = device.get_current_data_as_json()
            message = json.dumps(payload, separators=(",", ":"))
            mqtt_client.publish(args.topic, message, qos=0, retain=False)
            time.sleep(args.interval)
    finally:
        device.close()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
