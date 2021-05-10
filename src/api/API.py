import re
import requests
import time
import asyncio

from typing import List
from rauth import OAuth2Service
from bs4 import BeautifulSoup, PageElement
from datetime import datetime

from .Song import Song
from .Artist import Artist
from .Album import Album
from .Search import Search


class API:
    def __init__(self):
        self.genius = OAuth2Service(
            client_id="xAP0jvOkLrC3eAjwE4iCeY5BdSrgH7qKUQyh8907-2fGiAGYEHJMNhtFglSLznAq",
            client_secret="WIVq7t1Jq5uaN0OkYCPzhVMr4mt_d-ufoq5fSC6qmyUaxodx5kZ4bS56J87C-LXGRqeeXp9nFpjgrgPtZ_8niA",
            authorize_url="https://api.genius.com/oauth/authorize",
            base_url="https://api.genius.com/"
        )

        self.session = self.genius.get_session(
            token="qfhBonIalyiGK0DcsHmg3-heXf485c1dSV-gOM3ZU4Wn3eD-6-pKjESnhYg4kJ1y"
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

        lyricsDiv: PageElement = html.find("div", class_="lyrics")

        if lyricsDiv == None:
            lyricsDiv = html.find("div", class_="Lyrics__Root-sc-1ynbvzw-0")

        if lyricsDiv != None:
            for br in lyricsDiv.find_all("br"):
                br.replace_with("\n")

            lyrics: str = lyricsDiv.get_text()

            lyrics = lyrics \
                .replace(r'[\(\[].*?[\)\]]', '') \
                .replace('\n', ' ').strip() \
                .replace(r'\s+', ' ')

            time.sleep(wait)

            return lyrics
        elif retry:
            print(f"Cannot scrap lyrics... waiting {wait_retry} secondes")
            time.sleep(wait_retry)
            return self.getLyrics(url, retry, wait_retry, wait)

        return None

    async def getSong(
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

        album: Album = None

        if res['response']['song']['album']:
            album = Album(
                name=res['response']['song']['album']['name'],
                id=res['response']['song']['album']['id']
            )

        artist = Artist(
            name=res['response']['song']['primary_artist']['name'],
            id=res['response']['song']['primary_artist']['id'],
            url=res['response']['song']['primary_artist']['url'],
            image=res['response']['song']['primary_artist']['image_url']
        )

        song = Song(
            id=res['response']['song']['id'],
            name=res['response']['song']['title'],
            album=album,
            artist=artist,
            image=res['response']['song']['header_image_url'],
            url=url,
            lyrics=lyrics,
            date=datetime.strptime(
                res['response']['song']['release_date'] or "1900-01-01", "%Y-%m-%d").isoformat()
        )

        if with_lyrics:
            lyrics = self.getLyrics(url, retry, wait_retry, wait)

        if lyrics != None:
            song.lyrics = lyrics

        return song

    def search(self, query: str) -> List[Search]:
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

    def populateResults(
        self,
        results: List[Search],
        wait: int = 10
    ) -> List[Song]:
        songs: List[Song] = []

        for result in results:
            print(f"Getting:    {result.artist.name} - {result.title}")
            song = self.getSong(result.song_id)
            songs.append(song)

        return songs
