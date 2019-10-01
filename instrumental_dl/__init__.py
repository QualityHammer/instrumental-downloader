import sys, os
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
        'nocheckcertificate': True,
        'outtmpl': '%(title)s.%(ext)s',
    }

    if len(sys.argv) > 1:
        os.chdir(os.getcwd() + '/../output')
        urls = sys.argv
        urls.pop(0)
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download(urls)
    else:
        print("Error: enter a url")


__all__ = ['main']
