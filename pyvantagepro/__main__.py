# -*- coding: utf-8 -*-
# Pedagogical note: the next line explains one concrete step in the program flow.
'''
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pyvantagepro
    # Pedagogical note: the next line explains one concrete step in the program flow.
    ------------

    # Pedagogical note: the next line explains one concrete step in the program flow.
    The public API and command-line interface to PyVantagePro package.

    # Pedagogical note: the next line explains one concrete step in the program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: the next line explains one concrete step in the program flow.
    :license: GNU GPL v3.

# Pedagogical note: the next line explains one concrete step in the program flow.
'''
# Pedagogical note: the next line explains one concrete step in the program flow.
import os
# Pedagogical note: the next line explains one concrete step in the program flow.
import argparse

# Pedagogical note: the next line explains one concrete step in the program flow.
from datetime import datetime

# Make sure the logger is configured early:
# Pedagogical note: the next line explains one concrete step in the program flow.
from . import VERSION
# Pedagogical note: the next line explains one concrete step in the program flow.
from .logger import active_logger
# Pedagogical note: the next line explains one concrete step in the program flow.
from .device import VantagePro2
# Pedagogical note: the next line explains one concrete step in the program flow.
from .utils import csv_to_dict
# Pedagogical note: the next line explains one concrete step in the program flow.
from .compat import stdout


# Pedagogical note: the next line explains one concrete step in the program flow.
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")


# Pedagogical note: the next line explains one concrete step in the program flow.
def gettime_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Gettime command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(f"{vp.gettime()} - {vp.timezone}")


# Pedagogical note: the next line explains one concrete step in the program flow.
def settime_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Settime command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    old_time = vp.gettime()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    vp.settime(datetime.strptime(args.datetime, "%Y-%m-%d %H:%M"))
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(f"Old value: {old_time} - {vp.timezone}")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(f"New value: {vp.gettime()} - {vp.timezone}")


# Pedagogical note: the next line explains one concrete step in the program flow.
def getinfo_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Getinfo command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info = f"Firmware date: {vp.firmware_date}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"Firmware version: {vp.firmware_version}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"Diagnostics: {vp.diagnostics}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(info)

# Pedagogical note: the next line explains one concrete step in the program flow.
def getbar_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Displays of the current barometer calibration parameters in text."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    data = vp.getbar()

    # Pedagogical note: the next line explains one concrete step in the program flow.
    info = f"Bar. measurement (Hg): {data['bar']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"Elevation (ft): {data['elevation']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"Dew Point (F): {data['dew_point']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"Virtual Temp. (F): {data['virtual_temp']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"C (Humidity correction factor): {data['c']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"R (Humidity correction ratio): {data['r']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"BarCal (Correction ratio): {data['barcal']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"Gain (Calibration values): {data['gain']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    info += f"Offset (Calibration values): {data['offset']}\n"
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(info)

# Pedagogical note: the next line explains one concrete step in the program flow.
def getdata_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Get real-time data command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    args.delim = bytes(args.delim, "utf-8").decode("unicode_escape")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    data = vp.get_current_data().to_csv(delimiter=args.delim)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    args.output.write(data)


# Pedagogical note: the next line explains one concrete step in the program flow.
def getarchives(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Getarchive with progress bar if `args.debug` is True."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    from .utils import ListDict
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if args.debug:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        return vp.get_archives(args.start, args.stop)

    # Pedagogical note: the next line explains one concrete step in the program flow.
    from progressbar import ProgressBar, Percentage, Bar
    # Pedagogical note: the next line explains one concrete step in the program flow.
    archives = ListDict()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    dates = []
    # Pedagogical note: the next line explains one concrete step in the program flow.
    generator = vp._get_archives_generator(args.start, args.stop)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    widgets = ['Archives download: ', Percentage(), ' ', Bar()]
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pbar = ProgressBar(widgets=widgets, maxval=2600).start()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    for step, record in enumerate(generator):
        # Pedagogical note: the next line explains one concrete step in the program flow.
        pbar.update(step)
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if record['Datetime'] not in dates:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            archives.append(record)
            # Pedagogical note: the next line explains one concrete step in the program flow.
            dates.append(record['Datetime'])
    # Pedagogical note: the next line explains one concrete step in the program flow.
    pbar.finish()

    # Pedagogical note: the next line explains one concrete step in the program flow.
    if not archives:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        print("No new records were found")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    elif len(archives) == 1:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        print("1 new record was found")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    else:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        print(f"{len(archives)} new records were found")

    # Pedagogical note: the next line explains one concrete step in the program flow.
    return archives.sorted_by('Datetime')


# Pedagogical note: the next line explains one concrete step in the program flow.
def getarchives_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Getarchive command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    args.delim = bytes(args.delim, "utf-8").decode("unicode_escape")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if args.start is not None:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        args.start = datetime.strptime(args.start, "%Y-%m-%d %H:%M")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    if args.stop is not None:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        args.stop = datetime.strptime(args.stop, "%Y-%m-%d %H:%M")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    args.output.write(getarchives(args, vp).to_csv(delimiter=args.delim))


# Pedagogical note: the next line explains one concrete step in the program flow.
def update_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Update command."""
    # Create file if it doesn't exist
    # Pedagogical note: the next line explains one concrete step in the program flow.
    open(args.db, 'a').close()  # Equivalent to `touch` in Python 3
    # Pedagogical note: the next line explains one concrete step in the program flow.
    with open(args.db, 'r+', newline='') as file_db:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        db = csv_to_dict(file_db, delimiter=args.delim)
        # Pedagogical note: the next line explains one concrete step in the program flow.
        args.start = None
        # Pedagogical note: the next line explains one concrete step in the program flow.
        args.stop = None
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if len(db) > 0:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            db = db.sorted_by("Datetime", reverse=True)
            # Pedagogical note: the next line explains one concrete step in the program flow.
            format = "%Y-%m-%d %H:%M:%S"
            # Pedagogical note: the next line explains one concrete step in the program flow.
            start_date = datetime.strptime(db[0]['Datetime'], format)
            # Pedagogical note: the next line explains one concrete step in the program flow.
            args.start = start_date
            # Pedagogical note: the next line explains one concrete step in the program flow.
            items = getarchives(args, vp)
            # Pedagogical note: the next line explains one concrete step in the program flow.
            file_db.write(items.to_csv(delimiter=args.delim, header=False))
        # Pedagogical note: the next line explains one concrete step in the program flow.
        else:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            file_db.write(getarchives(args, vp).to_csv(delimiter=args.delim))


# Pedagogical note: the next line explains one concrete step in the program flow.
def get_cmd_parser(cmd, subparsers, help, func):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Make a subparser command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    parser = subparsers.add_parser(cmd, help=help, description=help)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    parser.add_argument('--timeout', default=10.0, type=float,
                        # Pedagogical note: the next line explains one concrete step in the program flow.
                        help="Connection link timeout")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    parser.add_argument('--debug', action="store_true", default=False,
                        # Pedagogical note: the next line explains one concrete step in the program flow.
                        help="Display log")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    parser.add_argument('url', action="store",
                        # Pedagogical note: the next line explains one concrete step in the program flow.
                        help="Specify URL for connection link. "
                             # Pedagogical note: the next line explains one concrete step in the program flow.
                             "E.g. tcp:iphost:port "
                             # Pedagogical note: the next line explains one concrete step in the program flow.
                             "or serial:/dev/ttyUSB0:19200:8N1")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    parser.set_defaults(func=func)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    return parser

# Pedagogical note: the next line explains one concrete step in the program flow.
def getperiod_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Getperiod command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(f"{vp.getperiod()}")

# Pedagogical note: the next line explains one concrete step in the program flow.
def setperiod_cmd(args, vp):
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Setperiod command."""
    # Pedagogical note: the next line explains one concrete step in the program flow.
    old_period = vp.getperiod()
    # Pedagogical note: the next line explains one concrete step in the program flow.
    vp.setperiod(args.period)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(f"Old value: {old_period}")
    # Pedagogical note: the next line explains one concrete step in the program flow.
    print(f"New value: {args.period}")

# Pedagogical note: the next line explains one concrete step in the program flow.
def main():
    # Pedagogical note: the next line explains one concrete step in the program flow.
    """Parse command-line arguments and execute VP2 command."""

    # Pedagogical note: the next line explains one concrete step in the program flow.
    parser = argparse.ArgumentParser(
        # Pedagogical note: the next line explains one concrete step in the program flow.
        prog='pyvantagepro',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        description='VantagePro 2 communication tools (New version)'
    # Pedagogical note: the next line explains one concrete step in the program flow.
    )
    # Pedagogical note: the next line explains one concrete step in the program flow.
    parser.add_argument(
        # Pedagogical note: the next line explains one concrete step in the program flow.
        '--version', action='version',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        version=f'PyVantagePro version {VERSION}',
        # Pedagogical note: the next line explains one concrete step in the program flow.
        help='Print PyVantagePro’s version number and exit.'
    # Pedagogical note: the next line explains one concrete step in the program flow.
    )
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparsers = parser.add_subparsers(title='The PyVantagePro commands')

    # gettime command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    get_cmd_parser('gettime', subparsers,
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   help='Print the current datetime of the station.',
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   func=gettime_cmd)

    # settime command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser = get_cmd_parser('settime', subparsers,
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               help='Set the given datetime argument on the station.',
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               func=settime_cmd)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('datetime', help=f'The chosen datetime value (like: "{NOW}")')

    # getinfo command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    get_cmd_parser('getinfo', subparsers,
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   help='Print VantagePro 2 information.',
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   func=getinfo_cmd)

    # getbarcommand
    # Pedagogical note: the next line explains one concrete step in the program flow.
    get_cmd_parser('getbar', subparsers,
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   help='Current Barometer calibration parameters',
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   func=getbar_cmd)

    # getarchives command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser = get_cmd_parser('getarchives', subparsers,
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               help='Extract archives data from the station '
                                    # Pedagogical note: the next line explains one concrete step in the program flow.
                                    'between start datetime and stop datetime. '
                                    # Pedagogical note: the next line explains one concrete step in the program flow.
                                    'By default the entire contents of the '
                                    # Pedagogical note: the next line explains one concrete step in the program flow.
                                    'data archive will be downloaded.',
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               func=getarchives_cmd)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('--output', action='store', default=stdout,
                           # Pedagogical note: the next line explains one concrete step in the program flow.
                           type=argparse.FileType('w'),
                           # Pedagogical note: the next line explains one concrete step in the program flow.
                           help='Filename where output is written')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('--start', help=f'The beginning datetime record (like: "{NOW}")')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('--stop', help=f'The stopping datetime record (like: "{NOW}")')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('--delim', action='store', default=",",
                           # Pedagogical note: the next line explains one concrete step in the program flow.
                           help='CSV char delimiter')

    # getdata command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser = get_cmd_parser('getdata', subparsers,
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               help='Extract real-time data from the station.',
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               func=getdata_cmd)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('--output', action="store", default=stdout,
                           # Pedagogical note: the next line explains one concrete step in the program flow.
                           type=argparse.FileType('w'),
                           # Pedagogical note: the next line explains one concrete step in the program flow.
                           help='Filename where output is written')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('--delim', action="store", default=",",
                           # Pedagogical note: the next line explains one concrete step in the program flow.
                           help='CSV char delimiter')

    # update command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser = get_cmd_parser('update', subparsers,
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               help='Update CSV database records by automatically '
                                    # Pedagogical note: the next line explains one concrete step in the program flow.
                                    'fetching new archive records.',
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               func=update_cmd)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('--delim', action="store", default=",",
                           # Pedagogical note: the next line explains one concrete step in the program flow.
                           help='CSV char delimiter')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('db', action="store", help='The CSV file database')

    # getperiod command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    get_cmd_parser('getperiod', subparsers,
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   help='Print the current archive period time of the station.',
                   # Pedagogical note: the next line explains one concrete step in the program flow.
                   func=getperiod_cmd)

    # setperiod command
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser = get_cmd_parser('setperiod', subparsers,
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               help='Set the given archive time period argument on the station.',
                               # Pedagogical note: the next line explains one concrete step in the program flow.
                               func=setperiod_cmd)
    # Pedagogical note: the next line explains one concrete step in the program flow.
    subparser.add_argument('period', help='The chosen period value ( Values are 1, 5, 10, 15, 30, 60, and 120)')

    # Parse argv arguments
    # Pedagogical note: the next line explains one concrete step in the program flow.
    args = parser.parse_args()

    # Pedagogical note: the next line explains one concrete step in the program flow.
    if hasattr(args, 'func'):  # Check if a command function is associated
        # Pedagogical note: the next line explains one concrete step in the program flow.
        if getattr(args, 'debug', False):  # Use getattr for optional args
            # Pedagogical note: the next line explains one concrete step in the program flow.
            active_logger()
            # Pedagogical note: the next line explains one concrete step in the program flow.
            vp = VantagePro2.from_url(args.url, args.timeout)
            # Pedagogical note: the next line explains one concrete step in the program flow.
            args.func(args, vp)
        # Pedagogical note: the next line explains one concrete step in the program flow.
        else:
            # Pedagogical note: the next line explains one concrete step in the program flow.
            try:
                # Pedagogical note: the next line explains one concrete step in the program flow.
                vp = VantagePro2.from_url(args.url, args.timeout)
                # Pedagogical note: the next line explains one concrete step in the program flow.
                args.func(args, vp)
            # Pedagogical note: the next line explains one concrete step in the program flow.
            except Exception as e:
                # Pedagogical note: the next line explains one concrete step in the program flow.
                parser.error(f'{e}')
    # Pedagogical note: the next line explains one concrete step in the program flow.
    else:
        # Pedagogical note: the next line explains one concrete step in the program flow.
        parser.print_help()


# Pedagogical note: the next line explains one concrete step in the program flow.
if __name__ == '__main__':
    # Pedagogical note: the next line explains one concrete step in the program flow.
    main()
