import json

class Song:
  def __init__(
    self,
    name,
    id,
    artist,
    album,
    lyrics
  ):
    self.name = name
    self.id = id
    self.album = album
    self.lyrics = lyrics
    self.artist = artist
  
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)
