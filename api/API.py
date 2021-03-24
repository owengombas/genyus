import json
import http.client
import re
import requests
import time

from rauth import OAuth2Service
from bs4 import BeautifulSoup
from datetime import datetime

from Song import Song
from Artist import Artist
from Album import Album

class API:
    def __init__(self):
        self.genius = OAuth2Service(
            client_id="xAP0jvOkLrC3eAjwE4iCeY5BdSrgH7qKUQyh8907-2fGiAGYEHJMNhtFglSLznAq",
            client_secret="WIVq7t1Jq5uaN0OkYCPzhVMr4mt_d-ufoq5fSC6qmyUaxodx5kZ4bS56J87C-LXGRqeeXp9nFpjgrgPtZ_8niA",
            authorize_url="https://api.genius.com/oauth/authorize",
            base_url="https://api.genius.com/"
        )

        self.session = self.genius.get_session(
            token="MMkxdEEuFTGee5lvCdwIOwwIMZNcHozfm1J9LZq4Cy0Ade0_Mn_J4alFHsdAyyix"
        )
    
    def getSong(self, id: int) -> Song:
        res = self.session.get(f"songs/{id}?text_format=plain").json()
        lyricsPageUrl = res['response']['song']['url']
        htmlRes = requests.get(lyricsPageUrl).text

        html = BeautifulSoup(htmlRes, 'html.parser')

        lyricsDiv = html.find("div", class_="lyrics")

        if lyricsDiv != None:
            lyrics = lyricsDiv.get_text()
            lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
            lyrics = lyrics.replace('\n', ' ').strip()
            lyrics = re.sub('\s+', ' ', lyrics)

            album = Album(
                name=res['response']['song']['album']['name'],
                id=res['response']['song']['album']['id']
            )

            artist = Artist(
                name=res['response']['song']['album']['artist']['name'],
                id=res['response']['song']['album']['artist']['id']
            )

            return Song(
                id=res['response']['song']['id'],
                name=res['response']['song']['title'],
                album=album,
                artist=artist,
                lyrics=lyrics,
                image=res['response']['song']['header_image_url'],
                date=datetime.strptime(res['response']['song']['release_date'], "%Y-%m-%d").isoformat()
            )
        else:
            t = 10
            print(f"Waiting {t} secondes")
            time.sleep(t)
            return self.getSong(id)
    
    def search(self, query: str):
        return self.session.get(f"search?q={query}").json()

api = API()

song = api.getSong("3716416")
print(song)

data = api.search("Damso")
print(data)

f = open("data.json", "w")
f.write(song.toJson())
f.close()
