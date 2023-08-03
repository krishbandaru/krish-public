""" 
Script to control Spotify playback using basic client credentials.
Therefore, only methods that don't require user auth are allowed.
"""

import os
from pprint import pprint
from dotenv import load_dotenv
from tinytag import TinyTag  # https://pypi.org/project/tinytag/
from datetime import date, datetime
import base64
from requests import post, get
import json

def get_client_id():
    return os.environ.get("SPOTIFY_CLIENT_ID")

def get_client_secret():
    return os.environ.get("SPOTIFY_CLIENT_SECRET")

def get_itunes_filename():
    return os.environ.get("ITUNES_FILENAME")



def get_access_token(client_id, client_secret):
    auth_string = client_id + ":" + client_secret
    auth_enc = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_enc), "utf-8")
    
    URL = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {"grant_type": "client_credentials"}
    result = post(URL, headers=headers, data=body)
    json_result = json.loads(result.content)
    pprint(json_result)
    try:
        token = json_result["access_token"]
    except:
        token = None

    return token


def get_auth_header(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
        }


def get_user_id(access_token):
    URL = "https://api.spotify.com/v1/me"
    headers=get_auth_header(access_token)

    result = get(URL, headers=headers)
    json_result = json.loads(result.content)
    


def getSongList(filename):
    count=0
    song_list=[]
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                pass
            else:
                song_list.append(line.strip())
                count += 1
    return count,song_list


# Helps not have to do a lot of 
# src_file_path = src_file_path.replace("'","\\'")"
def escape_non_alphanumeric_chars(string):
    escaped_string = re.sub(r'([^a-zA-Z0-9])', r'\\\1', string)
    return escaped_string


def create_playlist(access_token):
    # Create a uniquely named playlist since Spotify lets you reuse the 
    # same name for different ones and then it's hard to know which one is 
    # the latest.  Much easier to rename from within Spotify.
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    playlist_nane = f"iTunesExport-{dt_string}"

    # Create Spotify Playlist and get an ID back
    playlist_id = None
    URL = "https://api.spotify.com/v1/users/me/playlists"
    headers = get_auth_header(access_token)
    body = {
        "name": f"{playlist_nane}",
        "description": "New playlist from iTunes",
        "public": "false"
    }
    result = post(URL, headers=headers, data=body)
    json_result = json.loads(result.content)
    print(json_result)
    exit()

    return playlist_id


def add_to_playlist(playlist_id,song):

    # add song to playlist
    
    # return playlist_id
    pass




def main():
    
    # Pull secrets out of .env file (not checked in)
    load_dotenv()

    client_id = get_client_id()
    client_secret = get_client_secret()
    itunes_filename = get_itunes_filename()
    SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
    SCOPE = "user-read-private user-read-email playlist-modify-public playlist-modify-private"

    if not os.path.exists(itunes_filename):
        print("**Source playlist file not found.")
        exit()
    
    
    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        print("Error: unable to get access_token")
        exit()

    user_id = None        
    user_id = get_user_id(access_token)
    if not user_id:
        print(f"Error: invalid user_id ({user_id})")
        exit()
        
    song_list = []
    src_count = 0
    src_count,song_list = getSongList(itunes_filename)

    file_summary=f"{src_count} music files extracted from {itunes_filename}"
    file_summary_len=len(file_summary)
    print("\n")
    print(file_summary_len*'=')
    print(file_summary)
    print(file_summary_len*'=')

    """
    Sample entry
    /Users/user/Music/Music/Media.localized/Music/Artist/Album/01 Song.m4a
    """
    source_count = 0
    found_count = 0
    error_list = []
    ret=1

    playlist_id = create_playlist(access_token)
    
    if not playlist_id:
        print("Error: Playlist could not be created.")
        exit()

    for song in song_list:
        tag = TinyTag.get(song)
        artist_name = tag.artist
        album_name = tag.album
        song_name = tag.title
        
        full_track = f"{artist_name}/{album_name}/{song_name}"
        print (f"Adding: {full_track}")
        # 1. lookup Spotify URI for track
        # 2. if found, add track ID to playlist
        # 3. else, print not found and add to error_list
            # error_list.append(full_track)
        exit()
                
        source_count = source_count + 1


    print(f"Errors: {error_list}")
    print(f"Source Count: {source_count}\nGood count: {found_count}\nError count: {len(error_list)}")


if __name__ == '__main__':
    main()
