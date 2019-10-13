import argparse


parser = None


def arg_init():
    global parser
    parser = argparse.ArgumentParser(description='A downloader for instrumentals.')
    parser.add_argument('--f', '-File', nargs='?', required=False,
                        help='A file name of a txt file with a list of song names to download.')
    parser.add_argument('--s', '-Songs', metavar='SONGS', nargs='+', required=False,
                        help='A list of song names to download.')
    parser.add_argument('-v', action='store_true', help='Print out detailed information about the download process.')

    args = parser.parse_args()
    if not args.f and not args.s:
        msg = 'No file name or song names specified.'
        raise argparse.ArgumentTypeError(msg)


def parse_args():
    return parser.parse_args()


def get_songs():
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
    return parse_args().f


def has_filename():
    if parse_args().f:
        return True
    return False


def has_songs():
    if parse_args().s:
        return True
    return False


def get_song_names():
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
    return parse_args().v
