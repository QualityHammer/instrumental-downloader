from argparse import Namespace
from re import findall
from ssl import SSLContext
from urllib.parse import urlencode
from urllib.request import urlopen

from instrumental_dl.file_input import read_songs_txt


def get_video_urls(args: Namespace, ssl_context: SSLContext) -> (list, list, list):
    """Using a code snippet by Grant Curell, this gets a list
    of the urls for each of the instrumentals to be downloaded.

    source: https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video"""
    urls = []
    failed_songs = []
    song_names = _songs_from_args(args)
    for song_name in song_names:
        query_string = urlencode({"search_query": f"{song_name} instrumental"})
        html_content = urlopen(f"http://www.youtube.com/results?{query_string}",
                               context=ssl_context)

        results = findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        if len(results) > 0:
            url = f"http://www.youtube.com/watch?v={results[0]}"
            urls.append(url)
        else:
            failed_songs.append(song_name)

    for failed_song in failed_songs:
        song_names.remove(failed_song)

    return song_names, urls, failed_songs


def _songs_from_args(args: Namespace) -> list:
    if args.file != None:
        return read_songs_txt(args.file)
    else:
        return args.songs.copy()
