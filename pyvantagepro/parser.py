# -*- coding: utf-8 -*-
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro.parser
    # Pedagogical note: this line is part of the step-by-step program flow.
    -------------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    Allows parsing Vantage Pro2 data.

    # Pedagogical note: this line is part of the step-by-step program flow.
    Original Author: Patrick C. McGinty (pyweather@tuxcoder.com)
    # Pedagogical note: this line is part of the step-by-step program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: this line is part of the step-by-step program flow.
    :license: GNU GPL v3.

# Pedagogical note: this line is part of the step-by-step program flow.
'''
# Pedagogical note: this line is part of the step-by-step program flow.
from __future__ import division, unicode_literals
# Pedagogical note: this line is part of the step-by-step program flow.
import struct
# Pedagogical note: this line is part of the step-by-step program flow.
from datetime import datetime
# Pedagogical note: this line is part of the step-by-step program flow.
from array import array

# Pedagogical note: this line is part of the step-by-step program flow.
from .compat import bytes
# Pedagogical note: this line is part of the step-by-step program flow.
from .logger import LOGGER
# Pedagogical note: this line is part of the step-by-step program flow.
from .utils import (cached_property, bytes_to_hex, Dict, bytes_to_binary,
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    binary_to_int)


# Pedagogical note: this line is part of the step-by-step program flow.
class VantageProCRC(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Implements CRC algorithm, necessary for encoding and verifying data from
    # Pedagogical note: this line is part of the step-by-step program flow.
    the Davis Vantage Pro unit.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    CRC_TABLE = (
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x0,    0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7, 0x8108,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef, 0x1231, 0x210,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6, 0x9339, 0x8318, 0xb37b,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de, 0x2462, 0x3443, 0x420,  0x1401,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x64e6, 0x74c7, 0x44a4, 0x5485, 0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xf5cf, 0xc5ac, 0xd58d, 0x3653, 0x2672, 0x1611, 0x630,  0x76d7, 0x66f6,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x5695, 0x46b4, 0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xc7bc, 0x48c4, 0x58e5, 0x6886, 0x78a7, 0x840,  0x1861, 0x2802, 0x3823,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b, 0x5af5,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0xa50,  0x3a33, 0x2a12, 0xdbfd, 0xcbdc,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a, 0x6ca6, 0x7c87, 0x4ce4,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x5cc5, 0x2c22, 0x3c03, 0xc60,  0x1c41, 0xedae, 0xfd8f, 0xcdec, 0xddcd,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xad2a, 0xbd0b, 0x8d68, 0x9d49, 0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x2e32, 0x1e51, 0xe70,  0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x9f59, 0x8f78, 0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xe16f, 0x1080, 0xa1,   0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e, 0x2b1,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256, 0xb5ea, 0xa5cb,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d, 0x34e2, 0x24c3, 0x14a0,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x481,  0x7466, 0x6447, 0x5424, 0x4405, 0xa7db, 0xb7fa, 0x8799, 0x97b8,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xe75f, 0xf77e, 0xc71d, 0xd73c, 0x26d3, 0x36f2, 0x691,  0x16b0, 0x6657,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x7676, 0x4615, 0x5634, 0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xb98a, 0xa9ab, 0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x8e1,  0x3882,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x28a3, 0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x4a75, 0x5a54, 0x6a37, 0x7a16, 0xaf1,  0x1ad0, 0x2ab3, 0x3a92, 0xfd2e,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9, 0x7c26, 0x6c07,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0xcc1,  0xef1f, 0xff3e, 0xcf5d,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8, 0x6e17, 0x7e36, 0x4e55, 0x5e74,
        # Pedagogical note: this line is part of the step-by-step program flow.
        0x2e93, 0x3eb2, 0xed1,  0x1ef0,
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, data):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.data = data

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def checksum(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Return CRC calc value from raw serial data.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        crc = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        for byte in array(str('B'), bytes(self.data)):
            # Pedagogical note: this line is part of the step-by-step program flow.
            crc = (self.CRC_TABLE[((crc >> 8) ^ byte)] ^ ((crc & 0xFF) << 8))
        # Pedagogical note: this line is part of the step-by-step program flow.
        return crc

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def data_with_checksum(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Return packed raw CRC from raw data.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        checksum = struct.pack(b'>H', self.checksum)
        # Pedagogical note: this line is part of the step-by-step program flow.
        return b''.join([self.data, checksum])

    # Pedagogical note: this line is part of the step-by-step program flow.
    def check(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Perform CRC check on raw serial data, return true if valid.
        # Pedagogical note: this line is part of the step-by-step program flow.
        A valid CRC == 0.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        if len(self.data) != 0 and self.checksum == 0:
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.info("Check CRC : OK")
            # Pedagogical note: this line is part of the step-by-step program flow.
            return True
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.error("Check CRC : BAD")
            # Pedagogical note: this line is part of the step-by-step program flow.
            return False


# Pedagogical note: this line is part of the step-by-step program flow.
class DataParser(Dict):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Implements a reusable class for working with a binary data structure.
    # Pedagogical note: this line is part of the step-by-step program flow.
    It provides a named fields interface, similiar to C structures.'''

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, data, data_format, order='='):
        # Pedagogical note: this line is part of the step-by-step program flow.
        super(DataParser, self).__init__()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.fields, format_t = zip(*data_format)
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.crc_error = False
        # Pedagogical note: this line is part of the step-by-step program flow.
        if "CRC" in self.fields:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.crc_error = not VantageProCRC(data).check()
        # Pedagogical note: this line is part of the step-by-step program flow.
        format_t = str("%s%s" % (order, ''.join(format_t)))
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.struct = struct.Struct(format=format_t)
        # save raw_bytes
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.raw_bytes = data
        # Unpacks data from `raw_bytes` and returns a dication of named fields
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.struct.unpack_from(self.raw_bytes, 0)
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['Datetime'] = None
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.update(Dict(zip(self.fields, data)))

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def raw(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return bytes_to_hex(self.raw_bytes)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def tuple_to_dict(self, key):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Convert {key<->tuple} to {key1<->value2, key2<->value2 ... }.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        for i, value in enumerate(self[key]):
            # Pedagogical note: this line is part of the step-by-step program flow.
            self["%s%.2d" % (key, i + 1)] = value
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self[key]

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __unicode__(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        name = self.__class__.__name__
        # Pedagogical note: this line is part of the step-by-step program flow.
        return "<%s %s>" % (name, self.raw)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __str__(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return str(self.__unicode__())

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __repr__(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return str(self.__unicode__())


# Pedagogical note: this line is part of the step-by-step program flow.
class LoopDataParserRevB(DataParser):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Parse data returned by the 'LOOP' command. It contains all of the
    # Pedagogical note: this line is part of the step-by-step program flow.
    real-time data that can be read from the Davis VantagePro2.'''
    # Loop data format (RevB)
    # Pedagogical note: this line is part of the step-by-step program flow.
    LOOP_FORMAT = (
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('LOO', '3s'), ('BarTrend', 'B'), ('PacketType', 'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('NextRec', 'H'), ('Barometer', 'H'), ('TempIn', 'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('HumIn', 'B'), ('TempOut', 'H'), ('WindSpeed', 'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('WindSpeed10Min', 'B'), ('WindDir', 'H'), ('ExtraTemps', '7s'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('SoilTemps', '4s'), ('LeafTemps', '4s'), ('HumOut', 'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('HumExtra', '7s'), ('RainRate', 'H'), ('UV', 'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('SolarRad', 'H'), ('RainStorm', 'H'), ('StormStartDate', 'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('RainDay', 'H'), ('RainMonth', 'H'), ('RainYear', 'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('ETDay', 'H'), ('ETMonth', 'H'), ('ETYear', 'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('SoilMoist', '4s'), ('LeafWetness', '4s'), ('AlarmIn', 'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('AlarmRain', 'B'), ('AlarmOut', '2s'), ('AlarmExTempHum', '8s'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('AlarmSoilLeaf', '4s'), ('BatteryStatus', 'B'), ('BatteryVolts', 'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('ForecastIcon', 'B'), ('ForecastRuleNo', 'B'), ('SunRise', 'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('SunSet', 'H'), ('EOL', '2s'), ('CRC', 'H'),
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, data, dtime):
        # Pedagogical note: this line is part of the step-by-step program flow.
        super(LoopDataParserRevB, self).__init__(data, self.LOOP_FORMAT)
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['Datetime'] = dtime
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['Barometer'] = self['Barometer'] / 1000
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['TempIn'] = self['TempIn'] / 10
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['TempOut'] = self['TempOut'] / 10
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['RainRate'] = self['RainRate'] / 100
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['RainStorm'] = self['RainStorm'] / 100
        # Given a packed storm date field, unpack and return date
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['StormStartDate'] = self.unpack_storm_date()
        # rain totals
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['RainDay'] = self['RainDay'] / 100
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['RainMonth'] = self['RainMonth'] / 100
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['RainYear'] = self['RainYear'] / 100
        # evapotranspiration totals
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['ETDay'] = self['ETDay'] / 1000
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['ETMonth'] = self['ETMonth'] / 100
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['ETYear'] = self['ETYear'] / 100
        # battery statistics
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['BatteryVolts'] = self['BatteryVolts'] * 300 / 512 / 100
        # sunrise / sunset
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['SunRise'] = self.unpack_time(self['SunRise'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['SunSet'] = self.unpack_time(self['SunSet'])
        # convert to int
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['HumExtra'] = struct.unpack(b'7B', self['HumExtra'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['ExtraTemps'] = struct.unpack(b'7B', self['ExtraTemps'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['SoilMoist'] = struct.unpack(b'4B', self['SoilMoist'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['SoilTemps'] = struct.unpack(b'4B', self['SoilTemps'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['LeafWetness'] = struct.unpack(b'4B', self['LeafWetness'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['LeafTemps'] = struct.unpack(b'4B', self['LeafTemps'])

        # Inside Alarms bits extraction, only 7 bits are used
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmIn'] = bytes_to_binary(self.raw_bytes[70])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmInFallBarTrend'] = int(self['AlarmIn'][0])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmInRisBarTrend'] = int(self['AlarmIn'][1])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmInLowTemp'] = int(self['AlarmIn'][2])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmInHighTemp'] = int(self['AlarmIn'][3])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmInLowHum'] = int(self['AlarmIn'][4])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmInHighHum'] = int(self['AlarmIn'][5])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmInTime'] = int(self['AlarmIn'][6])
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['AlarmIn']
        # Rain Alarms bits extraction, only 5 bits are used
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmRain'] = bytes_to_binary(self.raw_bytes[71])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmRainHighRate'] = int(self['AlarmRain'][0])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmRain15min'] = int(self['AlarmRain'][1])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmRain24hour'] = int(self['AlarmRain'][2])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmRainStormTotal'] = int(self['AlarmRain'][3])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmRainETDaily'] = int(self['AlarmRain'][4])
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['AlarmRain']
        # Oustide Alarms bits extraction, only 13 bits are used
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOut'] = bytes_to_binary(self.raw_bytes[72])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutLowTemp'] = int(self['AlarmOut'][0])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutHighTemp'] = int(self['AlarmOut'][1])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutWindSpeed'] = int(self['AlarmOut'][2])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOut10minAvgSpeed'] = int(self['AlarmOut'][3])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutLowDewpoint'] = int(self['AlarmOut'][4])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutHighDewPoint'] = int(self['AlarmOut'][5])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutHighHeat'] = int(self['AlarmOut'][6])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutLowWindChill'] = int(self['AlarmOut'][7])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOut'] = bytes_to_binary(self.raw_bytes[73])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutHighTHSW'] = int(self['AlarmOut'][0])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutHighSolarRad'] = int(self['AlarmOut'][1])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutHighUV'] = int(self['AlarmOut'][2])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutUVDose'] = int(self['AlarmOut'][3])
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['AlarmOutUVDoseEnabled'] = int(self['AlarmOut'][4])
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['AlarmOut']
        # AlarmExTempHum bits extraction, only 3 bits are used, but 7 bytes
        # Pedagogical note: this line is part of the step-by-step program flow.
        for i in range(1, 8):
            # Pedagogical note: this line is part of the step-by-step program flow.
            data = self.raw_bytes[74 + i]
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['AlarmExTempHum'] = bytes_to_binary(data)
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['AlarmEx%.2dLowTemp' % i] = int(self['AlarmExTempHum'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['AlarmEx%.2dHighTemp' % i] = int(self['AlarmExTempHum'][1])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['AlarmEx%.2dLowHum' % i] = int(self['AlarmExTempHum'][2])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['AlarmEx%.2dHighHum' % i] = int(self['AlarmExTempHum'][3])
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['AlarmExTempHum']
        # AlarmSoilLeaf 8bits, 4 bytes
        # Pedagogical note: this line is part of the step-by-step program flow.
        for i in range(1, 5):
            # Pedagogical note: this line is part of the step-by-step program flow.
            data = self.raw_bytes[81 + i]
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['AlarmSoilLeaf'] = bytes_to_binary(data)
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dLowLeafWet' % i] = int(self['AlarmSoilLeaf'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dHighLeafWet' % i] = int(self['AlarmSoilLeaf'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dLowSoilMois' % i] = int(self['AlarmSoilLeaf'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dHighSoilMois' % i] = int(self['AlarmSoilLeaf'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dLowLeafTemp' % i] = int(self['AlarmSoilLeaf'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dHighLeafTemp' % i] = int(self['AlarmSoilLeaf'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dLowSoilTemp' % i] = int(self['AlarmSoilLeaf'][0])
            # Pedagogical note: this line is part of the step-by-step program flow.
            self['Alarm%.2dHighSoilTemp' % i] = int(self['AlarmSoilLeaf'][0])
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['AlarmSoilLeaf']
        # delete unused values
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['LOO']
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['NextRec']
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['PacketType']
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['EOL']
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['CRC']
        # Tuple to dict
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("ExtraTemps")
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("LeafTemps")
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("SoilTemps")
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("HumExtra")
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("LeafWetness")
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("SoilMoist")

    # Pedagogical note: this line is part of the step-by-step program flow.
    def unpack_storm_date(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Given a packed storm date field, unpack and return date.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        date = bytes_to_binary(self.raw_bytes[48:50])
        # Pedagogical note: this line is part of the step-by-step program flow.
        year = binary_to_int(date, 0, 7) + 2000
        # Pedagogical note: this line is part of the step-by-step program flow.
        day = binary_to_int(date, 7, 12)
        # Pedagogical note: this line is part of the step-by-step program flow.
        month = binary_to_int(date, 12, 16)
        # Pedagogical note: this line is part of the step-by-step program flow.
        return "%s-%s-%s" % (year, month, day)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def unpack_time(self, time):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Given a packed time field, unpack and return "HH:MM" string.'''
        # format: HHMM, and space padded on the left.ex: "601" is 6:01 AM
        # Pedagogical note: this line is part of the step-by-step program flow.
        return "%02d:%02d" % divmod(time, 100)  # covert to "06:01"


# Pedagogical note: this line is part of the step-by-step program flow.
class ArchiveDataParserRevB(DataParser):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Parse data returned by the 'LOOP' command. It contains all of the
    # Pedagogical note: this line is part of the step-by-step program flow.
    real-time data that can be read from the Davis VantagePro2.'''

    # Pedagogical note: this line is part of the step-by-step program flow.
    ARCHIVE_FORMAT = (
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('DateStamp',      'H'), ('TimeStamp',   'H'), ('TempOut',      'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('TempOutHi',      'H'), ('TempOutLow',  'H'), ('RainRate',     'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('RainRateHi',     'H'), ('Barometer',   'H'), ('SolarRad',     'H'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('WindSamps',      'H'), ('TempIn',      'H'), ('HumIn',        'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('HumOut',         'B'), ('WindAvg',     'B'), ('WindHi',       'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('WindHiDir',      'B'), ('WindAvgDir',  'B'), ('UV',           'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('ETHour',         'B'), ('SolarRadHi',  'H'), ('UVHi',         'B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('ForecastRuleNo', 'B'), ('LeafTemps',  '2s'), ('LeafWetness', '2s'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('SoilTemps',     '4s'), ('RecType',     'B'), ('ExtraHum',    '2s'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('ExtraTemps',    '3s'), ('SoilMoist',  '4s'),
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, data):
        # Unpack archive bytes into named fields defined in ARCHIVE_FORMAT.
        # Pedagogical note: this line is part of the step-by-step program flow.
        super(ArchiveDataParserRevB, self).__init__(data, self.ARCHIVE_FORMAT)
        # Keep a bit-level view of the raw date/time header for diagnostics.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['raw_datestamp'] = bytes_to_binary(self.raw_bytes[0:4])
        # Convert Davis date/time words into a Python datetime object.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['Datetime'] = unpack_dmp_date_time(self['DateStamp'],
                                                # Pedagogical note: this line is part of the step-by-step program flow.
                                                self['TimeStamp'])
        # Remove raw timestamp words after deriving the normalized datetime.
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['DateStamp']
        # Pedagogical note: this line is part of the step-by-step program flow.
        del self['TimeStamp']
        # Convert tenths of degrees F to degrees F.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['TempOut'] = self['TempOut'] / 10
        # Convert tenths of degrees F to degrees F.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['TempOutHi'] = self['TempOutHi'] / 10
        # Convert tenths of degrees F to degrees F.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['TempOutLow'] = self['TempOutLow'] / 10
        # Convert hundredths of in/hr to in/hr.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['RainRate'] = self['RainRate'] / 100
        # Convert hundredths of in/hr to in/hr.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['RainRateHi'] = self['RainRateHi'] / 100
        # Convert thousandths of inHg to inHg.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['Barometer'] = self['Barometer'] / 1000
        # Convert tenths of degrees F to degrees F.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['TempIn'] = self['TempIn'] / 10
        # Convert tenths UV index to UV index.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['UV'] = self['UV'] / 10
        # Convert thousandths inches to inches for hourly ET.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['ETHour'] = self['ETHour'] / 1000
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['WindHiDir'] = int(self['WindHiDir'] * 22.5)
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['WindAvgDir'] = int(self['WindAvgDir'] * 22.5)
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''
        # Decode 4 packed soil temperature bytes.
        # Pedagogical note: this line is part of the step-by-step program flow.
        SoilTempsValues = struct.unpack(b'4B', self['SoilTemps'])
        # Convert Davis soil temp encoding (offset +90) to actual values.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['SoilTemps'] = tuple((t - 90) for t in SoilTempsValues)

        # Decode 2 packed extra humidity channels.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['ExtraHum'] = struct.unpack(b'2B', self['ExtraHum'])
        # Decode 4 packed soil moisture channels.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['SoilMoist'] = struct.unpack(b'4B', self['SoilMoist'])
        # Decode 2 packed leaf temperature bytes.
        # Pedagogical note: this line is part of the step-by-step program flow.
        LeafTempsValues = struct.unpack(b'2B', self['LeafTemps'])
        # Convert Davis leaf temp encoding (offset +90) to actual values.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['LeafTemps'] = tuple((t - 90) for t in LeafTempsValues)
        # Decode 2 packed leaf wetness channels.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['LeafWetness'] = struct.unpack(b'2B', self['LeafWetness'])
        # Decode 3 packed extra temperature bytes.
        # Pedagogical note: this line is part of the step-by-step program flow.
        ExtraTempsValues = struct.unpack(b'3B', self['ExtraTemps'])
        # Convert Davis extra temp encoding (offset +90) to actual values.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self['ExtraTemps'] = tuple((t - 90) for t in ExtraTempsValues)
        # Expand tuple fields into numbered scalar keys (SoilTemps01, etc.).
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("SoilTemps")
        # Expand tuple fields into numbered scalar keys (LeafTemps01, etc.).
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("LeafTemps")
        # Expand tuple fields into numbered scalar keys (ExtraTemps01, etc.).
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("ExtraTemps")
        # Expand tuple fields into numbered scalar keys (SoilMoist01, etc.).
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("SoilMoist")
        # Expand tuple fields into numbered scalar keys (LeafWetness01, etc.).
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("LeafWetness")
        # Expand tuple fields into numbered scalar keys (ExtraHum01, etc.).
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.tuple_to_dict("ExtraHum")


# Pedagogical note: this line is part of the step-by-step program flow.
class DmpHeaderParser(DataParser):
    # Pedagogical note: this line is part of the step-by-step program flow.
    DMP_FORMAT = (
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('Pages',   'H'),  ('Offset',   'H'),  ('CRC',     'H'),
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, data):
        # Pedagogical note: this line is part of the step-by-step program flow.
        super(DmpHeaderParser, self).__init__(data, self.DMP_FORMAT)


# Pedagogical note: this line is part of the step-by-step program flow.
class DmpPageParser(DataParser):
    # Pedagogical note: this line is part of the step-by-step program flow.
    DMP_FORMAT = (
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('Index',   'B'),  ('Records',   '260s'),  ('unused',     '4B'),
        # Pedagogical note: this line is part of the step-by-step program flow.
        ('CRC',   'H'),
    # Pedagogical note: this line is part of the step-by-step program flow.
    )

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, data):
        # Pedagogical note: this line is part of the step-by-step program flow.
        super(DmpPageParser, self).__init__(data, self.DMP_FORMAT)


# Pedagogical note: this line is part of the step-by-step program flow.
def pack_dmp_date_time(d):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Pack `datetime` to DateStamp and TimeStamp VantagePro2 with CRC.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    vpdate = d.day + d.month * 32 + (d.year - 2000) * 512
    # Pedagogical note: this line is part of the step-by-step program flow.
    vptime = 100 * d.hour + d.minute
    # Pedagogical note: this line is part of the step-by-step program flow.
    data = struct.pack(b'HH', vpdate, vptime)
    # Pedagogical note: this line is part of the step-by-step program flow.
    return VantageProCRC(data).data_with_checksum


# Pedagogical note: this line is part of the step-by-step program flow.
def unpack_dmp_date_time(date, time):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Unpack `date` and `time` to datetime'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    if date != 0xffff and time != 0xffff:
        # Pedagogical note: this line is part of the step-by-step program flow.
        day = date & 0x1f                     # 5 bits
        # Pedagogical note: this line is part of the step-by-step program flow.
        month = (date >> 5) & 0x0f            # 4 bits
        # Pedagogical note: this line is part of the step-by-step program flow.
        year = ((date >> 9) & 0x7f) + 2000    # 7 bits
        # Pedagogical note: this line is part of the step-by-step program flow.
        hour, min_ = divmod(time, 100)
        # Pedagogical note: this line is part of the step-by-step program flow.
        return datetime(year, month, day, hour, min_)


# Pedagogical note: this line is part of the step-by-step program flow.
def pack_datetime(dtime):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Returns packed `dtime` with CRC.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    data = struct.pack(b'>BBBBBB', dtime.second, dtime.minute,
                       # Pedagogical note: this line is part of the step-by-step program flow.
                       dtime.hour, dtime.day, dtime.month, dtime.year - 1900)
    # Pedagogical note: this line is part of the step-by-step program flow.
    return VantageProCRC(data).data_with_checksum


# Pedagogical note: this line is part of the step-by-step program flow.
def unpack_datetime(data):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Return unpacked datetime `data` and check CRC.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    VantageProCRC(data).check()
    # Pedagogical note: this line is part of the step-by-step program flow.
    s, m, h, day, month, year = struct.unpack(b'>BBBBBB', data[:6])
    # Pedagogical note: this line is part of the step-by-step program flow.
    return datetime(year + 1900, month, day, h, m, s)
