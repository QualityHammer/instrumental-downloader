import argparse
from json import loads
from os.path import dirname, realpath, join, isfile

from instrumental_dl import __version__


def get_arguments():
    long_args = {'-f': "--file", '-s': "--songs", '-v': "--verbose", '-o': "--output"}
    arg_help = _get_argument_help()
    parser = argparse.ArgumentParser(prog='instrumental_dl', description='A downloader for instrumentals.')
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-f", long_args["-f"], metavar="FILE", nargs='?', required=False, help=arg_help["-f"])
    parser.add_argument("-s", long_args["-s"], metavar="SONGS", nargs='+', required=False, help=arg_help["-s"])
    parser.add_argument("-o", long_args["-o"], metavar="OUTPUT", help=arg_help["-o"])
    parser.add_argument("-v", long_args["-v"], action="store_true", help=arg_help["-v"])

    args = parser.parse_args()
    if not hasattr(args, 'f') and not hasattr(args, 's'):
        # TODO: Add usage message
        print("Usage: ")

    return args


def _get_argument_help():
    filename = join(dirname(realpath(__file__)), "config", "arg_help.json")
    if isfile(filename):
        with open(filename, "r") as arg_help:
            return loads(arg_help.read())
    else:
        # TODO: Add config exception
        print("Error: config file not found")
        return None
