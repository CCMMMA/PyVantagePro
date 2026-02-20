from pyvantagepro import VantagePro2


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        print("Connected over URL transport")
    finally:
        device.close()


if __name__ == "__main__":
    main()
