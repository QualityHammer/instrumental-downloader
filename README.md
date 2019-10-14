# Instrumental-Downloader
A command line tool to download a song's instrumental from Youtube.


# Installation

First, you need to install [ffprobe/ ffmpeg](https://ffmpeg.org/download.html).<br>
Then, use pip3 to install:

    pip3 install instrumental_dl

# Description

**Instrumental_dl** was created as a command-line tool used to download a list of instrumentals based on just the song name.(and sometimes the artist is needed to identify the song) This tool is based off of [youtube_dl](https://github.com/ytdl-org/youtube-dl), a tool used to download youtube videos from their url. The Python interpreter version 3.6+ is needed for this program. FFprobe/ ffmpeg needs to be installed in the PATH, as that is the program used to download instrumentals as mp3 files. 

    instrumental_dl --f FILE_NAME
    instrumental_dl --s "SONG_NAMES" ["SONG_NAMES"]
      (with --s the song name needs to be in quotations
      if it contains any spaces)

# Options
    -h, --help              Print this help text and exit
    
    ONE REQUIRED
    ---------------------
    --f, -File              Open this file and download each song
                            name in the file as an instrumental
                            (each song name should be on a seperate line)
    --s, -Songs             Download each song name as an instrumental
                            (can be multiple song names)
    
    OPTIONS
    ---------------------
    -v                      Verbose: Print out each download and conversion.
                            Also gives detailed time elapsed description.
