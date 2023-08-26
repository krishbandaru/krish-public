"""
Class to make it easier to reuse access to Spotify
across diff apps.
"""


import os
from dotenv import load_dotenv
from datetime import date, datetime
import spotipy
from spotipy.client import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

class Spotify:
    def __init__(self, CLIENT_ID=None, CLIENT_SECRET=None):
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.SCOPE = "user-library-read playlist-read-private playlist-read-collaborative user-read-currently-playing user-read-playback-state user-modify-playback-state"
        
        if CLIENT_ID==None or CLIENT_SECRET==None:
            raise Exception("ClientID and/or ClientSecret not set.")

    def create_spotify_oauth(self):
        oauth_mgr = SpotifyOAuth(
            client_id=self.CLIENT_ID, 
            client_secret=self.CLIENT_SECRET, 
            redirect_uri="http://127.0.0.1:5000/auth", 
            scope=self.SCOPE)
        return spotipy.Spotify(oauth_manager=oauth_mgr)


    def get_current(self):
        sp = self.create_spotify_oauth()
        playing = sp.currently_playing(market='US')
        if not playing:
            return "Player Stopped"
        
        artist = playing['item']['artists'][0]['name']
        track = playing['item']['name']
        return f"{artist} / {track}"


    def get_user(self):
        sp = self.create_spotify_oauth()
        self.user_info = sp.current_user()
        self.user_id = self.user_info['id']
        self.user_uri = self.user_info['uri']
        return self.user_id, self.user_uri


    def get_current_device(self):
        sp = self.create_spotify_oauth()
        devices = sp.devices()['devices']
        current_devices = []
        # TODO: Change to list comprehension
        for dev in devices:
            if dev['is_active']:
                current_devices.append(dev['name'])
        
        return current_devices


    def start_playback(self):
        self._call_playback_api("play")

    def pause(self):
        self._call_playback_api("pause")

    def next(self):
        self._call_playback_api("next")

    def previous(self):
        self._call_playback_api("previous")

    def play(self):
        self._call_playback_api("play")
        

    def search(self, str):
        sp = self.create_spotify_oauth()
        return sp.search(str)

        
    def create_pl(self, name):
        sp = self.create_spotify_oauth()
        playlist = sp.user_playlist_create(self.user_id, 
                                           self.playlist_nane, 
                                           public=False)
        return playlist['id']


    def _call_playback_api(self, action):
        try:
            sp = self.create_spotify_oauth()
            match action:
                case "pause":
                    try:
                        sp.pause_playback()
                    except:
                        raise
                case "play":
                    sp.start_playback()    
                case "next":
                    sp.next_track()
                case "previous":
                    sp.previous_track()                
        except SpotifyException as e:
            print(f"Error calling api: {e}")
            
            
def main():
    # Pull secrets out of .env file (not checked in)
    load_dotenv()
    CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

    spotify = Spotify(CLIENT_ID, CLIENT_SECRET)

    user_id, user_uri = spotify.get_user()
    print(user_id, user_uri)

    quit = False
    while not quit:
        print(f"\n{user_id} playing on {spotify.get_current_device()}")
        current = spotify.get_current()

        print(len(current)*'=')
        print(current)
        print(len(current)*'=')

        key = input("\n[q]uit - p[l]ay - [p]ause - [n]ext - pre[v]ious >   ")
        if key in ["q", "Q"]:
            quit = True
            print("Goodbye")
        elif key in ["n", "N"]:
            spotify.next()
        elif key in ["v", "V"]:
            spotify.previous()
        elif key in ["p","P"]:
            spotify.pause()
        elif key in ["l","L"]:
            spotify.play()

                        
if __name__ == "__main__":
    main()