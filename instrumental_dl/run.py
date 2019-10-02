import sys

from .youtube_dl_wrapper.wrapper import YoutubeDL
from .common.file_reader import read_txt_file
from .logger.logger import Logger


def real_main():
    if len(sys.argv) > 1:
        if sys.argv[1][-4:] == '.txt':
            song_names = read_txt_file(sys.argv[1])
        else:
            song_names = sys.argv
            song_names.pop(0)
        logger = Logger(song_names)
        YoutubeDL(logger).download_songs(song_names)
        logger.print_log()
    else:
        print("Error: enter a song name to download")
