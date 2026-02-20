from datetime import datetime
from pyvantagepro import VantagePro2


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        start = datetime(2026, 2, 19, 0, 0)
        stop = datetime(2026, 2, 19, 23, 59)
        rows = device.get_archives_as_list(start_date=start, stop_date=stop)
        print("List archive rows:", len(rows))
        if rows:
            print("First row, first 8 values:", rows[0][:8])
    finally:
        device.close()


if __name__ == "__main__":
    main()
