from argparse import Namespace
from logging import getLogger
from logging.config import fileConfig
from os.path import join, abspath, dirname, split
from ssl import SSLContext
from sys import version_info, platform

from instrumental_dl.args import get_arguments
from instrumental_dl.file_names import rename_all_files
from instrumental_dl.__version__ import __version__
from instrumental_dl.youtube_dl_wrapper import download_songs


def run(args: Namespace = None):
    _startup_log()
    if not args:
        args = get_arguments()
    ssl_context = SSLContext()
    song_names, file_names, failed_songs = download_songs(ssl_context, args)
    rename_all_files(file_names, args.verbose)


def _startup_log():
    fileConfig(join(join(split(dirname(abspath(__file__)))[0]),
        "config", "logging.conf"))
    logger = getLogger("client")
    logger.debug(f"Instrumental-Downloader(v{__version__}) running on Python {version_info}")
    logger.debug(f"Platform: {platform}")

