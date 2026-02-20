import argparse
import json
import time

from pyvantagepro import VantagePro2


def main():
    parser = argparse.ArgumentParser(
        description="Stream live data as JSON objects intended as array elements."
    )
    parser.add_argument(
        "--source",
        default="tcp:127.0.0.1:22222",
        help="PyLink source URL (default: tcp:127.0.0.1:22222)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Seconds between samples (default: 2.0)",
    )
    args = parser.parse_args()

    device = VantagePro2.from_url(args.source, timeout=10)
    try:
        # Open an array-like stream.
        print("[", flush=True)
        first = True
        while True:
            payload = device.get_current_data_as_json()
            line = json.dumps(payload, separators=(",", ":"))
            if first:
                print(line, flush=True)
                first = False
            else:
                print("," + line, flush=True)
            time.sleep(args.interval)
    finally:
        device.close()


if __name__ == "__main__":
    main()
