import os
import youtube_dl

from instrumental_dl.url_query.query import get_urls


class Logger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def hook(download):
    if download['status'] == 'finished':
        print(download['filename'], 'finished downloading in', download['elapsed'], 'seconds')


class YoutubeDL:

    def __init__(self):
        self.options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': Logger(),
            'progress_hooks': [hook],
            'nocheckcertificate': True,
            'outtmpl': '%(title)s.%(ext)s',
        }
        self.change_output()

    @staticmethod
    def change_output():
        os.chdir(os.getcwd() + '/../output')

    def download_songs(self, song_names):
        urls = get_urls(song_names)
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download(urls)
