import argparse
from json import loads
from logging import getLogger
from os.path import dirname, realpath, join, isfile
from sys import exit

from instrumental_dl.__version__ import __version__
from instrumental_dl.exceptions import HelpFileNotFoundException

USAGE_MSG = "Usage: \n" \
            "   instrumental_dl -f FILE_NAME\n" \
            "   instrumental_dl -s 'SONG_NAMES' ['SONG_NAMES'...]\n" \
            "       (with -s the song name needs to be in quotations\n" \
            "        if it contains any spaces)"


def get_arguments():
    long_args = {'-f': "--file", '-s': "--songs", '-v': "--verbose", '-o': "--output"}
    arg_help = _get_argument_help()
    if not arg_help:
        # This will only occur if the help file is not found for whatever reason
        arg_help = {key: "" for key in long_args.keys()}
    parser = argparse.ArgumentParser(prog='instrumental_dl', description='A downloader for instrumentals.')
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-f", long_args["-f"], metavar="FILE", nargs='?', required=False, help=arg_help["-f"])
    parser.add_argument("-s", long_args["-s"], metavar="SONGS", nargs='+', required=False, help=arg_help["-s"])
    parser.add_argument("-o", long_args["-o"], metavar="OUTPUT", help=arg_help["-o"])
    parser.add_argument("-v", long_args["-v"], action="store_true", help=arg_help["-v"])

    args = parser.parse_args()
    if args.file == None and args.songs == None:
        print('\n', USAGE_MSG)
        exit(1)

    return args


def _get_argument_help():
    logger = getLogger("arguments")
    filename = join(dirname(dirname(realpath(__file__))), "config", "arg_help.json")
    if isfile(filename):
        with open(filename, "r") as arg_help:
            return loads(arg_help.read())
    else:
        logger.error(str(HelpFileNotFoundException()))
        return None
