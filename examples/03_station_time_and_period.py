from datetime import datetime
from pyvantagepro import VantagePro2


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        before = device.gettime()
        print("Station time before:", before.isoformat())

        device.settime(datetime.now())
        after = device.gettime()
        print("Station time after:", after.isoformat())

        current_period = device.getperiod()
        print("Archive period before:", current_period)

        device.setperiod(10)
        print("Archive period after:", device.getperiod())
    finally:
        device.close()


if __name__ == "__main__":
    main()
