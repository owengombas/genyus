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
            r"\s*(j'|l'|t'|c'|qu'|t'|d'|s'|n'|y'|m'|qu'|-)\s*", " ", lyrics, flags=re.M | re.I)
        lyrics_dictionary = re.sub(
            r"'", " ", lyrics_dictionary, flags=re.M | re.I)
        lyrics_dictionary = re.sub(
            r"\s{1,}\w{,1}\s{1,}", "", lyrics_dictionary, flags=re.M | re.I)
        lyrics_dictionary = re.sub(
            r"\s{2,}", " ", lyrics_dictionary, flags=re.M | re.I)

        lyrics = lyrics.strip().lower()
        lyrics_dictionary = lyrics_dictionary.strip().lower()

        song["lyrics_dictionary"] = lyrics_dictionary
        song["lyrics"] = lyrics

    File.write_json("./src/datas/songs.json", songs)
