import json

from typing import List

from api.API import API
from api.Song import Song
from lib.File import File

api = API()

songs_input: List[str] = []
songs_json: List[Song] = []

with open("./src/datas/songs.txt", "r", encoding="utf8") as file:
    lines = file.read().splitlines()

    for line in lines:
        existing = list(filter(lambda x: x == line, lines))
        if len(existing) < 2:
            songs_input.append(line)

    f = open("./src/datas/songs.txt", "w", encoding="utf8")
    f.write("\n".join(songs_input))
    f.close()

with open("./src/datas/songs.json", "r", encoding="utf8") as file:
    songs: List[Song] = json.loads(file.read())

    for song in songs:
        existing = list(filter(lambda x: x["name"] == song["name"], songs))
        if len(existing) < 2:
            songs_json.append(song)

    File.write_json("./src/datas/songs.json", songs_json)
