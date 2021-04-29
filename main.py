import json
from typing import List

from api.API import API
from api.Song import Song

api = API()
songs: List[Song] = []

def writeFile():
    f = open("data.json", "w", encoding="utf8")
    f.write(
        json.dumps(
            songs,
            default=lambda obj: obj.__dict__,
            ensure_ascii=False
        )
    )
    f.close()


with open("songs.txt", "r", encoding="utf8") as file:
    lines = file.read().splitlines()
    for songQuery in lines:
        results = api.search(songQuery)
        if len(results) > 0:
            song = api.getSong(results[0].song_id, True, True, 10, 0)
            songs.append(song)
            print(f"SCRAPED: {song.artist.name} - {song.name}")
            writeFile()
