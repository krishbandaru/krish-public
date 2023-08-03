# Script to

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect
import time


def get_client_id():
    return os.environ.get("SPOTIFY_CLIENT_ID")

def get_client_secret():
    return os.environ.get("SPOTIFY_CLIENT_SECRET")

def get_itunes_filename():
    return os.environ.get("ITUNES_FILENAME")


SCOPE = "user-library-read user-read-private user-read-email playlist-modify-public playlist-modify-private"

# App config
app = Flask(__name__)

app.secret_key = '!ycoF!MXosfm9DVo.T@v_@wZZZ-P8m'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/getUser")


@app.route('/getUser')
def get_all_tracks():
    sp_oauth = create_spotify_oauth()
    session.clear()

    return "done"


# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid



def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=get_client_id(),
            client_secret=get_client_secret(),
            redirect_uri=url_for('authorize', _external=True),
            scope=SCOPE)
    
