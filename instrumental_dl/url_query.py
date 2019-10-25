import urllib.request
import urllib.parse
import re
import ssl


def get_urls(logger, song_names: list):
    """Using a code snippet by Grant Curell, this gets a list
    of the urls for each of the instrumentals to be downloaded.

    source: https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video

    :param: song_names: A list of song names to be searched for.
    :return: urls: A list of the urls for all the instrumentals to be downloaded
    """
    ssl_context = ssl.SSLContext()
    urls = []
    failed_songs = []
    for song_name in song_names:
        query_string = urllib.parse.urlencode({"search_query": song_name + " instrumental"})
        html_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string,
            context=ssl_context
        )

        try:
            url = "http://www.youtube.com/watch?v=" + \
                  re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())[0]
            urls.append(url)
        except IndexError:
            failed_songs.append(song_name)
            song_names.remove(song_name)

    return urls, failed_songs, song_names
