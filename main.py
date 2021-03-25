import json
from api.API import API

api = API()

searchResults = api.search("Damso")
songs = api.populateResults(searchResults)

f = open("data.json", "w")
f.write(
    json.dumps(
        songs,
        default=lambda obj: obj.__dict__
    )
)
f.close()