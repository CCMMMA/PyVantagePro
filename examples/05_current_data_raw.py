from pyvantagepro import VantagePro2


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        current = device.get_current_data()
        print("Raw LOOP fields:", len(current))
        print("TempIn (station units):", current.get("TempIn"))
        print("RainRate (station units):", current.get("RainRate"))
    finally:
        device.close()


if __name__ == "__main__":
    main()
