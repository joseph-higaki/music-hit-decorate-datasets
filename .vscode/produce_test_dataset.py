import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time 
from datetime import datetime
import instagram 
import config

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = config.get_config("spotify_client_id"),
                                                           client_secret = config.get_config("spotify_client_secret")))


instagram_user = config.get_config("instagram_user")
instagram_password = config.get_config("instagram_password")
instagram_client = instagram.Instagram(instagram_user, instagram_password)


TRACK_COLUMNS = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 
'key',
'valence',
'mode',
  'instagram_url', 'instagram_followers']

def get_audio_features(trackid):
    audio_features = sp.audio_features(tracks=trackid)
    track = sp.track(trackid)
    row = pd.Series(
        [
            track["name"],
            track["album"]["name"],
            track["artists"][0]["name"],
            track["album"]["release_date"],
            track["duration_ms"],
            track["popularity"],
            audio_features[0]["danceability"],
            audio_features[0]["acousticness"],
            audio_features[0]["energy"],
            audio_features[0]["instrumentalness"],
            audio_features[0]["liveness"],
            audio_features[0]["loudness"],
            audio_features[0]["speechiness"],
            audio_features[0]["tempo"],
            audio_features[0]["time_signature"],
            audio_features[0]["key"],
            audio_features[0]["valence"],
            audio_features[0]["mode"],
            "",
            -1
        ]
        ,
        index = TRACK_COLUMNS
    )
    return row

def produce_test_dataset_by_spotify_playlist(spotify_playlist_id = "2zJ8THtx6HVqIBXDZbM8Qm"):
    df = pd.DataFrame(columns = TRACK_COLUMNS)
    tracks = sp.playlist(spotify_playlist_id)
    for track in tracks["tracks"]["items"]:
        trackid = track["track"]["id"]
        new_row = get_audio_features(trackid)

        instagram_artist_search_result = instagram_client.get_artist_by_name(new_row["artist"])
        instagram_artist = instagram_artist_search_result[0]
        instagram_followers = instagram_artist.followers
        instagram_url = instagram_artist.get_url()
        new_row["instagram_url"] = instagram_url
        new_row["instagram_followers"] = instagram_followers
        df = df.append(new_row, ignore_index=True)
    return_value_filename = "spotifyExtract{0}.csv".format(datetime.now().strftime("%Y-%m-%d_%H%M%S%f"))
    df.to_csv(return_value_filename, sep = ',')
    return return_value_filename


#produce_test_dataset_by_spotify_playlist("2be8Q4uvGVnH3didCoySP6")