from argparse import Namespace
from logging import getLogger
from ssl import SSLContext
from os import chdir, mkdir
from os.path import join, isdir, expanduser
from youtube_dl import YoutubeDL

from instrumental_dl.conversion import get_video_urls


class _YdlLogger(object):

    def __init__(self):
        self.logger = getLogger("youtube_dl")

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


def download_songs(ssl_context: SSLContext, args: Namespace) -> (list, list, list):
    file_names = []

    def file_name_hook(download):
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
    """Uses ~/Music/Instrumentals as the primary download path.
    If the path doesn't exist, it uses (and creates if needed)
    ~/music/Instrumentals as the download path.
    Returns
    -------
    download_path: str
        The path to the Instrumentals folder
    """
    # Uses ~/Music as default, but if no music folder exists, ~/music is created and used
    music_path = join(expanduser('~'), 'Music')
    if not isdir(music_path):
        music_path = join(expanduser('~'), 'music')
        if not isdir(music_path):
            mkdir(music_path)

    download_path = join(music_path, 'Instrumentals')
    if not isdir(download_path):
        mkdir(download_path)

    return download_path
