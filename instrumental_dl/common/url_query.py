from ssl import SSLContext
import urllib.request
import urllib.parse
import re


def get_video_urls(song_names: list, ssl_context: SSLContext):
    """Using a code snippet by Grant Curell, this gets a list
    of the urls for each of the instrumentals to be downloaded.

    source: https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video

    Parameters
    ----------
    song_names: list of str
        A list of song names to be searched for.
    ssl_context: SSLContext
        The SSL Context used for urls.

    Returns
    -------
    urls: list of str
        A list of the urls for all the instrumentals to be downloaded
    failed_songs: list of str
        A list of the names of instrumentals that failed downloading for any reason
    song_names: list of str
        A list of the names of all the instrumentals that successfully downloaded
    """
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

    for failed_song in failed_songs:
        song_names.remove(failed_song)

    return urls, failed_songs, song_names
