import time

from .youtube_dl_wrapper import YoutubeDL
from .common.args import arg_init, get_song_names
from .logger.logger import Logger


def real_main():
    arg_init()
    logger = Logger()
    start_time = time.time()
    song_names = get_song_names()
    # Download songs
    YoutubeDL(logger).download_songs(song_names)
    # Print log
    logger.print_log(time.time() - start_time)
