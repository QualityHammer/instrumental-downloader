from argparse import Namespace
from ssl import SSLContext

from .args import get_arguments
from .file_names import rename_all_files
from .youtube_dl_wrapper import download_songs


def run(args: Namespace = None):
    if not args:
        args = get_arguments()
    ssl_context = SSLContext()
    song_names, file_names, failed_songs = download_songs(ssl_context, args)
    rename_all_files(file_names, args.v if hasattr(args, 'v') else False)
