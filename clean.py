import json
from typing import List
import re

from api.Song import Song
from lib.File import File

with open("./datas/songs.json", "r", encoding="utf8") as file:
    songs: List[Song] = json.loads(file.read())

    for song in songs:
        lyrics: str = song["lyrics"]

        lyrics = re.sub(r"\s*\[(.*?)\]\s*", " ", lyrics, flags=re.M | re.I)
        lyrics = re.sub(r"[^a-zA-Z \w ' -]", " ", lyrics, flags=re.M | re.I)
        lyrics = re.sub(r"\w*\d\w*", "", lyrics, flags=re.M | re.I)
        lyrics = re.sub(r"\s{2,}", " ", lyrics, flags=re.M | re.I)

        lyrics_dictionary = re.sub(
            r"\s(j'|l'|t'|c'|qu'|t'|d'|s'|n'|y')\s*", " ", lyrics, flags=re.M | re.I)

        lyrics = lyrics.strip()
        lyrics_dictionary = lyrics_dictionary.strip()

        song["lyrics_dictionary"] = lyrics_dictionary
        song["lyrics"] = lyrics

    File.write_json("./datas/songs_cleaned.json", songs)
