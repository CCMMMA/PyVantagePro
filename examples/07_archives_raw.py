from datetime import datetime
from pyvantagepro import VantagePro2


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        start = datetime(2026, 2, 19, 0, 0)
        stop = datetime(2026, 2, 19, 23, 59)
        archives = device.get_archives(start_date=start, stop_date=stop)
        print("Raw archive rows:", len(archives))
        if archives:
            print("First row keys:", list(archives[0].keys())[:8])
    finally:
        device.close()


if __name__ == "__main__":
    main()
