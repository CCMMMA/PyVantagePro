# Examples

This folder contains runnable Python examples for the `VantagePro2` API.

## Prerequisites

1. Install the package in your environment.
2. Ensure your weather station (or serial/TCP bridge) is reachable.
3. Update connection parameters in each script (`tcp:127.0.0.1:22222` or serial path/baud).

Run any example from the repository root:

```bash
python3 examples/01_connect_from_url.py
```

## Example Index

### `01_connect_from_url.py`

- Purpose: create a `VantagePro2` instance using `from_url()`.
- API used: `from_url`, `close`.

### `02_connect_from_serial.py`

- Purpose: connect directly to a serial station/adapter.
- API used: `from_serial`, `close`.
- Note: edit `/dev/ttyUSB0` and `19200` for your hardware.

### `03_station_time_and_period.py`

- Purpose: read/set station clock and archive period.
- API used: `gettime`, `settime`, `getperiod`, `setperiod`, `close`.

### `04_station_info_and_diagnostics.py`

- Purpose: inspect station metadata and status.
- API used: `firmware_date`, `firmware_version`, `timezone`, `getdiagnostics`, `getbar`, `close`.

### `05_current_data_raw.py`

- Purpose: read one raw LOOP packet as parsed station values.
- API used: `get_current_data`, `close`.

### `06_current_data_meta_json_list.py`

- Purpose: inspect normalized live payloads.
- API used: `meta`, `get_current_data_as_json`, `get_current_data_as_list`, `close`.
- Notes:
  - `meta()` returns descriptors with internal and SI units.
  - `get_current_data_as_json()` returns normalized dict output.
  - `get_current_data_as_list()` returns normalized row in `meta()` order.

### `07_archives_raw.py`

- Purpose: fetch archive rows in native parser representation.
- API used: `get_archives`, `close`.

### `08_archives_json.py`

- Purpose: fetch archive rows as normalized JSON dictionaries.
- API used: `get_archives_as_json`, `close`.
- Signature:
  - `get_archives_as_json(start_date=None, stop_date=None)`

### `09_archives_list.py`

- Purpose: fetch archive rows as normalized ordered lists.
- API used: `get_archives_as_list`, `close`.
- Signature:
  - `get_archives_as_list(start_date=None, stop_date=None)`

### `10_resilient_read.py`

- Purpose: handle recoverable transport/protocol failures.
- API used: `get_current_data_as_json`, `NoDeviceException`, `BadAckException`, `close`.

### `11_dump_as_csv.py`

- Purpose: stream live rows to stdout as semicolon-separated values.
- API used: `meta`, `get_current_data_as_csv` (with fallback to `get_current_data_as_list`), `close`.
- Behavior:
  - Prints the CSV header row once at startup.
  - Prints one data row per sample.
  - Uses `;` as separator.
- Arguments:
  - `--source` (default: `tcp:127.0.0.1:22222`)
  - `--interval` (default: `2.0`)
- Example:

```bash
python3 examples/11_dump_as_csv.py --source tcp:127.0.0.1:22222 --interval 1
```

### `12_dump_as_json.py`

- Purpose: stream live JSON objects to stdout.
- API used: `get_current_data_as_json`, `close`.
- Behavior:
  - Prints `[` at startup.
  - Prints one JSON object per sample.
  - Prefixes each object after the first with a comma, so rows are array elements.
- Arguments:
  - `--source` (default: `tcp:127.0.0.1:22222`)
  - `--interval` (default: `2.0`)
- Example:

```bash
python3 examples/12_dump_as_json.py --source tcp:127.0.0.1:22222 --interval 1
```

### `12_mqtt.py`

- Purpose: publish each live normalized JSON payload to an MQTT broker.
- API used: `get_current_data_as_json`, `close`.
- Extra dependency:
  - `paho-mqtt` (`python3 -m pip install paho-mqtt`)
- Arguments:
  - `--source` (default: `tcp:127.0.0.1:22222`)
  - `--host` (required)
  - `--port` (default: `1883`)
  - `--topic` (default: `pyvantagepro/live`)
  - `--username` / `--password` (optional)
  - `--interval` (default: `2.0`)
- Example:

```bash
python3 examples/12_mqtt.py \
  --source tcp:127.0.0.1:22222 \
  --host 127.0.0.1 \
  --port 1883 \
  --topic pyvantagepro/live \
  --interval 1
```

### `14_stream.py`

- Purpose: continuous station stream to both CSV files and MQTT GeoJSON packets.
- Behavior:
  - Opens device connection.
  - Reads parameter list from `meta()` and uses those names as CSV header.
- Reads configuration from a flat `config.json` schema (same as real deployment).
  - Rotates CSV files each UTC hour:
    - `root/YYYY/MM/DD/<station_uuid>_YYYYMMDDZHH00.csv`
  - Appends each `get_current_data_as_json()` sample as one CSV row (`;` delimiter).
  - Builds a GeoJSON `Feature` with:
    - `geometry.coordinates = [longitude, latitude]`
    - `properties = get_current_data_as_json() + {"uuid": ..., "name": ...}`
  - Publishes to MQTT topic equal to station UUID (`uuid`).
- Uses a store-and-forward strategy for MQTT:
    - every GeoJSON message is appended to a durable local spool file,
    - a dedicated MQTT worker thread forwards queued messages with `qos=1`,
    - messages are removed from spool only after successful publish.
- If MQTT is unavailable, data collection and CSV writing continue and queued packets are sent when connectivity returns.
- Uses logging output instead of `print`.
- Handles `SIGINT`/`SIGTERM` for graceful shutdown:
  - stops acquisition loop,
  - closes MQTT worker cleanly,
  - flushes/finishes file writes,
  - closes VantagePro2 connection.

CLI options:

- `--config <path>`: config JSON path (default: `config.json`).
- `--dry`: disable CSV and MQTT; logs each CSV row and MQTT packet.
- `--no-csv`: disable CSV writing.
- `--no-mqtt`: disable MQTT publishing.

Automatic behaviors:

- If `pathStorage` is missing, CSV is disabled (equivalent to `--no-csv`).
- If MQTT config is missing or incomplete, dry mode is forced.

Supported config schema (`examples/config.json.sample`):

```json
{
  "uuid": "it.uniparthenope.meteo.ws2",
  "name": "Gaiola",
  "lat": 40.7923,
  "lon": 14.1875,
  "usbPort": 22222,
  "usbPollInterval": 1.0,
  "delay": 10,
  "timeout": 60,
  "pathStorage": "/storage/vantage-pro/",
  "mqttBroker": "193.205.230.7",
  "mqttPort": 1883,
  "mqttUser": "admin",
  "mqttPass": "password",
  "mqttQos": 1,
  "offlineMaxMessages": 200000,
  "offlineMaxAgeSec": 604800,
  "airlinkIntervalSec": 300
}
```

Run:

```bash
cp examples/config.json.sample examples/config.json
python3 examples/14_stream.py --config examples/config.json
```

Dry run:

```bash
python3 examples/14_stream.py --config examples/config.json --dry
```

## Tips

- For long-running scripts, recreate the `VantagePro2` instance on persistent link failures.
- Use archive range windows (`start_date`/`stop_date`) to keep downloads bounded.
- Use normalized payload APIs (`*_as_json`, `*_as_list`) for downstream systems expecting SI units and ISO8601 timestamps.
