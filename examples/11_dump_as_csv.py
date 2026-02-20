import argparse
import time

from pyvantagepro import VantagePro2


def _as_csv_cell(value):
    if value is None:
        return ""
    return str(value)


def main():
    parser = argparse.ArgumentParser(
        description="Stream live data as semicolon-separated CSV rows."
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
        headers = [item["param"] for item in device.meta()]
        print(";".join(headers), flush=True)

        # Compatibility fallback if get_current_data_as_csv is not present.
        reader = getattr(device, "get_current_data_as_csv", device.get_current_data_as_list)

        while True:
            row = reader()
            print(";".join(_as_csv_cell(value) for value in row), flush=True)
            time.sleep(args.interval)
    finally:
        device.close()


if __name__ == "__main__":
    main()
