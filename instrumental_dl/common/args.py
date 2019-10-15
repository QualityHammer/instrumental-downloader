import argparse
from platform import system

from .path import goto_program
from ..version import __version__


parser = None


def arg_init():
    """This is called at the start of the program to add arguments."""
    global parser
    parser = argparse.ArgumentParser(prog='instrumental_dl', description='A downloader for instrumentals.')
    arg_ids = ['--f', '--s', '-v']
    arg_help = _get_arg_help(arg_ids)

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument(arg_ids[0], '-File', nargs='?', required=False,
                        help=arg_help[arg_ids[0]])
    parser.add_argument(arg_ids[1], '-Songs', metavar='SONGS', nargs='+', required=False,
                        help=arg_help[arg_ids[1]])
    parser.add_argument(arg_ids[2], action='store_true', help=arg_help[arg_ids[2]])

    # Raises argument error if there is no song/ file specified
    args = parser.parse_args()
    if not args.f and not args.s:
        msg = 'No file name or song names specified.'
        raise argparse.ArgumentTypeError(msg)


def parse_args():
    """Returns the object with all args passed."""
    return parser.parse_args()


def get_songs():
    """Returns a list of song names passed as arguments."""
    return parse_args().s.copy()


def get_songs_txt(file_name: str):
    """
    Opens up the provided text file to retrieve a list of all
    the instrumentals that are going to be downloaded.

    :param file_name: The name of the file that contains
                      a list of all the instrumentals to be downloaded.
    :return: song_names: A list of the names of all of the instrumentals
                         to be downloaded.
    """
    with open(file_name, "r") as file:
        song_names = [song.rstrip('\n') for song in file]
    return song_names


def get_filename():
    """Returns the filename passed as an argument."""
    return parse_args().f


def has_filename():
    """Returns true if a filename has been passed as an argument."""
    if parse_args().f:
        return True
    return False


def has_songs():
    """Returns true if song names have been passed as arguments."""
    if parse_args().s:
        return True
    return False


def get_song_names():
    """Returns a list of song names from a list and/ or a file."""
    song_names = None
    filename = get_filename()
    if has_songs() and has_filename():
        song_names = get_songs() + get_songs_txt(filename)
        print(f'Downloading and converting {len(song_names)} instrumentals from list and {filename}...')
    elif has_filename():
        song_names = get_songs_txt(filename)
        print(f"Downloading and converting {len(song_names)} instrumentals from {filename}...")
    elif has_songs():
        song_names = get_songs()
        print(f"Downloading and converting {len(song_names)} instrumentals from list...")

    return song_names


def is_verbose():
    """Returns true if the program is in verbose mode."""
    return parse_args().v


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
