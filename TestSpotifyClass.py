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


