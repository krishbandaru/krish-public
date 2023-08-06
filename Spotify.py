"""
Class to make it easier to reuse access to Spotify
across diff apps.
"""

from datetime import date, datetime
import spotipy
from spotipy.client import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

class Spotify:
    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.SCOPE = "user-library-read playlist-read-private playlist-read-collaborative user-read-currently-playing user-read-playback-state user-modify-playback-state"

    def create_spotify_oauth(self):
        oauth_mgr = SpotifyOAuth(
            client_id=self.CLIENT_ID, 
            client_secret=self.CLIENT_SECRET, 
            redirect_uri="http://127.0.0.1:5000/auth", 
            scope=self.SCOPE)
        return spotipy.Spotify(oauth_manager=oauth_mgr)


    def get_current(self):
        sp = create_spotify_oauth()
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
        sp = create_spotify_oauth()
        devices = sp.devices()['devices']
        current_devices = []
        # TODO: Change to list comprehension
        for dev in devices:
            if dev['is_active']:
                current_devices.append(dev['name'])
        
        return current_devices


    def start_playback(self):
        sp = create_spotify_oauth()
        sp.start_playback()


    def pause(self):
        sp = create_spotify_oauth()
        try:
            sp.pause_playback()
        except:
            start_playback()


    def next(self):
        sp = create_spotify_oauth()
        sp.next_track()
        

    def previous(self):
        sp = create_spotify_oauth()
        sp.previous_track()
        

    def create_pl(self, name):
        sp = create_spotify_oauth()
        playlist = sp.user_playlist_create(self.user_id, 
                                           self.playlist_nane, 
                                           public=False)
        return playlist['id']

    