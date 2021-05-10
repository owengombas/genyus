from typing import List
from .Song import Song


class Artist:
    name: str
    image: str
    id: str
    url: str
    songs: List[Song]

    def __init__(
        self,
        name: str,
        image: str,
        id: str,
        url: str
    ):
        self.name = name
        self.id = id
        self.image = image
        self.url = url
