import sys
import time

from instrumental_dl.youtube_dl_wrapper import YoutubeDL
from .common.io import read_txt_file
from .logger.logger import Logger


def real_main():
    if len(sys.argv) > 1:
        start_time = time.time()
        if sys.argv[1][-4:] == '.txt':
            print("Downloading and converting songs from " + sys.argv[1] + "...")
            song_names = read_txt_file(sys.argv[1])
        else:
            print("Downloading and converting songs...")
            song_names = sys.argv
            song_names.pop(0)
        logger = Logger(song_names)
        YoutubeDL(logger).download_songs(song_names)
        logger.print_log(time.time() - start_time)
    else:
        print("Error: enter either a .txt filename or "
              "song names to download")
