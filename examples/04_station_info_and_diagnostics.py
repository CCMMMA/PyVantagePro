from pyvantagepro import VantagePro2


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        print("Firmware date:", device.firmware_date)
        print("Firmware version:", device.firmware_version)
        print("Timezone:", device.timezone)
        print("Diagnostics:", device.getdiagnostics())
        print("Barometer calibration:", device.getbar())
    finally:
        device.close()


if __name__ == "__main__":
    main()
