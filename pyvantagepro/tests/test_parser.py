# coding: utf8
# Pedagogical note: the next line explains one concrete step in the program flow.
'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pyvantagepro.tests.test_link
    # Pedagogical note: the next line explains one concrete step in the program flow.
    ----------------------------

    # Pedagogical note: the next line explains one concrete step in the program flow.
    The pyvantagepro test suite.

    # Pedagogical note: the next line explains one concrete step in the program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    :license: GNU GPL v3.

# Pedagogical note: the next line explains one concrete step in the program flow.
'''
# Pedagogical note: the next line explains one concrete step in the program flow.
from __future__ import unicode_literals
# Pedagogical note: the next line explains one concrete step in the program flow.
from datetime import datetime
# Pedagogical note: the next line explains one concrete step in the program flow.
import struct


# Pedagogical note: the next line explains one concrete step in the program flow.
from ..logger import active_logger
# Pedagogical note: the next line explains one concrete step in the program flow.
from ..parser import (LoopDataParserRevB, ArchiveDataParserRevB,
                      # Pedagogical note: the next line explains one concrete step in the program flow.
                      VantageProCRC, pack_datetime, unpack_datetime,
                      # Pedagogical note: the next line explains one concrete step in the program flow.
                      pack_dmp_date_time,
                      # Pedagogical note: the next line explains one concrete step in the program flow.
                      unpack_dmp_date_time)
# Pedagogical note: the next line explains one concrete step in the program flow.
from ..utils import hex_to_bytes


# active logging for tests
# Pedagogical note: the next line explains one concrete step in the program flow.
active_logger()


# Pedagogical note: the next line explains one concrete step in the program flow.
class TestLoopDataParser:
    # Pedagogical note: the next line explains one concrete step in the program flow.
    ''' Test parser.'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    def setup_class(self):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Setup common data.'''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.data = "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF" \
                    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000" \
                    "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000" \
                    "0000000000000000000000000000008C00060C610183070A" \
                    "0D2A3C"
        # Pedagogical note: the next line explains one concrete step in the program flow.
        self.bytes = hex_to_bytes(self.data)

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def test_check_crc(self):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Test crc verification.'''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert VantageProCRC(self.bytes).check()

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def test_check_raw_data(self):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        item = LoopDataParserRevB(self.bytes, datetime.now())
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item.raw.replace(' ', '') == self.data
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item.raw_bytes == self.bytes

    # Pedagogical note: the next line explains one concrete step in the program flow.
    def test_unpack(self):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '''Test unpack loop packet.'''
        # Pedagogical note: the next line explains one concrete step in the program flow.
        item = LoopDataParserRevB(self.bytes, datetime.now())

        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01HighLeafTemp'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01HighLeafWet'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01HighSoilMois'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01HighSoilTemp'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01LowLeafTemp'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01LowLeafWet'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01LowSoilMois'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Alarm01LowSoilTemp'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['AlarmEx01HighHum'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['AlarmInFallBarTrend'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['AlarmOut10minAvgSpeed'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['AlarmRain15min'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['BarTrend'] == 196
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['Barometer'] == 31.572
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['BatteryStatus'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['BatteryVolts'] == 0.8203125
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['ETDay'] == 0.0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['ETMonth'] == 0.0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['ETYear'] == 0.0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['ExtraTemps01'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['ForecastIcon'] == 6
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['ForecastRuleNo'] == 12
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['HumExtra01'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['HumIn'] == 30
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['HumOut'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['LeafTemps01'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['LeafWetness01'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['LeafWetness04'] == 0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['RainDay'] == 0.0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['RainMonth'] == 0.0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['RainRate'] == 655.35
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['RainStorm'] == 0.0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['RainYear'] == 8.28
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['SoilMoist01'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['SolarRad'] == 32767
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['StormStartDate'] == '2127-15-31'
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['SunRise'] == '03:53'
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['SunSet'] == '19:23'
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['TempIn'] == 85.0
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['TempOut'] == 3276.7
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['UV'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['WindDir'] == 32767
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['WindSpeed'] == 255
        # Pedagogical note: the next line explains one concrete step in the program flow.
        assert item['WindSpeed10Min'] == 255


# Pedagogical note: the next line explains one concrete step in the program flow.
def test_datetime_parser():
    # Pedagogical note: the next line explains one concrete step in the program flow.
    '''Test pack and unpack datetime.'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    data = hex_to_bytes("25 35 0A 07 06 70 60 BA")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    assert VantageProCRC(data).check()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    date = unpack_datetime(data)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    assert date == datetime(2012, 6, 7, 10, 53, 37)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    assert data == pack_datetime(date)


# Pedagogical note: the next line explains one concrete step in the program flow.
def test_dump_date_time():
    # Build a deterministic datetime for round-trip verification.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    d = datetime(2012, 10, 26, 10, 10)
    # Encode datetime into Davis DateStamp/TimeStamp plus CRC.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    packed = pack_dmp_date_time(d)
    # Unpack encoded payload into date, time, and CRC words.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    date, time, _ = struct.unpack(b"HHH", packed)
    # Ensure decoded date/time exactly matches the original.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    assert d == unpack_dmp_date_time(date, time)


# Pedagogical note: the next line explains one concrete step in the program flow.
def test_archive_rain_rate_scaling():
    # Encode 2024-03-02 using Davis packed archive date format.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    date = 2 + 3 * 32 + (2024 - 2000) * 512
    # Use 12:34 packed as HHMM.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    time = 1234
    # Build one full binary archive record with known rain-rate values.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    raw = struct.pack(
        # Pedagogical note: the next line explains one concrete step in the program flow.
        b'=HHHHHHHHHHHBBBBBBBBHBB2s2s4sB2s3s4s',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        date, time,         # DateStamp, TimeStamp
        # Pedagogical note: the next line explains one concrete step in the program flow.
        700, 710, 690,      # TempOut, TempOutHi, TempOutLow
        # Pedagogical note: the next line explains one concrete step in the program flow.
        123, 456,           # RainRate, RainRateHi
        # Pedagogical note: the next line explains one concrete step in the program flow.
        30000, 500, 6,      # Barometer, SolarRad, WindSamps
        # Pedagogical note: the next line explains one concrete step in the program flow.
        680,                # TempIn
        # Pedagogical note: the next line explains one concrete step in the program flow.
        50, 51, 3, 8, 4, 5, 9, 20,  # HumIn..ETHour
        # Pedagogical note: the next line explains one concrete step in the program flow.
        700, 25, 1,         # SolarRadHi, UVHi, ForecastRuleNo
        # Pedagogical note: the next line explains one concrete step in the program flow.
        b'\x64\x65', b'\x01\x02', b'\x5A\x5B\x5C\x5D',  # Leaf/Soil temps
        # Pedagogical note: the next line explains one concrete step in the program flow.
        0,                  # RecType
        # Pedagogical note: the next line explains one concrete step in the program flow.
        b'\x32\x33', b'\x60\x61\x62', b'\x10\x11\x12\x13',  # Extra*
    # Pedagogical note: the next line explains one concrete step in the program flow.
    )
    # Parse binary payload using archive parser under test.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    item = ArchiveDataParserRevB(raw)
    # Verify rain rate converts from hundredths to engineering units.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    assert item['RainRate'] == 1.23
    # Verify rain-rate high-watermark uses identical scaling.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    assert item['RainRateHi'] == 4.56
