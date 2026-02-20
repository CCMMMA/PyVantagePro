# -*- coding: utf-8 -*-
# Pedagogical note: this line is part of the step-by-step program flow.
'''
    # Pedagogical note: this line is part of the step-by-step program flow.
    pyvantagepro
    # Pedagogical note: this line is part of the step-by-step program flow.
    ------------

    # Pedagogical note: this line is part of the step-by-step program flow.
    The public API and command-line interface to PyVantagePro package.

    # Pedagogical note: this line is part of the step-by-step program flow.
    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    # Pedagogical note: this line is part of the step-by-step program flow.
    :license: GNU GPL v3.

# Pedagogical note: this line is part of the step-by-step program flow.
'''
# Pedagogical note: this line is part of the step-by-step program flow.
import os
# Pedagogical note: this line is part of the step-by-step program flow.
import argparse

# Pedagogical note: this line is part of the step-by-step program flow.
from datetime import datetime

# Make sure the logger is configured early:
# Pedagogical note: this line is part of the step-by-step program flow.
from . import VERSION
# Pedagogical note: this line is part of the step-by-step program flow.
from .logger import active_logger
# Pedagogical note: this line is part of the step-by-step program flow.
from .device import VantagePro2
# Pedagogical note: this line is part of the step-by-step program flow.
from .utils import csv_to_dict
# Pedagogical note: this line is part of the step-by-step program flow.
from .compat import stdout


# Pedagogical note: this line is part of the step-by-step program flow.
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")


# Pedagogical note: this line is part of the step-by-step program flow.
def gettime_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Gettime command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(f"{vp.gettime()} - {vp.timezone}")


# Pedagogical note: this line is part of the step-by-step program flow.
def settime_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Settime command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    old_time = vp.gettime()
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.settime(datetime.strptime(args.datetime, "%Y-%m-%d %H:%M"))
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(f"Old value: {old_time} - {vp.timezone}")
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(f"New value: {vp.gettime()} - {vp.timezone}")


# Pedagogical note: this line is part of the step-by-step program flow.
def getinfo_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Getinfo command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    info = f"Firmware date: {vp.firmware_date}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"Firmware version: {vp.firmware_version}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"Diagnostics: {vp.diagnostics}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(info)

# Pedagogical note: this line is part of the step-by-step program flow.
def getbar_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Displays of the current barometer calibration parameters in text."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    data = vp.getbar()

    # Pedagogical note: this line is part of the step-by-step program flow.
    info = f"Bar. measurement (Hg): {data['bar']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"Elevation (ft): {data['elevation']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"Dew Point (F): {data['dew_point']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"Virtual Temp. (F): {data['virtual_temp']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"C (Humidity correction factor): {data['c']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"R (Humidity correction ratio): {data['r']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"BarCal (Correction ratio): {data['barcal']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"Gain (Calibration values): {data['gain']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    info += f"Offset (Calibration values): {data['offset']}\n"
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(info)

# Pedagogical note: this line is part of the step-by-step program flow.
def getdata_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Get real-time data command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    args.delim = bytes(args.delim, "utf-8").decode("unicode_escape")
    # Pedagogical note: this line is part of the step-by-step program flow.
    data = vp.get_current_data().to_csv(delimiter=args.delim)
    # Pedagogical note: this line is part of the step-by-step program flow.
    args.output.write(data)


# Pedagogical note: this line is part of the step-by-step program flow.
def getarchives(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Getarchive with progress bar if `args.debug` is True."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    from .utils import ListDict
    # Pedagogical note: this line is part of the step-by-step program flow.
    if args.debug:
        # Pedagogical note: this line is part of the step-by-step program flow.
        return vp.get_archives(args.start, args.stop)

    # Pedagogical note: this line is part of the step-by-step program flow.
    from progressbar import ProgressBar, Percentage, Bar
    # Pedagogical note: this line is part of the step-by-step program flow.
    archives = ListDict()
    # Pedagogical note: this line is part of the step-by-step program flow.
    dates = []
    # Pedagogical note: this line is part of the step-by-step program flow.
    generator = vp._get_archives_generator(args.start, args.stop)
    # Pedagogical note: this line is part of the step-by-step program flow.
    widgets = ['Archives download: ', Percentage(), ' ', Bar()]
    # Pedagogical note: this line is part of the step-by-step program flow.
    pbar = ProgressBar(widgets=widgets, maxval=2600).start()
    # Pedagogical note: this line is part of the step-by-step program flow.
    for step, record in enumerate(generator):
        # Pedagogical note: this line is part of the step-by-step program flow.
        pbar.update(step)
        # Pedagogical note: this line is part of the step-by-step program flow.
        if record['Datetime'] not in dates:
            # Pedagogical note: this line is part of the step-by-step program flow.
            archives.append(record)
            # Pedagogical note: this line is part of the step-by-step program flow.
            dates.append(record['Datetime'])
    # Pedagogical note: this line is part of the step-by-step program flow.
    pbar.finish()

    # Pedagogical note: this line is part of the step-by-step program flow.
    if not archives:
        # Pedagogical note: this line is part of the step-by-step program flow.
        print("No new records were found")
    # Pedagogical note: this line is part of the step-by-step program flow.
    elif len(archives) == 1:
        # Pedagogical note: this line is part of the step-by-step program flow.
        print("1 new record was found")
    # Pedagogical note: this line is part of the step-by-step program flow.
    else:
        # Pedagogical note: this line is part of the step-by-step program flow.
        print(f"{len(archives)} new records were found")

    # Pedagogical note: this line is part of the step-by-step program flow.
    return archives.sorted_by('Datetime')


# Pedagogical note: this line is part of the step-by-step program flow.
def getarchives_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Getarchive command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    args.delim = bytes(args.delim, "utf-8").decode("unicode_escape")
    # Pedagogical note: this line is part of the step-by-step program flow.
    if args.start is not None:
        # Pedagogical note: this line is part of the step-by-step program flow.
        args.start = datetime.strptime(args.start, "%Y-%m-%d %H:%M")
    # Pedagogical note: this line is part of the step-by-step program flow.
    if args.stop is not None:
        # Pedagogical note: this line is part of the step-by-step program flow.
        args.stop = datetime.strptime(args.stop, "%Y-%m-%d %H:%M")
    # Pedagogical note: this line is part of the step-by-step program flow.
    args.output.write(getarchives(args, vp).to_csv(delimiter=args.delim))


# Pedagogical note: this line is part of the step-by-step program flow.
def update_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Update command."""
    # Create file if it doesn't exist
    # Pedagogical note: this line is part of the step-by-step program flow.
    open(args.db, 'a').close()  # Equivalent to `touch` in Python 3
    # Pedagogical note: this line is part of the step-by-step program flow.
    with open(args.db, 'r+', newline='') as file_db:
        # Pedagogical note: this line is part of the step-by-step program flow.
        db = csv_to_dict(file_db, delimiter=args.delim)
        # Pedagogical note: this line is part of the step-by-step program flow.
        args.start = None
        # Pedagogical note: this line is part of the step-by-step program flow.
        args.stop = None
        # Pedagogical note: this line is part of the step-by-step program flow.
        if len(db) > 0:
            # Pedagogical note: this line is part of the step-by-step program flow.
            db = db.sorted_by("Datetime", reverse=True)
            # Pedagogical note: this line is part of the step-by-step program flow.
            format = "%Y-%m-%d %H:%M:%S"
            # Pedagogical note: this line is part of the step-by-step program flow.
            start_date = datetime.strptime(db[0]['Datetime'], format)
            # Pedagogical note: this line is part of the step-by-step program flow.
            args.start = start_date
            # Pedagogical note: this line is part of the step-by-step program flow.
            items = getarchives(args, vp)
            # Pedagogical note: this line is part of the step-by-step program flow.
            file_db.write(items.to_csv(delimiter=args.delim, header=False))
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            file_db.write(getarchives(args, vp).to_csv(delimiter=args.delim))


# Pedagogical note: this line is part of the step-by-step program flow.
def get_cmd_parser(cmd, subparsers, help, func):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Make a subparser command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    parser = subparsers.add_parser(cmd, help=help, description=help)
    # Pedagogical note: this line is part of the step-by-step program flow.
    parser.add_argument('--timeout', default=10.0, type=float,
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        help="Connection link timeout")
    # Pedagogical note: this line is part of the step-by-step program flow.
    parser.add_argument('--debug', action="store_true", default=False,
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        help="Display log")
    # Pedagogical note: this line is part of the step-by-step program flow.
    parser.add_argument('url', action="store",
                        # Pedagogical note: this line is part of the step-by-step program flow.
                        help="Specify URL for connection link. "
                             # Pedagogical note: this line is part of the step-by-step program flow.
                             "E.g. tcp:iphost:port "
                             # Pedagogical note: this line is part of the step-by-step program flow.
                             "or serial:/dev/ttyUSB0:19200:8N1")
    # Pedagogical note: this line is part of the step-by-step program flow.
    parser.set_defaults(func=func)
    # Pedagogical note: this line is part of the step-by-step program flow.
    return parser

# Pedagogical note: this line is part of the step-by-step program flow.
def getperiod_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Getperiod command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(f"{vp.getperiod()}")

# Pedagogical note: this line is part of the step-by-step program flow.
def setperiod_cmd(args, vp):
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Setperiod command."""
    # Pedagogical note: this line is part of the step-by-step program flow.
    old_period = vp.getperiod()
    # Pedagogical note: this line is part of the step-by-step program flow.
    vp.setperiod(args.period)
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(f"Old value: {old_period}")
    # Pedagogical note: this line is part of the step-by-step program flow.
    print(f"New value: {args.period}")

# Pedagogical note: this line is part of the step-by-step program flow.
def main():
    # Pedagogical note: this line is part of the step-by-step program flow.
    """Parse command-line arguments and execute VP2 command."""

    # Pedagogical note: this line is part of the step-by-step program flow.
    parser = argparse.ArgumentParser(
        # Pedagogical note: this line is part of the step-by-step program flow.
        prog='pyvantagepro',
        # Pedagogical note: this line is part of the step-by-step program flow.
        description='VantagePro 2 communication tools (New version)'
    # Pedagogical note: this line is part of the step-by-step program flow.
    )
    # Pedagogical note: this line is part of the step-by-step program flow.
    parser.add_argument(
        # Pedagogical note: this line is part of the step-by-step program flow.
        '--version', action='version',
        # Pedagogical note: this line is part of the step-by-step program flow.
        version=f'PyVantagePro version {VERSION}',
        # Pedagogical note: this line is part of the step-by-step program flow.
        help='Print PyVantagePro’s version number and exit.'
    # Pedagogical note: this line is part of the step-by-step program flow.
    )
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparsers = parser.add_subparsers(title='The PyVantagePro commands')

    # gettime command
    # Pedagogical note: this line is part of the step-by-step program flow.
    get_cmd_parser('gettime', subparsers,
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   help='Print the current datetime of the station.',
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   func=gettime_cmd)

    # settime command
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser = get_cmd_parser('settime', subparsers,
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               help='Set the given datetime argument on the station.',
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               func=settime_cmd)
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('datetime', help=f'The chosen datetime value (like: "{NOW}")')

    # getinfo command
    # Pedagogical note: this line is part of the step-by-step program flow.
    get_cmd_parser('getinfo', subparsers,
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   help='Print VantagePro 2 information.',
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   func=getinfo_cmd)

    # getbarcommand
    # Pedagogical note: this line is part of the step-by-step program flow.
    get_cmd_parser('getbar', subparsers,
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   help='Current Barometer calibration parameters',
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   func=getbar_cmd)

    # getarchives command
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser = get_cmd_parser('getarchives', subparsers,
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               help='Extract archives data from the station '
                                    # Pedagogical note: this line is part of the step-by-step program flow.
                                    'between start datetime and stop datetime. '
                                    # Pedagogical note: this line is part of the step-by-step program flow.
                                    'By default the entire contents of the '
                                    # Pedagogical note: this line is part of the step-by-step program flow.
                                    'data archive will be downloaded.',
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               func=getarchives_cmd)
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('--output', action='store', default=stdout,
                           # Pedagogical note: this line is part of the step-by-step program flow.
                           type=argparse.FileType('w'),
                           # Pedagogical note: this line is part of the step-by-step program flow.
                           help='Filename where output is written')
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('--start', help=f'The beginning datetime record (like: "{NOW}")')
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('--stop', help=f'The stopping datetime record (like: "{NOW}")')
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('--delim', action='store', default=",",
                           # Pedagogical note: this line is part of the step-by-step program flow.
                           help='CSV char delimiter')

    # getdata command
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser = get_cmd_parser('getdata', subparsers,
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               help='Extract real-time data from the station.',
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               func=getdata_cmd)
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('--output', action="store", default=stdout,
                           # Pedagogical note: this line is part of the step-by-step program flow.
                           type=argparse.FileType('w'),
                           # Pedagogical note: this line is part of the step-by-step program flow.
                           help='Filename where output is written')
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('--delim', action="store", default=",",
                           # Pedagogical note: this line is part of the step-by-step program flow.
                           help='CSV char delimiter')

    # update command
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser = get_cmd_parser('update', subparsers,
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               help='Update CSV database records by automatically '
                                    # Pedagogical note: this line is part of the step-by-step program flow.
                                    'fetching new archive records.',
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               func=update_cmd)
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('--delim', action="store", default=",",
                           # Pedagogical note: this line is part of the step-by-step program flow.
                           help='CSV char delimiter')
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('db', action="store", help='The CSV file database')

    # getperiod command
    # Pedagogical note: this line is part of the step-by-step program flow.
    get_cmd_parser('getperiod', subparsers,
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   help='Print the current archive period time of the station.',
                   # Pedagogical note: this line is part of the step-by-step program flow.
                   func=getperiod_cmd)

    # setperiod command
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser = get_cmd_parser('setperiod', subparsers,
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               help='Set the given archive time period argument on the station.',
                               # Pedagogical note: this line is part of the step-by-step program flow.
                               func=setperiod_cmd)
    # Pedagogical note: this line is part of the step-by-step program flow.
    subparser.add_argument('period', help='The chosen period value ( Values are 1, 5, 10, 15, 30, 60, and 120)')

    # Parse argv arguments
    # Pedagogical note: this line is part of the step-by-step program flow.
    args = parser.parse_args()

    # Pedagogical note: this line is part of the step-by-step program flow.
    if hasattr(args, 'func'):  # Check if a command function is associated
        # Pedagogical note: this line is part of the step-by-step program flow.
        if getattr(args, 'debug', False):  # Use getattr for optional args
            # Pedagogical note: this line is part of the step-by-step program flow.
            active_logger()
            # Pedagogical note: this line is part of the step-by-step program flow.
            vp = VantagePro2.from_url(args.url, args.timeout)
            # Pedagogical note: this line is part of the step-by-step program flow.
            args.func(args, vp)
        # Pedagogical note: this line is part of the step-by-step program flow.
        else:
            # Pedagogical note: this line is part of the step-by-step program flow.
            try:
                # Pedagogical note: this line is part of the step-by-step program flow.
                vp = VantagePro2.from_url(args.url, args.timeout)
                # Pedagogical note: this line is part of the step-by-step program flow.
                args.func(args, vp)
            # Pedagogical note: this line is part of the step-by-step program flow.
            except Exception as e:
                # Pedagogical note: this line is part of the step-by-step program flow.
                parser.error(f'{e}')
    # Pedagogical note: this line is part of the step-by-step program flow.
    else:
        # Pedagogical note: this line is part of the step-by-step program flow.
        parser.print_help()


# Pedagogical note: this line is part of the step-by-step program flow.
if __name__ == '__main__':
    # Pedagogical note: this line is part of the step-by-step program flow.
    main()
