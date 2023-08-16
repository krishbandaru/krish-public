# Simple script to control Spotify playback

import os
from dotenv import load_dotenv
from datetime import date, datetime
import spotipy
from spotipy.client import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


# Pull secrets out of .env file (not checked in)
load_dotenv()
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SCOPE = "user-library-read playlist-read-private playlist-read-collaborative user-read-currently-playing user-read-playback-state user-modify-playback-state"

def create_spotify_oauth():
    oauth_mgr = SpotifyOAuth(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET, 
        redirect_uri="http://127.0.0.1:5000/auth", 
        scope=SCOPE)
    return spotipy.Spotify(oauth_manager=oauth_mgr)


def get_current():
    sp = create_spotify_oauth()
    playing = sp.currently_playing(market='US')
    if not playing:
        return "Player Stopped"
    
    artist = playing['item']['artists'][0]['name']
    track = playing['item']['name']
    return f"{artist} / {track}"


def get_user():
    sp = create_spotify_oauth()

    user_info = sp.current_user()
    user_id = user_info['id']
    user_uri = user_info['uri']
    return user_id, user_uri


def get_current_device():
    sp = create_spotify_oauth()
    devices = sp.devices()['devices']
    current_devices = []
    # TODO: Change to list comprehension
    for dev in devices:
        if dev['is_active']:
            current_devices.append(dev['name'])
    
    return current_devices


def pause(sp):
    try:
        sp.pause_playback()
    except:
        call_api("play")

    
def call_api(action):
    try:
        sp = create_spotify_oauth()
        match action:
            case "pause":
                pause(sp)
            case "play":
                sp.start_playback()    
            case "next":
                sp.next_track()
            case "previous":
                sp.previous_track()                
    except SpotifyException as e:
        print(f"Error calling api: {e}")


def main():
    user_id, user_uri = get_user()
    print(user_id, user_uri)

    quit = False
    while not quit:
        print(f"Playing on {get_current_device()}")
        print(get_current())
        # time.sleep(10)
        
        key = input("[q]uit - p[l]ay - [p]ause - [n]ext - pre[v]ious >   ")
        if key in ["q", "Q"]:
            quit = True
            print("\nGoodbye")
        elif key in ["n", "N"]:
            call_api("next")
        elif key in ["v", "V"]:
            call_api("previous")
        elif key in ["p","P"]:
            call_api("pause")
        elif key in ["l","L"]:
            call_api("play")

                        
if __name__ == "__main__":
    main()