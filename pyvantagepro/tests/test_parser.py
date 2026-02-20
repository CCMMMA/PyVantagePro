# coding: utf8
'''
    pyvantagepro.tests.test_link
    ----------------------------

    The pyvantagepro test suite.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import unicode_literals
from datetime import datetime
import struct


from ..logger import active_logger
from ..parser import (LoopDataParserRevB, ArchiveDataParserRevB,
                      VantageProCRC, pack_datetime, unpack_datetime,
                      pack_dmp_date_time,
                      unpack_dmp_date_time)
from ..utils import hex_to_bytes


# active logging for tests
active_logger()


class TestLoopDataParser:
    ''' Test parser.'''
    def setup_class(self):
        '''Setup common data.'''
        self.data = "4C4F4FC4006802547B52031EFF7FFFFFFF7FFFFFFFFFFFFF" \
                    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF7F0000" \
                    "FFFF000000003C03000000000000FFFFFFFFFFFFFF000000" \
                    "0000000000000000000000000000008C00060C610183070A" \
                    "0D2A3C"
        self.bytes = hex_to_bytes(self.data)

    def test_check_crc(self):
        '''Test crc verification.'''
        assert VantageProCRC(self.bytes).check()

    def test_check_raw_data(self):
        item = LoopDataParserRevB(self.bytes, datetime.now())
        assert item.raw.replace(' ', '') == self.data
        assert item.raw_bytes == self.bytes

    def test_unpack(self):
        '''Test unpack loop packet.'''
        item = LoopDataParserRevB(self.bytes, datetime.now())

        assert item['Alarm01HighLeafTemp'] == 0
        assert item['Alarm01HighLeafWet'] == 0
        assert item['Alarm01HighSoilMois'] == 0
        assert item['Alarm01HighSoilTemp'] == 0
        assert item['Alarm01LowLeafTemp'] == 0
        assert item['Alarm01LowLeafWet'] == 0
        assert item['Alarm01LowSoilMois'] == 0
        assert item['Alarm01LowSoilTemp'] == 0
        assert item['AlarmEx01HighHum'] == 0
        assert item['AlarmInFallBarTrend'] == 0
        assert item['AlarmOut10minAvgSpeed'] == 0
        assert item['AlarmRain15min'] == 0
        assert item['BarTrend'] == 196
        assert item['Barometer'] == 31.572
        assert item['BatteryStatus'] == 0
        assert item['BatteryVolts'] == 0.8203125
        assert item['ETDay'] == 0.0
        assert item['ETMonth'] == 0.0
        assert item['ETYear'] == 0.0
        assert item['ExtraTemps01'] == 255
        assert item['ForecastIcon'] == 6
        assert item['ForecastRuleNo'] == 12
        assert item['HumExtra01'] == 255
        assert item['HumIn'] == 30
        assert item['HumOut'] == 255
        assert item['LeafTemps01'] == 255
        assert item['LeafWetness01'] == 255
        assert item['LeafWetness04'] == 0
        assert item['RainDay'] == 0.0
        assert item['RainMonth'] == 0.0
        assert item['RainRate'] == 655.35
        assert item['RainStorm'] == 0.0
        assert item['RainYear'] == 8.28
        assert item['SoilMoist01'] == 255
        assert item['SolarRad'] == 32767
        assert item['StormStartDate'] is None
        assert item['SunRise'] == '03:53'
        assert item['SunSet'] == '19:23'
        assert item['TempIn'] == 85.0
        assert item['TempOut'] == 3276.7
        assert item['UV'] == 255
        assert item['WindDir'] == 32767
        assert item['WindSpeed'] == 255
        assert item['WindSpeed10Min'] == 255

    def test_unpack_storm_date_valid_datestamp(self):
        raw = bytearray(self.bytes)
        packed = 2 + 3 * 32 + (2024 - 2000) * 512  # 2024-03-02
        raw[48:50] = struct.pack(b'<H', packed)
        item = LoopDataParserRevB(bytes(raw), datetime.now())
        assert item['StormStartDate'] == '2024-03-02'

    def test_unpack_storm_date_recent_example(self):
        raw = bytearray(self.bytes)
        packed = 19 + 2 * 32 + (2026 - 2000) * 512  # 2026-02-19
        raw[48:50] = struct.pack(b'<H', packed)
        item = LoopDataParserRevB(bytes(raw), datetime.now())
        assert item['StormStartDate'] == '2026-02-19'


def test_datetime_parser():
    '''Test pack and unpack datetime.'''
    data = hex_to_bytes("25 35 0A 07 06 70 60 BA")
    assert VantageProCRC(data).check()
    date = unpack_datetime(data)
    assert date == datetime(2012, 6, 7, 10, 53, 37)
    assert data == pack_datetime(date)


def test_dump_date_time():
    # Build a deterministic datetime for round-trip verification.
    d = datetime(2012, 10, 26, 10, 10)
    # Encode datetime into Davis DateStamp/TimeStamp plus CRC.
    packed = pack_dmp_date_time(d)
    # Unpack encoded payload into date, time, and CRC words.
    date, time, _ = struct.unpack(b"HHH", packed)
    # Ensure decoded date/time exactly matches the original.
    assert d == unpack_dmp_date_time(date, time)


def test_archive_rain_rate_scaling():
    # Encode 2024-03-02 using Davis packed archive date format.
    date = 2 + 3 * 32 + (2024 - 2000) * 512
    # Use 12:34 packed as HHMM.
    time = 1234
    # Build one full binary archive record with known rain-rate values.
    raw = struct.pack(
        b'=HHHHHHHHHHHBBBBBBBBHBB2s2s4sB2s3s4s',
        date, time,         # DateStamp, TimeStamp
        700, 710, 690,      # TempOut, TempOutHi, TempOutLow
        123, 456,           # RainRate, RainRateHi
        30000, 500, 6,      # Barometer, SolarRad, WindSamps
        680,                # TempIn
        50, 51, 3, 8, 4, 5, 9, 20,  # HumIn..ETHour
        700, 25, 1,         # SolarRadHi, UVHi, ForecastRuleNo
        b'\x64\x65', b'\x01\x02', b'\x5A\x5B\x5C\x5D',  # Leaf/Soil temps
        0,                  # RecType
        b'\x32\x33', b'\x60\x61\x62', b'\x10\x11\x12\x13',  # Extra*
    )
    # Parse binary payload using archive parser under test.
    item = ArchiveDataParserRevB(raw)
    # Verify rain rate converts from hundredths to engineering units.
    assert item['RainRate'] == 1.23
    # Verify rain-rate high-watermark uses identical scaling.
    assert item['RainRateHi'] == 4.56
