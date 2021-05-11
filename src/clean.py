import json
import re

from typing import List

from api.Song import Song
from lib.File import File

with open("./src/datas/songs.json", "r", encoding="utf8") as file:
    songs: List[Song] = json.loads(file.read())

    cleaned_songs: List[Song] = []

    for song in songs:
        lyrics: str = song["lyrics"]

        # Remove all the undesired chars
        lyrics = re.sub(r"\s*\[(.*?)\]\s*", " ", lyrics, flags=re.M | re.I)
        lyrics = re.sub(r"[^a-zA-Z \w ' -]", " ", lyrics, flags=re.M | re.I)
        lyrics = re.sub(r"\w*\d\w*", "", lyrics, flags=re.M | re.I)
        lyrics = re.sub(r"\s{2,}", " ", lyrics, flags=re.M | re.I)

        # Create a field that aims to be compared to a french dictionary
        lyrics_dictionary = re.sub(
            r"\s(j'|l'|t'|c'|qu'|t'|d'|s'|n'|y')\s*", " ", lyrics, flags=re.M | re.I)

        lyrics = lyrics.strip()
        lyrics_dictionary = lyrics_dictionary.strip()

        song["lyrics_dictionary"] = lyrics_dictionary
        song["lyrics"] = lyrics

    File.write_json("./src/datas/songs.json", songs)
