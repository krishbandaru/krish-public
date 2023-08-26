import os
from dotenv import load_dotenv
from Spotify import Spotify


# Pull secrets out of .env file (not checked in)
load_dotenv()
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

spotify = Spotify(CLIENT_ID, CLIENT_SECRET)

user, user_uri = spotify.get_user()
print(user, user_uri)
print(spotify.get_current())
# spotify.next()

results = spotify.search("track:Money%20artist:Pink%20Floyd")
print(results)
