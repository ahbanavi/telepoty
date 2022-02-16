import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=[
            "user-library-read",
            "playlist-modify-public",
            "playlist-modify-private",
        ],
    )
)

PLAY_LIST_ID = "6vBHSjzJHvMkiayb7IoOSw"

# spotify add song to playlist
def add_song_to_playlist(tracks, playlist_id=PLAY_LIST_ID):
    # cast song_id to array if it's not an array
    if not isinstance(tracks, list):
        tracks = [tracks]

    sp.user_playlist_add_tracks(user="", playlist_id=playlist_id, tracks=tracks)


# get song id from search query
def get_song_id(song_name, artist=""):
    query = "artist:" + artist + " track:" + song_name
    results = sp.search(q=query, type="track")
    items = results["tracks"]["items"]
    for item in items:
        if item["name"] == song_name:
            return item["id"]


add_song_to_playlist(get_song_id("This Year's Love", "David Gray"))
