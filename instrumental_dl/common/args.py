import argparse
from platform import system
from os import getcwd

from .path import goto_program, goto_origin
from ..version import __version__


class ArgHandler:
    parser = argparse.ArgumentParser(prog='instrumental_dl', description='A downloader for instrumentals.')
    origin_path = getcwd()

    @staticmethod
    def arg_init():
        """This is called at the start of the program to add arguments."""
        ArgHandler.add_arguments()
        ArgHandler.check_for_input()

    @staticmethod
    def add_arguments():
        """Adds all arguments to the argument parser"""
        arg_ids = ['--f', '--s', '-v']
        arg_help = ArgHandler._get_arg_help(arg_ids)
        ArgHandler.parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
        ArgHandler.parser.add_argument(arg_ids[0], '-File', nargs='?', required=False,
                                       help=arg_help[arg_ids[0]])
        ArgHandler.parser.add_argument(arg_ids[1], '-Songs', metavar='SONGS', nargs='+', required=False,
                                       help=arg_help[arg_ids[1]])
        ArgHandler.parser.add_argument(arg_ids[2], action='store_true', help=arg_help[arg_ids[2]])

    @staticmethod
    def check_for_input():
        """Raises argument error if there is no song/ file specified"""
        args = ArgHandler.parser.parse_args()
        if not args.f and not args.s:
            msg = 'No file name or song names specified.'
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def parse_args():
        """Returns the object with all args passed."""
        return ArgHandler.parser.parse_args()

    @staticmethod
    def get_songs():
        """Returns a list of song names passed as arguments."""
        return ArgHandler.parse_args().s.copy()

    @staticmethod
    def get_songs_txt(file_name: str):
        """
        Opens up the provided text file to retrieve a list of all
        the instrumentals that are going to be downloaded.

        :param file_name: The name of the file that contains
                          a list of all the instrumentals to be downloaded.
        :return: song_names: A list of the names of all of the instrumentals
                             to be downloaded.
        """
        goto_origin(ArgHandler.origin_path)
        with open(file_name, "r") as file:
            song_names = [song.rstrip('\n') for song in file]
        return song_names

    @staticmethod
    def get_filename():
        """Returns the filename passed as an argument."""
        return ArgHandler.parse_args().f

    @staticmethod
    def has_filename():
        """Returns true if a filename has been passed as an argument."""
        if ArgHandler.parse_args().f:
            return True
        return False

    @staticmethod
    def has_songs():
        """Returns true if song names have been passed as arguments."""
        if ArgHandler.parse_args().s:
            return True
        return False

    @staticmethod
    def get_song_names():
        """Returns a list of song names from a list and/ or a file."""

        def _getS(song_names_len):
            if song_names_len == 1:
                return ''
            else:
                return 's'

        song_names = None
        filename = ArgHandler.get_filename()
        if ArgHandler.has_songs() and ArgHandler.has_filename():
            song_names = ArgHandler.get_songs() + ArgHandler.get_songs_txt(filename)
            print(
                f'Downloading and converting {len(song_names)} instrumental{_getS(len(song_names))} '
                "from list and {filename}...")
        elif ArgHandler.has_filename():
            song_names = ArgHandler.get_songs_txt(filename)
            print(
                f"Downloading and converting {len(song_names)} instrumental{_getS(len(song_names))} from {filename}...")
        elif ArgHandler.has_songs():
            song_names = ArgHandler.get_songs()
            print(f"Downloading and converting {len(song_names)} instrumental{_getS(len(song_names))} from list...")

        return song_names

    @staticmethod
    def is_verbose():
        """Returns true if the program is in verbose mode."""
        return ArgHandler.parse_args().v

    @staticmethod
    def _get_arg_help(args):
        """Get a dict of help descriptions for all arguments passed.

        :param: args: A list of arguments that could be passed through.

        :return: arg_help:  A dict with keys of the argument id, and the
                            help description."""
        arg_help = {}
        goto_program()
        if system() == 'Windows':
            arg_file = 'config\\arg_help.txt'
        else:
            arg_file = 'config/arg_help.txt'
        with open(arg_file, 'r') as f:
            for line in f:
                arg_id, help_str = line.split(sep=':')
                if arg_id in args:
                    arg_help[arg_id] = help_str

        return arg_help
