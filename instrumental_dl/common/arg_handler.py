import argparse
from platform import system
from os import getcwd

from .path import goto_program, goto_origin
from ..version import __version__


class ArgHandler:
    """ArgHandler is used to parse arguments when using the CLI.

    Attributes
    ----------
    parser: ArgumentParser
        argparse is used as a parser to parse the arguments that a user inputs into the command line
    origin_path: str
        The path to the folder that the user called this command in

    Methods
    -------
    arg_init()
        This is called at the start of the program to add arguments.
    get_song_names()
        Returns a list of song names from a list and/ or a file.
    is_verbose()
        Returns true if the program is in verbose mode.
    """
    parser = argparse.ArgumentParser(prog='instrumental_dl', description='A downloader for instrumentals.')
    origin_path = getcwd()

    @staticmethod
    def arg_init():
        """This is called at the start of the program to add arguments."""
        ArgHandler._add_arguments()
        ArgHandler._check_for_input()

    @staticmethod
    def get_song_names():
        """Returns a list of song names from a list and/ or a file.

        Returns
        -------
        song_names: list of str
            A list of the total song names inputted
        """

        def _getS(song_names_len):
            if song_names_len == 1:
                return ''
            else:
                return 's'

        song_names = None
        filename = ArgHandler._get_filename()
        if ArgHandler._has_songs() and ArgHandler._has_filename():
            song_names = ArgHandler._get_songs() + ArgHandler._get_songs_txt(filename)
            print(
                f'Downloading and converting {len(song_names)} instrumental{_getS(len(song_names))} '
                "from list and {filename}...")
        elif ArgHandler._has_filename():
            song_names = ArgHandler._get_songs_txt(filename)
            print(
                f"Downloading and converting {len(song_names)} instrumental{_getS(len(song_names))} from {filename}...")
        elif ArgHandler._has_songs():
            song_names = ArgHandler._get_songs()
            print(f"Downloading and converting {len(song_names)} instrumental{_getS(len(song_names))} from list...")

        return song_names

    @staticmethod
    def is_verbose():
        """Returns true if the program is in verbose mode."""
        return ArgHandler._parse_args().v

    @staticmethod
    def _add_arguments():
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
    def _check_for_input():
        """Raises argument error if there is no song/ file specified.

        Raises
        ------
        ArgumentTypeError if no file or song name is specified
        """
        args = ArgHandler.parser.parse_args()
        if not args.f and not args.s:
            msg = 'No file name or song names specified.'
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def _get_arg_help(args: list):
        """Get a dict of help descriptions for all arguments passed.

        Parameter
        ---------
        args: list of str
            A list of arguments that could be passed through.

        Returns
        -------
        arg_help: dict
            A dict with keys of the argument id, and the help description.
        """
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

    @staticmethod
    def _get_filename():
        """Returns the filename passed as an argument.

        Returns
        -------
        str
            The filename that was passed as an argument if there is one
        """
        return ArgHandler._parse_args().f

    @staticmethod
    def _get_songs():
        """Returns a list of song names passed as arguments.

        Returns
        -------
        list of str
            A list of all the song names that were passed as command line arguments
        """
        return ArgHandler._parse_args().s.copy()

    @staticmethod
    def _get_songs_txt(file_name: str):
        """
        Opens up the provided text file to retrieve a list of all
        the instrumentals that are going to be downloaded.

        Parameter
        ---------
        file_name: str
            The name of the file that contains a list of all the instrumentals to be downloaded.

        Returns
        -------
        song_names: list of str
            A list of the names of all of the instrumentals to be downloaded.
        """
        goto_origin(ArgHandler.origin_path)
        with open(file_name, "r") as file:
            song_names = [song.rstrip('\n') for song in file]
        return song_names

    @staticmethod
    def _has_filename():
        """Returns true if a filename has been passed as an argument."""
        if ArgHandler._parse_args().f:
            return True
        return False

    @staticmethod
    def _has_songs():
        """Returns true if song names have been passed as arguments."""
        if ArgHandler._parse_args().s:
            return True
        return False

    @staticmethod
    def _parse_args():
        """Returns the object with all args passed."""
        return ArgHandler.parser.parse_args()
