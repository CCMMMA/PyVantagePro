# PyVantagePro

Python tools to communicate with Davis Vantage Pro2 weather stations.

This project provides:
- A Python API (`VantagePro2`) for live data, archives, and station metadata
- A CLI (`pyvantagepro`) for common operational workflows
- Parsers for LOOP and archive records

## Highlights

- Read current station time (`gettime`) and set it (`settime`)
- Read live LOOP data (`get_current_data`)
- Download archive records (`get_archives`)
- Read station diagnostics, firmware info, and barometer calibration data
- Export data to CSV from API and CLI
- Connection recovery on `BrokenPipeError` (automatic reconnect/retry)

## Installation

### From source (recommended)

```bash
git clone https://github.com/CCMMMA/PyVantagePro.git
cd PyVantagePro
python3 -m pip install -U .
```

### In editable mode for development

```bash
python3 -m pip install -U -e .
```

### Upgrade an existing environment

```bash
python -m pip uninstall -y pyvantagepro PyVantagePro
python -m pip install --no-cache-dir -U git+https://github.com/CCMMMA/PyVantagePro.git@master
```

## Quick Start (Python API)

```python
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222', timeout=10)

station_time = device.gettime()
print(station_time)

current = device.get_current_data()
print(current['TempIn'])
print(current['RainRate'])

# Keep only selected fields and serialize as CSV
print(current.filter(('Datetime', 'TempIn', 'TempOut', 'RainRate')).to_csv())

archives = device.get_archives()
print(len(archives))

# Always close when done
device.close()
```

## More API Examples

### 1. List available live-data variables

```python
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222')
fields = device.meta()  # names returned by get_current_data()
print(fields)
device.close()
```

### 2. Read only selected live fields

```python
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222')
data = device.get_current_data()

subset = data.filter(('Datetime', 'TempIn', 'TempOut', 'HumOut', 'RainRate', 'WindSpeed'))
print(subset)
print(subset.to_csv())
device.close()
```

### 3. Get live data as a JSON object

```python
import json
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222')
payload = device.get_current_data_as_json()

print(type(payload))          # dict
print(payload['TempIn'])      # float
print(payload['Datetime'])    # JSON-ready datetime string

# Optional: serialize to JSON string
print(json.dumps(payload))
device.close()
```

### 4. Download archives for a specific time window

```python
from datetime import datetime
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222')

start = datetime(2026, 2, 19, 0, 0)
stop = datetime(2026, 2, 19, 23, 59)
archives = device.get_archives(start_date=start, stop_date=stop)

print(f"records: {len(archives)}")
print(archives[0])
print(archives[-1])
device.close()
```

### 5. Keep a local CSV archive up to date

```python
from pathlib import Path
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222')
db_path = Path("weather_archive.csv")

new_rows = device.get_archives()
if new_rows:
    csv_text = new_rows.to_csv(header=not db_path.exists())
    mode = "a" if db_path.exists() else "w"
    with db_path.open(mode) as f:
        f.write(csv_text if mode == "w" else csv_text.split("\n", 1)[1])

device.close()
```

### 6. Read station metadata and diagnostics

```python
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222')

print("Firmware date:", device.firmware_date)
print("Firmware version:", device.firmware_version)
print("Archive period (min):", device.getperiod())
print("Timezone:", device.timezone)
print("Diagnostics:", device.getdiagnostics())
print("Barometer calibration:", device.getbar())

device.close()
```

### 7. Set station time and archive period

```python
from datetime import datetime
from pyvantagepro import VantagePro2

device = VantagePro2.from_url('tcp:127.0.0.1:22222')

before = device.gettime()
device.settime(datetime.now())
after = device.gettime()
print("time:", before, "->", after)

old_period = device.getperiod()
device.setperiod(10)  # allowed values: 1, 5, 10, 15, 30, 60, 120
print("archive period:", old_period, "->", device.getperiod())

device.close()
```

### 8. Handle recoverable link errors

```python
from pyvantagepro import VantagePro2
from pyvantagepro.device import NoDeviceException, BadAckException

device = VantagePro2.from_url('tcp:127.0.0.1:22222', timeout=10)

try:
    data = device.get_current_data()
except (NoDeviceException, BadAckException) as exc:
    # The library retries internally; this handles final failure.
    print("station read failed:", exc)
finally:
    device.close()
```

## Connection URLs

`PyVantagePro` uses `pylink` URLs, for example:
- `tcp:host:port`
- `serial:/dev/ttyUSB0:19200:8N1`

Use the transport format that matches your hardware setup.

## CLI Usage

```bash
pyvantagepro --help
```

Available commands include:
- `gettime`
- `settime`
- `getinfo`
- `getbar`
- `getdata`
- `getarchives`
- `update`
- `getperiod`
- `setperiod`

### CLI examples

```bash
# Read station time
pyvantagepro gettime tcp:127.0.0.1:22222

# Read one live packet and print CSV to stdout
pyvantagepro getdata tcp:127.0.0.1:22222

# Download archives between two timestamps
pyvantagepro getarchives \
  --start "2026-02-19 00:00" \
  --stop "2026-02-19 23:59" \
  tcp:127.0.0.1:22222

# Update a local CSV database file with new archive rows
pyvantagepro update tcp:127.0.0.1:22222 weather_archive.csv
```

## Troubleshooting

### `BrokenPipeError: [Errno 32] Broken pipe`

If your station/proxy drops idle connections, writes can fail with `BrokenPipeError`.
Recent versions of this repository include automatic reconnect and retry logic.

If you still see this error:
1. Make sure your environment is running the latest code (`pip install -U ...`).
2. Recreate the `VantagePro2` instance after long idle periods.
3. Verify host/port serial bridge health (e.g. TCP proxy, USB serial adapter).
4. Increase timeout if your link is slow.

### Imported package does not match repository code

If stack traces point to `.../site-packages/pyvantagepro/...`, your virtualenv may use an older installed package.
Reinstall from this repository in that exact virtualenv.

## Development

Run tests:

```bash
python3 -m pytest -q
```

Repository guidance for agents/contributors is documented in `AGENTS.md`.

## Notes

- Legacy documentation still exists in `README.rst` and `docs/`.
- `setup.py` currently reads `README.rst` for package metadata.

## License

GNU GPL v3 (see `COPYING`).
