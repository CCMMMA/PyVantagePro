# -*- coding: utf-8 -*-
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro.device
    # Pedagogical note: this line is part of the step-by-step program flow.
    -------------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    Allows data query of Davis Vantage Pro2 devices

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
import errno
# Pedagogical note: this line is part of the step-by-step program flow.
from datetime import datetime, timedelta
# Pedagogical note: this line is part of the step-by-step program flow.
from pylink import link_from_url, SerialLink

# Pedagogical note: this line is part of the step-by-step program flow.
from .logger import LOGGER
# Pedagogical note: this line is part of the step-by-step program flow.
from .utils import (cached_property, retry, bytes_to_hex,
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    ListDict, is_bytes)

# Pedagogical note: this line is part of the step-by-step program flow.
from .parser import (LoopDataParserRevB, DmpHeaderParser, DmpPageParser,
                     # Pedagogical note: this line is part of the step-by-step program flow.
                     ArchiveDataParserRevB, VantageProCRC, pack_datetime,
                     # Pedagogical note: this line is part of the step-by-step program flow.
                     unpack_datetime, pack_dmp_date_time)


# Pedagogical note: this line is part of the step-by-step program flow.
class NoDeviceException(Exception):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Can not access weather station.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    value = __doc__


# Pedagogical note: this line is part of the step-by-step program flow.
class BadAckException(Exception):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''No valid acknowledgement.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __str__(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.__doc__


# Pedagogical note: this line is part of the step-by-step program flow.
class BadCRCException(Exception):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''No valid checksum.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __str__(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.__doc__


# Pedagogical note: this line is part of the step-by-step program flow.
class BadDataException(Exception):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''No valid data.'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    def __str__(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.__doc__


# Pedagogical note: this line is part of the step-by-step program flow.
class VantagePro2(object):
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''Communicates with the station by sending commands, reads the binary
    # Pedagogical note: this line is part of the step-by-step program flow.
    data and parsing it into usable scalar values.

    # Pedagogical note: this line is part of the step-by-step program flow.
    :param link: A `PyLink` connection.
    # Pedagogical note: this line is part of the step-by-step program flow.
    '''

    # device reply commands
    # Pedagogical note: this line is part of the step-by-step program flow.
    WAKE_STR = '\n'
    # Pedagogical note: this line is part of the step-by-step program flow.
    WAKE_ACK = '\n\r'
    # Pedagogical note: this line is part of the step-by-step program flow.
    ACK = '\x06'
    # Pedagogical note: this line is part of the step-by-step program flow.
    NACK = '\x21'
    # Pedagogical note: this line is part of the step-by-step program flow.
    DONE = 'DONE\n\r'
    # Pedagogical note: this line is part of the step-by-step program flow.
    CANCEL = '\x18'
    # Pedagogical note: this line is part of the step-by-step program flow.
    ESC = '\x1b'
    # Pedagogical note: this line is part of the step-by-step program flow.
    OK = '\n\rOK\n\r'

    # Pedagogical note: this line is part of the step-by-step program flow.
    def __init__(self, link, link_factory=None, timeout=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.link = link
        # Pedagogical note: this line is part of the step-by-step program flow.
        self._link_factory = link_factory
        # Pedagogical note: this line is part of the step-by-step program flow.
        self._timeout = timeout
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.link.open()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self._check_revision()

    # Pedagogical note: this line is part of the step-by-step program flow.
    @classmethod
    # Pedagogical note: this line is part of the step-by-step program flow.
    def from_url(cls, url, timeout=10):
        # Pedagogical note: this line is part of the step-by-step program flow.
        ''' Get device from url.

        # Pedagogical note: this line is part of the step-by-step program flow.
        :param url: A `PyLink` connection URL.
        # Pedagogical note: this line is part of the step-by-step program flow.
        :param timeout: Set a read timeout value.
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''
        # Pedagogical note: this line is part of the step-by-step program flow.
        def link_factory():
            # Pedagogical note: this line is part of the step-by-step program flow.
            link = link_from_url(url)
            # Pedagogical note: this line is part of the step-by-step program flow.
            link.settimeout(timeout)
            # Pedagogical note: this line is part of the step-by-step program flow.
            return link

        # Pedagogical note: this line is part of the step-by-step program flow.
        return cls(link_factory(), link_factory=link_factory, timeout=timeout)

    # Pedagogical note: this line is part of the step-by-step program flow.
    @classmethod
    # Pedagogical note: this line is part of the step-by-step program flow.
    def from_serial(cls, tty, baud, timeout=10):
        # Pedagogical note: this line is part of the step-by-step program flow.
        ''' Get device from serial port.

        # Pedagogical note: this line is part of the step-by-step program flow.
        :param url: A `PyLink` connection URL.
        # Pedagogical note: this line is part of the step-by-step program flow.
        :param timeout: Set a read timeout value.
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''
        # Pedagogical note: this line is part of the step-by-step program flow.
        def link_factory():
            # Pedagogical note: this line is part of the step-by-step program flow.
            link = SerialLink(tty, baud)
            # Pedagogical note: this line is part of the step-by-step program flow.
            link.settimeout(timeout)
            # Pedagogical note: this line is part of the step-by-step program flow.
            return link

        # Pedagogical note: this line is part of the step-by-step program flow.
        return cls(link_factory(), link_factory=link_factory, timeout=timeout)

    # Pedagogical note: this line is part of the step-by-step program flow.
    @retry(tries=3, delay=1)
    # Pedagogical note: this line is part of the step-by-step program flow.
    def wake_up(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Wakeup the station console.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        wait_ack = self.WAKE_ACK
        # Pedagogical note: this line is part of the step-by-step program flow.
        LOGGER.info("try wake up console")
        # Pedagogical note: this line is part of the step-by-step program flow.
        try:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link.write(self.WAKE_STR)
        # Pedagogical note: this line is part of the step-by-step program flow.
        except OSError as e:
            # Pedagogical note: this line is part of the step-by-step program flow.
            if self._recover_broken_pipe(e):
                # Pedagogical note: this line is part of the step-by-step program flow.
                raise NoDeviceException()
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise
        # Pedagogical note: this line is part of the step-by-step program flow.
        ack = self.link.read(len(wait_ack))
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self._is_wake_ack(ack):
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.info("Check ACK: OK (%s)" % (repr(ack)))
            # Pedagogical note: this line is part of the step-by-step program flow.
            return True
        #Sometimes we have a 1byte shift from Vantage Pro and that's why wake up doesn't work anymore
        #We just shift another 1byte to be aligned in the serial buffer again.
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.link.read(1)
        # Pedagogical note: this line is part of the step-by-step program flow.
        LOGGER.error("Check ACK: BAD (%s != %s)" % (repr(wait_ack), repr(ack)))
        # Pedagogical note: this line is part of the step-by-step program flow.
        raise NoDeviceException()

    # Pedagogical note: this line is part of the step-by-step program flow.
    @retry(tries=3, delay=0.5)
    # Pedagogical note: this line is part of the step-by-step program flow.
    def send(self, data, wait_ack=None, timeout=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Sends data to station.

         # Pedagogical note: this line is part of the step-by-step program flow.
         :param data: Can be a byte array or an ASCII command. If this is
            # Pedagogical note: this line is part of the step-by-step program flow.
            the case for an ascii command, a <LF> will be added.

         # Pedagogical note: this line is part of the step-by-step program flow.
         :param wait_ack: If `wait_ack` is not None, the function must check
            # Pedagogical note: this line is part of the step-by-step program flow.
            that acknowledgement is the one expected.

         # Pedagogical note: this line is part of the step-by-step program flow.
         :param timeout: Define this timeout when reading ACK from link﻿.
         # Pedagogical note: this line is part of the step-by-step program flow.
         '''
        # Pedagogical note: this line is part of the step-by-step program flow.
        if is_bytes(data):
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.info("try send : %s" % bytes_to_hex(data))
            # Pedagogical note: this line is part of the step-by-step program flow.
            try:
                # Pedagogical note: this line is part of the step-by-step program flow.
                self.link.write(data)
            # Pedagogical note: this line is part of the step-by-step program flow.
            except OSError as e:
                # Pedagogical note: this line is part of the step-by-step program flow.
                if self._recover_broken_pipe(e):
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    raise BadAckException()
                # Pedagogical note: this line is part of the step-by-step program flow.
                raise
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.info("try send : %s" % data)
            # Pedagogical note: this line is part of the step-by-step program flow.
            try:
                # Pedagogical note: this line is part of the step-by-step program flow.
                self.link.write("%s\n" % data)
            # Pedagogical note: this line is part of the step-by-step program flow.
            except OSError as e:
                # Pedagogical note: this line is part of the step-by-step program flow.
                if self._recover_broken_pipe(e):
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    raise BadAckException()
                # Pedagogical note: this line is part of the step-by-step program flow.
                raise
        # Pedagogical note: this line is part of the step-by-step program flow.
        if wait_ack is None:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return True
        # Pedagogical note: this line is part of the step-by-step program flow.
        ack = self.link.read(len(wait_ack), timeout=timeout)
        # Pedagogical note: this line is part of the step-by-step program flow.
        if wait_ack == ack:
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.info("Check ACK: OK (%s)" % (repr(ack)))
            # Pedagogical note: this line is part of the step-by-step program flow.
            return True
        # Pedagogical note: this line is part of the step-by-step program flow.
        LOGGER.error("Check ACK: BAD (%s != %s)" % (repr(wait_ack), repr(ack)))
        # Pedagogical note: this line is part of the step-by-step program flow.
        raise BadAckException()

    # Pedagogical note: this line is part of the step-by-step program flow.
    @retry(tries=3, delay=1)
    # Pedagogical note: this line is part of the step-by-step program flow.
    def read_from_eeprom(self, hex_address, size):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Reads from EEPROM the `size` number of bytes starting at the
        # Pedagogical note: this line is part of the step-by-step program flow.
        `hex_address`. Results are given as hex strings.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.link.write("EEBRD %s %.2d\n" % (hex_address, size))
        # Pedagogical note: this line is part of the step-by-step program flow.
        ack = self.link.read(len(self.ACK))
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self.ACK == ack:
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.info("Check ACK: OK (%s)" % (repr(ack)))
            # Pedagogical note: this line is part of the step-by-step program flow.
            data = self.link.read(size + 2)  # 2 bytes for CRC
            # Pedagogical note: this line is part of the step-by-step program flow.
            if VantageProCRC(data).check():
                # Pedagogical note: this line is part of the step-by-step program flow.
                return data[:-2]
            # Pedagogical note: this line is part of the step-by-step program flow.
            else:
                # Pedagogical note: this line is part of the step-by-step program flow.
                raise BadCRCException()
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            msg = "Check ACK: BAD (%s != %s)" % (repr(self.ACK), repr(ack))
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.error(msg)
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise BadAckException()

    # Pedagogical note: this line is part of the step-by-step program flow.
    def gettime(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns the current datetime of the console.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("GETTIME", self.ACK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.link.read(8)
        # Pedagogical note: this line is part of the step-by-step program flow.
        return unpack_datetime(data)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def settime(self, dtime):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Set the given `dtime` on the station.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("SETTIME", self.ACK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send(pack_datetime(dtime), self.ACK)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def getperiod(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns number of minutes in the archive period.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.archive_period

    # Pedagogical note: this line is part of the step-by-step program flow.
    def setperiod(self, dperiod):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Set the given `dperiod` on the station. Values are 1, 5, 10, 15, 30, 60, and 120'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send(f"SETPER {dperiod}", self.OK)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def getbar(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("BARDATA", self.OK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.link.read(97)
        # Pedagogical note: this line is part of the step-by-step program flow.
        return {
            # Pedagogical note: this line is part of the step-by-step program flow.
            key.lower().replace(" ", "_"): value
            # Pedagogical note: this line is part of the step-by-step program flow.
            for line in data.splitlines() if line.strip()
            # Pedagogical note: this line is part of the step-by-step program flow.
            for key, value in [line.rsplit(" ", 1)]
        # Pedagogical note: this line is part of the step-by-step program flow.
        }

    # Pedagogical note: this line is part of the step-by-step program flow.
    def getdiagnostics(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        return self.diagnostics

    # Pedagogical note: this line is part of the step-by-step program flow.
    def get_current_data(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns the real-time data as a `Dict`.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()

        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("LOOP 1", self.ACK)

        # Pedagogical note: this line is part of the step-by-step program flow.
        current_data = self.link.read(99)

        # Pedagogical note: this line is part of the step-by-step program flow.
        self.link.empty_socket()
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self.RevB:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return LoopDataParserRevB(current_data, datetime.now())
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise NotImplementedError('Do not support RevB data format')

    # Pedagogical note: this line is part of the step-by-step program flow.
    def meta(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Return the names of variables available from get_current_data().'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        return list(self.get_current_data().keys())

    # Pedagogical note: this line is part of the step-by-step program flow.
    def get_current_data_as_json(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Return get_current_data() as a JSON-serializable dict.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.get_current_data()
        # Pedagogical note: this line is part of the step-by-step program flow.
        payload = {}
        # Pedagogical note: this line is part of the step-by-step program flow.
        for key, value in data.items():
            # Pedagogical note: this line is part of the step-by-step program flow.
            if hasattr(value, 'isoformat'):
                # Pedagogical note: this line is part of the step-by-step program flow.
                try:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    payload[key] = value.isoformat(sep=' ')
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    continue
                # Pedagogical note: this line is part of the step-by-step program flow.
                except TypeError:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    payload[key] = value.isoformat()
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    continue
            # Pedagogical note: this line is part of the step-by-step program flow.
            payload[key] = value
        # Pedagogical note: this line is part of the step-by-step program flow.
        return payload

    # Pedagogical note: this line is part of the step-by-step program flow.
    def get_archives(self, start_date=None, stop_date=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Get archive records until `start_date` and `stop_date` as
        # Pedagogical note: this line is part of the step-by-step program flow.
        ListDict.

        # Pedagogical note: this line is part of the step-by-step program flow.
        :param start_date: The beginning datetime record.

        # Pedagogical note: this line is part of the step-by-step program flow.
        :param stop_date: The stopping datetime record.
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''
        # Pedagogical note: this line is part of the step-by-step program flow.
        generator = self._get_archives_generator(start_date, stop_date)
        # Pedagogical note: this line is part of the step-by-step program flow.
        archives = ListDict()
        # Pedagogical note: this line is part of the step-by-step program flow.
        dates = []
        # Pedagogical note: this line is part of the step-by-step program flow.
        for item in generator:
            # Pedagogical note: this line is part of the step-by-step program flow.
            if item['Datetime'] not in dates:
                # Pedagogical note: this line is part of the step-by-step program flow.
                archives.append(item)
                # Pedagogical note: this line is part of the step-by-step program flow.
                dates.append(item['Datetime'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        return archives.sorted_by('Datetime')

    # Pedagogical note: this line is part of the step-by-step program flow.
    def _get_archives_generator(self, start_date=None, stop_date=None):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Get archive records generator until `start_date` and `stop_date`.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # 2001-01-01 01:01:01
        # Pedagogical note: this line is part of the step-by-step program flow.
        start_date = start_date or datetime(2001, 1, 1, 1, 1, 1)
        # Pedagogical note: this line is part of the step-by-step program flow.
        stop_date = stop_date or datetime.now()
        # round start_date, with the archive period to the previous record
        # Pedagogical note: this line is part of the step-by-step program flow.
        period = self.archive_period
        # Pedagogical note: this line is part of the step-by-step program flow.
        minutes = (start_date.minute % period)
        # Pedagogical note: this line is part of the step-by-step program flow.
        start_date = start_date - timedelta(minutes=minutes)
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("DMPAFT", self.ACK)
        # I think that date_time_crc is incorrect...
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.link.write(pack_dmp_date_time(start_date))
        # timeout must be at least 2 seconds
        # Pedagogical note: this line is part of the step-by-step program flow.
        ack = self.link.read(len(self.ACK), timeout=2)
        # Pedagogical note: this line is part of the step-by-step program flow.
        if ack != self.ACK:
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise BadAckException()
        # Read dump header and get number of pages
        # Pedagogical note: this line is part of the step-by-step program flow.
        header = DmpHeaderParser(self.link.read(6))
        # Write ACK if crc is good. Else, send cancel.
        # Pedagogical note: this line is part of the step-by-step program flow.
        if header.crc_error:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link.write(self.CANCEL)
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise BadCRCException()
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link.write(self.ACK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        LOGGER.info('Starting download %d dump pages' % header['Pages'])
        # Pedagogical note: this line is part of the step-by-step program flow.
        finish = False
        # Pedagogical note: this line is part of the step-by-step program flow.
        r_index = 0
        # Pedagogical note: this line is part of the step-by-step program flow.
        for i in range(header['Pages']):
            # Read one dump page
            # Pedagogical note: this line is part of the step-by-step program flow.
            try:
                # Pedagogical note: this line is part of the step-by-step program flow.
                dump = self._read_dump_page()
            # Pedagogical note: this line is part of the step-by-step program flow.
            except (BadCRCException, BadDataException) as e:
                # Pedagogical note: this line is part of the step-by-step program flow.
                LOGGER.error('Error: %s' % e)
                # Pedagogical note: this line is part of the step-by-step program flow.
                finish = True
                # Pedagogical note: this line is part of the step-by-step program flow.
                break
            # Pedagogical note: this line is part of the step-by-step program flow.
            LOGGER.info('Dump page no %d ' % dump['Index'])
            # Get the 5 raw records
            # Pedagogical note: this line is part of the step-by-step program flow.
            raw_records = dump["Records"]
            # loop through archive records
            # Pedagogical note: this line is part of the step-by-step program flow.
            offsets = zip(range(0, 260, 52), range(52, 261, 52))
            # offsets = [(0, 52), (52, 104), ... , (156, 208), (208, 260)]
            # Pedagogical note: this line is part of the step-by-step program flow.
            for offset in offsets:
                # Pedagogical note: this line is part of the step-by-step program flow.
                raw_record = raw_records[offset[0]:offset[1]]
                # Pedagogical note: this line is part of the step-by-step program flow.
                if self.RevB:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    record = ArchiveDataParserRevB(raw_record)
                # Pedagogical note: this line is part of the step-by-step program flow.
                else:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    msg = 'Do not support RevA data format'
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    raise NotImplementedError(msg)
                # verify that record has valid data, and store
                # Pedagogical note: this line is part of the step-by-step program flow.
                r_time = record['Datetime']
                # Pedagogical note: this line is part of the step-by-step program flow.
                if r_time is None:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    LOGGER.error('Invalid record detected')
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    finish = True
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    break
                # Pedagogical note: this line is part of the step-by-step program flow.
                elif r_time <= stop_date:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    if start_date < r_time:
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        not_in_range = False
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        msg = "Record-%.4d - Datetime : %s" % (r_index, r_time)
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        LOGGER.info(msg)
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        yield record
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    else:
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        not_in_range = True
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        LOGGER.info('The record is not in the datetime range')
                # Pedagogical note: this line is part of the step-by-step program flow.
                else:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    LOGGER.error('Invalid record detected')
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    finish = True
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    break
                # Pedagogical note: this line is part of the step-by-step program flow.
                r_index += 1
            # Pedagogical note: this line is part of the step-by-step program flow.
            if finish:
                # Pedagogical note: this line is part of the step-by-step program flow.
                LOGGER.info('Canceling download : Finish')
                # Pedagogical note: this line is part of the step-by-step program flow.
                self.link.write(self.ESC)
                # Pedagogical note: this line is part of the step-by-step program flow.
                break
            # Pedagogical note: this line is part of the step-by-step program flow.
            elif not_in_range:
                # Pedagogical note: this line is part of the step-by-step program flow.
                msg = 'Page is not in the datetime range'
                # Pedagogical note: this line is part of the step-by-step program flow.
                LOGGER.info('Canceling download : %s' % msg)
                # Pedagogical note: this line is part of the step-by-step program flow.
                self.link.write(self.ESC)
                # Pedagogical note: this line is part of the step-by-step program flow.
                break
            # Pedagogical note: this line is part of the step-by-step program flow.
            else:
                # Pedagogical note: this line is part of the step-by-step program flow.
                if header['Pages'] - 1 == i:
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    LOGGER.info('Start downloading next page')
                # Pedagogical note: this line is part of the step-by-step program flow.
                self.link.write(self.ACK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        LOGGER.info('Pages Downloading process was finished')

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def archive_period(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns number of minutes in the archive period.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        return struct.unpack(b'B', self.read_from_eeprom("2D", 1))[0]

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def timezone(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns timezone offset as string.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.read_from_eeprom("14", 3)
        # Pedagogical note: this line is part of the step-by-step program flow.
        offset, gmt = struct.unpack(b'HB', data)
        # Pedagogical note: this line is part of the step-by-step program flow.
        if gmt == 1:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return "GMT+%.2f" % (offset / 100)
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return "Localtime"

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def firmware_date(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Return the firmware date code'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("VER", self.OK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.link.read(13)
        # Pedagogical note: this line is part of the step-by-step program flow.
        return datetime.strptime(data.strip('\n\r'), '%b %d %Y').date()

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def firmware_version(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Returns the firmware version as string'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("NVER", self.OK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.link.read(6)
        # Pedagogical note: this line is part of the step-by-step program flow.
        return data.strip('\n\r')

    # Pedagogical note: this line is part of the step-by-step program flow.
    @cached_property
    # Pedagogical note: this line is part of the step-by-step program flow.
    def diagnostics(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Return the Console Diagnostics report. (RXCHECK command)'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.wake_up()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.send("RXCHECK", self.OK)
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = self.link.read(22).strip('\n\r').split(' ')
        # Pedagogical note: this line is part of the step-by-step program flow.
        data = [int(i) for i in data]
        # Pedagogical note: this line is part of the step-by-step program flow.
        return dict(total_received=data[0], total_missed=data[1],
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    resyn=data[2], max_received=data[3],
                    # Pedagogical note: this line is part of the step-by-step program flow.
                    crc_errors=data[4])

    # Pedagogical note: this line is part of the step-by-step program flow.
    @retry(tries=3, delay=1)
    # Pedagogical note: this line is part of the step-by-step program flow.
    def _read_dump_page(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Read, parse and check a DmpPage.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        raw_dump = self.link.read(267)
        # Pedagogical note: this line is part of the step-by-step program flow.
        if len(raw_dump) != 267:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link.write(self.NACK)
            # Pedagogical note: this line is part of the step-by-step program flow.
            raise BadDataException()
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            dump = DmpPageParser(raw_dump)
            # Pedagogical note: this line is part of the step-by-step program flow.
            if dump.crc_error:
                # Pedagogical note: this line is part of the step-by-step program flow.
                self.link.write(self.NACK)
                # Pedagogical note: this line is part of the step-by-step program flow.
                raise BadCRCException()
            # Pedagogical note: this line is part of the step-by-step program flow.
            return dump
            
    # Pedagogical note: this line is part of the step-by-step program flow.
    def close(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.link.close()
        # Pedagogical note: this line is part of the step-by-step program flow.
        return True

    # Pedagogical note: this line is part of the step-by-step program flow.
    def _recover_broken_pipe(self, error):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Re-open the link when socket write fails with EPIPE.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        if getattr(error, 'errno', None) != errno.EPIPE:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return False
        # Pedagogical note: this line is part of the step-by-step program flow.
        LOGGER.error("Broken pipe detected, reconnecting link")
        # Pedagogical note: this line is part of the step-by-step program flow.
        try:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link.close()
        # Pedagogical note: this line is part of the step-by-step program flow.
        except Exception:
            # Pedagogical note: this line is part of the step-by-step program flow.
            pass
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self._link_factory is not None:
            # Some pylink transports cannot be reliably reused after EPIPE,
            # so rebuild the link object from original connection parameters.
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link = self._link_factory()
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link.open()
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.link.open()
        # Pedagogical note: this line is part of the step-by-step program flow.
        return True

    # Pedagogical note: this line is part of the step-by-step program flow.
    def _is_wake_ack(self, ack):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Return True when wake ACK bytes are valid despite line-ending order.'''
        # Pedagogical note: this line is part of the step-by-step program flow.
        if ack is None:
            # Pedagogical note: this line is part of the step-by-step program flow.
            return False
        # Pedagogical note: this line is part of the step-by-step program flow.
        if is_bytes(ack):
            # Pedagogical note: this line is part of the step-by-step program flow.
            ack = ack.decode('latin1', errors='ignore')
        # Accept expected wake responses and common bridge/proxy variants.
        # Pedagogical note: this line is part of the step-by-step program flow.
        if ack in (self.WAKE_ACK, '\r\n', '\n', '\r', self.ACK):
            # Pedagogical note: this line is part of the step-by-step program flow.
            return True
        # Some links return mixed payloads where newline and ACK bytes are
        # coalesced in one read call (e.g. "\n\x06" or "\rOK").
        # Pedagogical note: this line is part of the step-by-step program flow.
        return ('\n' in ack) or ('\r' in ack)

    # Pedagogical note: this line is part of the step-by-step program flow.
    def _check_revision(self):
        # Pedagogical note: this line is part of the step-by-step program flow.
        '''Check firmware date and get data format revision.'''
        #Rev "A" firmware, dated before April 24, 2002 uses the old format.
        #Rev "B" firmware dated on or after April 24, 2002
        # Pedagogical note: this line is part of the step-by-step program flow.
        date = datetime(2002, 4, 24).date()
        # Pedagogical note: this line is part of the step-by-step program flow.
        self.RevA = self.RevB = True
        # Pedagogical note: this line is part of the step-by-step program flow.
        if self.firmware_date < date:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.RevB = False
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            self.RevA = False
