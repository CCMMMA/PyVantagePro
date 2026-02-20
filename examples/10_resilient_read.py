from pyvantagepro import VantagePro2
from pyvantagepro.device import NoDeviceException, BadAckException


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        try:
            payload = device.get_current_data_as_json()
            print("Read OK, keys:", len(payload))
        except (NoDeviceException, BadAckException) as exc:
            print("Read failed:", exc)
    finally:
        device.close()


if __name__ == "__main__":
    main()
