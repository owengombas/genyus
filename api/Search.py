from .Artist import Artist

class Search:
  def __init__(
    self,
    title: str,
    url: str,
    artist: Artist,
    song_id: str,
  ):
    self.title = title
    self.url = url
    self.artist = artist
    self.song_id = song_id