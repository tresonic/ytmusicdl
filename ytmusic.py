#!/usr/bin/env python3

import sys, os
import eyed3
import yt_dlp
from ytmusicapi import YTMusic

ytmusic = YTMusic()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

def build_filename(artists, title):
    artists_str = artists[0]
    for a in range(len(artists) - 1):
        artists_str += ", " + artists[a + 1]
    filename = artists_str + " - " + title
    filename = filename.replace("/", " ")
    filename = filename.replace("?", "")
    return (filename, artists_str)

def download_track(track):
    artists = [t["name"] for t in track["artists"]]
    title = track["title"]

    filename, artists_str = build_filename(artists, title)

    ydl_opts["outtmpl"] = filename
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download("https://www.youtube.com/watch?v=" + track["videoId"])
    
    file = eyed3.load(filename + ".mp3")
    file.initTag()
    file.tag.artist = artists_str
    file.tag.title = title
    if track["album"]:
        file.tag.album = track["album"]["name"]
    file.tag.save()

def get_playlist(id):
    ret = ytmusic.get_playlist(id, None)
    filenames = os.listdir()

    for track in ret["tracks"]:
        artists = [t["name"] for t in track["artists"]]
        title = track["title"]
        f = build_filename(artists, title)[0] + ".mp3"
        if f in filenames:
            print(f"Skipping {f}")
            continue
        print(f"{f}")
        download_track(track)

def main():
    print("ytmusic - dl_test")
    url = sys.argv[1]
    print(url)
    if "list" in url:
        print("playlist mode")
        id = url.split('=')[-1]
        print(f"playlist id: {id}")
        get_playlist(id)


if __name__ == '__main__':
    main()
