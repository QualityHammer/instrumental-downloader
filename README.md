# Instrumental-Downloader
A command line tool to download a song's instrumental from Youtube.


# Installation
If you don't have pip, install it here: 
[https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

First, you need to install ffprobe/ ffmpeg: 
[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
  1) Download the build for your OS  
  2) Extract the program folder from the download  
  3) Add the program folder to the system PATH:  
       [Windows](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/)  
       [Mac](https://medium.com/@imstudio/path-macos-best-practice-for-path-environment-variables-on-mac-os-35ec4076a486)  
       [Linux](https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path)  
<p>Then, use pip3 to install:<p>

    pip3 install instrumental-dl

# Description

**Instrumental-downloader** was created as a command-line tool used to download a list of instrumentals based on just the song name.(and sometimes the artist is needed to identify the song) This tool is based off of [youtube-dl](https://github.com/ytdl-org/youtube-dl), a tool used to download youtube videos from their url. The Python interpreter version 3.6+ is needed for this program. FFprobe/ ffmpeg needs to be installed in the PATH, as that is the program used to download instrumentals as mp3 files. 

    instrumental-dl -f FILE_NAME
    instrumental-dl -s "SONG_NAMES" ["SONG_NAMES" ...]
      (with -s the song names need to be in quotations
      so that all the spaces are included)

# Options
    INFO
    ---------------------
    -h, --help              Print the help text and exit
    --version               Print the current version and exit
    
    ONE REQUIRED
    ---------------------
    -f, --file FILE        Open this file and download each song
                            name in the file as an instrumental
                            (each song name should be on a seperate line)
    -s, --songs ["SONGS" ...]
                           Download each song name as an instrumental
                            (can be multiple song names)
    
    OPTIONS
    ---------------------
    -v, --verbose           Verbose: Print out each download and conversion.
                              Also gives detailed time elapsed description.
    -o, --output PATH       Change the directory where the songs are
                              downloaded to.

## TODO

    - Download album cover for song to use as file icon
    - Check for wrong instrumental downloads
    - New file renaming system

    - GUI Application
        - Add gui interaction for Windows, MacOS, and Linux
