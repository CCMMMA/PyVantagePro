import json
from pyvantagepro import VantagePro2


def main():
    device = VantagePro2.from_url("tcp:127.0.0.1:22222", timeout=10)
    try:
        meta = device.meta()
        print("Metadata columns:", len(meta))
        print("First descriptor:", meta[0])

        payload = device.get_current_data_as_json()
        print("JSON keys:", sorted(payload.keys())[:8], "...")
        print(json.dumps(payload, indent=2))

        row = device.get_current_data_as_list()
        print("List columns:", len(row))
        print("First 5 values:", row[:5])
    finally:
        device.close()


if __name__ == "__main__":
    main()
