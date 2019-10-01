import sys
import youtube_dl


class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def main():
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': Logger(),
        'progress_hooks': [hook],
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=4N1bIfAlBPc'])


__all__ = ['main']
