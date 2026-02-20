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

## Tips

- For long-running scripts, recreate the `VantagePro2` instance on persistent link failures.
- Use archive range windows (`start_date`/`stop_date`) to keep downloads bounded.
- Use normalized payload APIs (`*_as_json`, `*_as_list`) for downstream systems expecting SI units and ISO8601 timestamps.
