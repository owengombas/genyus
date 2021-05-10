import re
import requests
import time

from typing import List
from rauth import OAuth2Service
from bs4 import BeautifulSoup, PageElement
from datetime import datetime

from .Song import Song
from .Artist import Artist
from .Album import Album
from .Search import Search


class API:
    """
    Simplify the requests to the Genius API
    """

    def __init__(self):
        """
        Initialize the Genius API session
        """
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
        """
        Get the lyrics from the Genius website

        Parameters:
            url (str): The lyrics page URL
            retry (bool): Retry the request if it fails (default False)
            wait_retry (int): Wait x seconds before retrying (default 30)
            wait (int): Wait x seconds before returning the result (default 0)

        Returns:
            lyrics (str or None): The lyrics of the song
        """

        htmlRes = requests.get(url).text

        html = BeautifulSoup(htmlRes, 'html.parser')

        # Find the correct lyrics div in the html file
        lyricsDiv: PageElement = html.find("div", class_="lyrics")
        if lyricsDiv == None:
            lyricsDiv = html.find("div", class_="Lyrics__Root-sc-1ynbvzw-0")

        if lyricsDiv != None:
            for br in lyricsDiv.find_all("br"):
                br.replace_with("\n")

            lyrics: str = lyricsDiv.get_text()

            # Normalize and remove weird chars from the lyrics
            lyrics = lyrics \
                .replace(r'[\(\[].*?[\)\]]', '') \
                .replace('\n', ' ').strip() \
                .replace(r'\s+', ' ')

            time.sleep(wait)

            return lyrics

        elif retry:
            # Retry if it failed
            print(f"Cannot scrap lyrics... waiting {wait_retry} secondes")
            time.sleep(wait_retry)
            return self.getLyrics(url, retry, wait_retry, wait)

        return None

    def getSong(
        self,
        id: int,
        with_lyrics: bool = False,
        retry: bool = False,
        wait_retry: int = 30,
        wait: int = 0
    ) -> Song:
        """
        Get a song from the Genius API and parse it into objects (selecting only interesting fields)

        Parameters:
            id (int): The song's ID
            with_lyrics (bool): Get the song with it's lyrics (default False)
            retry (bool): Retry the request if the getting lyrics method failed (default False)
            wait_retry (int): Wait x seconds if the getting lyrics method failed (default 30)
            wait (int): Wait x seconds after the lyrics method (default 0)

        Returns:
            lyrics (Song): The song
        """

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
        """
        Search for an album, artist, song in the Genius API

        Parameters:
            query (str): The search query

        Returns:
            Results (List[Search]): The provided results
        """

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
