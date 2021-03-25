import json

class Artist:
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
  
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)