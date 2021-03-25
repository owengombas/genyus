import json
import http.client
import re
import requests
import time

from rauth import OAuth2Service
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List

from Song import Song
from Artist import Artist
from Album import Album
from Search import Search

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
    
    def getLyrics(
        self,
        url: str, 
        retry: bool = False,
        wait_retry: int = 30,
        wait: int = 0
    ) -> str:
        htmlRes = requests.get(url).text

        html = BeautifulSoup(htmlRes, 'html.parser')

        lyricsDiv = html.find("div", class_="lyrics")

        if lyricsDiv != None:
            lyrics: str = lyricsDiv.get_text()

            lyrics = lyrics \
                .replace(r'[\(\[].*?[\)\]]', '') \
                .replace('\n', ' ').strip() \
                .replace(r'\s+', ' ')

            return lyrics
        elif retry:
            print(f"Cannot scrap lyrics... waiting {wait_retry} secondes")
            time.sleep(wait_retry)
            return self.getLyrics(url)
        

        time.sleep(wait)
        
        return None

    
    def getSong(
        self,
        id: int,
        with_lyrics: bool = False,
        retry: bool = False,
        wait_retry: int = 30,
        wait: int = 0
    ) -> Song:
        res = self.session.get(f"songs/{id}?text_format=plain").json()
        url = res['response']['song']['url']
        lyrics = ""

        if with_lyrics:
            lyrics = self.getLyrics(url, retry, wait_retry, wait)
        
        if lyrics != None:
            album = Album(
                name=res['response']['song']['album']['name'],
                id=res['response']['song']['album']['id']
            )

            artist = Artist(
                name=res['response']['song']['album']['artist']['name'],
                id=res['response']['song']['album']['artist']['id'],
                url=res['response']['song']['album']['artist']['url'],
                image=res['response']['song']['album']['artist']['image_url']
            )

            return Song(
                id=res['response']['song']['id'],
                name=res['response']['song']['title'],
                album=album,
                artist=artist,
                lyrics=lyrics,
                image=res['response']['song']['header_image_url'],
                url=url,
                date=datetime.strptime(res['response']['song']['release_date'], "%Y-%m-%d").isoformat()
            )
    
    def search(self, query: str):
        search = self.session.get(f"search?q={query}").json()
        hits = search['response']['hits']
        results: List[Search] = []

        for hit in hits:
            hitResult = hit['result']

            artist = Artist(
                name=hitResult['primary_artist']['name'],
                id=hitResult['primary_artist']['id'],
                image=hitResult['primary_artist']['image_url'],
                url=hitResult['primary_artist']['url']
            )

            search = Search(
                title=hitResult['title'],
                url=hitResult['url'],
                artist=artist,
                song_id=hitResult['id']
            )

            results.append(search)

        return results
    
    def populateResults(self, results: List[Search], wait = 10):
        songs: List[Song] = []

        for result in results:
            print(f"Scraping   {result.artist.name} - {result.title}   lyrics...")
            song = self.getSong(result.song_id)
            songs.append(song)

        return songs

api = API()

# song = api.getSong("3716416")
# print(song)

results = api.search("Damso")
searches = api.populateResults(results)
print(searches)

# f = open("data.json", "w")
# f.write(song.toJson())
# f.close()
