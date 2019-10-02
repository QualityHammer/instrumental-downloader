import urllib.request
import urllib.parse
import re
import ssl


def get_urls(song_names: list):
    ssl_context = ssl.SSLContext()
    urls = []
    for song_name in song_names:
        query_string = urllib.parse.urlencode({"search_query": song_name + " instrumental"})
        html_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string,
            context=ssl_context
        )
        urls.append("http://www.youtube.com/watch?v=" + re.findall(
            r'href=\"\/watch\?v=(.{11})', html_content.read().decode())[0])

    return urls
