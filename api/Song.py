import json

class Song:
  def __init__(
    self,
    name,
    id,
    artist,
    album,
    lyrics,
    image,
    date,
    url
  ):
    self.name = name
    self.id = id
    self.album = album
    self.lyrics = lyrics
    self.artist = artist
    self.image = image
    self.date = date
    self.url = url
  
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)
