from pyvantagepro import VantagePro2


def main():
    # Adjust serial path/baud for your environment.
    device = VantagePro2.from_serial("/dev/ttyUSB0", 19200, timeout=10)
    try:
        print("Connected over serial transport")
    finally:
        device.close()


if __name__ == "__main__":
    main()
