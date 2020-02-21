from argparse import Namespace
from logging import getLogger
from ssl import SSLContext
from os import chdir, mkdir
from os.path import join, isdir, expanduser
from youtube_dl import YoutubeDL

from instrumental_dl.conversion import get_video_urls


class _YdlLogger(object):
    """A class to log messages from youtube-dl."""

    def __init__(self):
        self.logger = getLogger("youtube_dl")

    def debug(self, msg):
        """Logs a debug message."""
        self.logger.debug(msg)

    def warning(self, msg):
        """Logs a warning message."""
        self.logger.warning(msg)

    def error(self, msg):
        """Logs an error message."""
        self.logger.error(msg)


def download_songs(ssl_context: SSLContext, args: Namespace) -> (list, list, list):
    """Downloads all of the songs in args and converts them to .mp3 files.

    The current directory is moved to the download path. That path
    could be either ~/Music/Instrumentals or a different output directory
    that can be passed using -o in the command line, or having
    the path under args.output if running from python.

    Parameters:
      ssl_context -- contains an ssl certificate used in youtube-dl
      args -- an object that contains all information passed to the program by the user

    Returns:
      A tuple with the following 3 values:
        a list of the names of all the songs that were downloaded
        a list of the file names of all the downloaded songs
        a list of the names of all the songs that failed to download
    """
    file_names = []

    def file_name_hook(download):
        """Adds a song to the log when it's finished downloading.

        Also prints to the console if verbose.
        """
        if download["status"] == "finished":
            file_names.append(download["filename"])
            if args.verbose:
                s_name = song_names[len(file_names) - 1]
                print(f"Downloaded {s_name}.")

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': _YdlLogger(),
        'progress_hooks': [file_name_hook],
        'nocheckcertificate': True,
        'outtmpl': '%(title)s.%(ext)s',
        "quiet": True
    }
    song_names, urls, failed_songs = get_video_urls(args, ssl_context)
    if args.output != None:
         download_path = args.output
    else:
        download_path = _get_download_path()
    chdir(download_path)
    with YoutubeDL(options) as ydl:
        ydl.download(urls)

    return song_names, file_names, failed_songs



def _get_download_path() -> str:
    """Returns the path to the user's default Instrumentals directory.

    Uses ~/Music/Instrumentals as the primary download path.
    If the path doesn't exist, it uses (and creates if needed)
    ~/music/Instrumentals as the download path.

    Returns:
      the path to the Instrumentals folder
    """
    music_path = join(expanduser('~'), 'Music')
    if not isdir(music_path):
        music_path = join(expanduser('~'), 'music')
        if not isdir(music_path):
            mkdir(music_path)

    download_path = join(music_path, 'Instrumentals')
    if not isdir(download_path):
        mkdir(download_path)

    return download_path

