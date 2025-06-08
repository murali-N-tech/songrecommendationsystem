# spotify_api.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_client():
    client_id = '30cf249435ae4dbf89e4c0f858cdb2e6'
    client_secret = '630e31d73c78490c9cea0f55f7d01475'

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)
