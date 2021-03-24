import json

class Album:
  def __init__(
    self,
    name,
    id
  ):
    self.name = name
    self.id = id
  
  def toJson(self):
    return json.dumps(self, default=lambda o: o.__dict__)