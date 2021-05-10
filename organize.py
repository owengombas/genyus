import pandas as pd
import json
from typing import List
from api import Song, Artist
from lib import File


with open("./datas/songs_cleaned.json", "r", encoding="utf8") as file:
    songs: List[Song] = json.loads(file.read())
    artists: List[Artist] = []

    for song in songs:
        foundArtists = list(
            filter(lambda a: a["id"] == song["artist"]["id"], artists))

        artist = foundArtists[0] if len(foundArtists) > 0 else song["artist"]

        if len(foundArtists) <= 0:
            artists.append(artist)

        if not "songs" in artist:
            artist["songs"] = []

        del song["artist"]

        artist["songs"].append(song)

    File.write_json("./datas/artists.json", artists)
