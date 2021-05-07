from .Artist import Artist
from .Album import Album


class Song:
    def __init__(
        self,
        name: str,
        id: int,
        artist: Artist,
        album: Album,
        lyrics: str,
        image: str,
        date: str,
        url: str
    ):
        self.name = name
        self.id = id
        self.album = album
        self.lyrics = lyrics
        self.lyrics_dictionary = lyrics
        self.artist = artist
        self.image = image
        self.date = date
        self.url = url
