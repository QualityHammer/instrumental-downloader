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
    """Runs the instrumental-downloader program.

    If running from the command line, arguments can
    be passed to tell the program what to do.

    If running directly from python, args can
    be passed through this function as a parameter.
    It should have all of the attributes needed to
    run this program.
    """
    _startup_log()
    if not args:
        args = get_arguments()
    ssl_context = SSLContext()
    song_names, file_names, failed_songs = download_songs(ssl_context, args)
    rename_all_files(file_names, args.verbose)


def _startup_log():
    """Initializes the log for this program."""
    fileConfig(join(split(dirname(abspath(__file__)))[0],
        "config", "logging.conf"))
    logger = getLogger("client")
    logger.debug(f"Instrumental-Downloader(v{__version__}) running on Python {version_info}")
    logger.debug(f"Platform: {platform}")

