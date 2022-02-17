from dotenv import load_dotenv
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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

PLAY_LIST_ID = os.getenv("PLAY_LIST_ID")


# get playlist items
def get_playlist_tracks(playlist_id=PLAY_LIST_ID, limit=100, offset=0, track_ids=[]):
    results = sp.playlist_items(
        playlist_id=playlist_id,
        additional_types=("track",),
        fields="items(track(id)), next",
        limit=limit,
        offset=offset,
    )

    for track in results["items"]:
        track_ids.append(track["track"]["id"])

    if results["next"] is None:
        return track_ids

    return get_playlist_tracks(
        playlist_id=playlist_id,
        limit=limit,
        offset=offset + limit,
        track_ids=track_ids,
    )


# spotify add song to playlist
def add_song_to_playlist(tracks, playlist_id=PLAY_LIST_ID):
    # cast song_id to array if it's not an array
    if not isinstance(tracks, list):
        tracks = [tracks]

    old_tracks = get_playlist_tracks(playlist_id=playlist_id)
    track_to_add = [track for track in tracks if track not in old_tracks]
    if not track_to_add:
        print("All songs are already in playlist!")
        return

    sp.playlist_add_items(playlist_id=playlist_id, items=track_to_add)
    print("All songs added to playlist.")


char_filter_list = ("(", ")", "-", "_", '"', "'", "’", "?")
# get song id from search query
def get_song_id(song_name, artist="", original_artist=""):
    song_name = "".join(ch for ch in song_name if ch not in char_filter_list)
    query = song_name
    if artist:
        query += " " + artist
    results = sp.search(q=query, type="track")
    items = results["tracks"]["items"]

    if not items:
        # try one more time without artist name
        if artist != "":
            return get_song_id(song_name, "", artist)
        print("Cannot find song:", query, "|" + original_artist)
        return None

    for item in items:
        item_name = "".join(ch for ch in item["name"] if ch not in char_filter_list)
        if item_name.lower() == song_name.lower():
            return item["id"]

    input_ = ""
    item_id = 0
    while (input_ != "y") and (input_ != "n"):
        if item_id >= len(items):
            input_ = input("Song not found. explicitly set uri? (empty for cancel) ")
            if input_ == "":
                return None
            return input_

        item = items[item_id]
        input_ = input(
            f"Song title `{item['name']}` by `{item['artists'][0]['name']}` for `{query} {original_artist}`? (y/n/empty for next) "
        )
        if input_.lower() == "y":
            return item["id"]
        else:
            item_id += 1

    return None


def find_song_ids(data):
    for item in data:
        if item.get("uri", False):
            continue

        song_id = get_song_id(item["song"], item["artist"])
        if song_id:
            item["uri"] = song_id

    return data


# load data
with open("data.json", "r") as json_file:
    data = json.load(json_file)


def write_uri():
    data["items"] = find_song_ids(data["items"])

    # write data
    with open("data.json", "w") as outfile:
        json.dump(data, outfile)


def add_songs_from_uri():
    # add songs to playlist
    uris = []
    for item in data["items"]:
        uris.append(item["uri"])

    add_song_to_playlist(uris)
