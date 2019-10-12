import sys
import time

from instrumental_dl.youtube_dl_wrapper import YoutubeDL
from .common.io import get_songs_txt
from .logger.logger import Logger
from .errors import MissingArgumentsError


def real_main():
    # Create logger
    logger = Logger()
    if len(sys.argv) > 1:
        start_time = time.time()
        if sys.argv[1][-4:] == '.txt':
            # Downloads all songs from a text file
            print(f"Downloading and converting instrumentals from {sys.argv[1]}...")
            song_names = get_songs_txt(sys.argv[1])
        else:
            # Downloads a list of songs written as arguments
            print("Downloading and converting instrumentals...")
            song_names = sys.argv
            song_names.pop(0)
        # Download songs
        YoutubeDL(logger).download_songs(song_names)
        # Print log
        logger.print_log(time.time() - start_time)
    else:
        raise MissingArgumentsError(logger)
