import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pprint
from collections import defaultdict

scope = "user-library-read user-read-recently-played playlist-read-private playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

target_playlist_id = None
offset = 0
results = sp.current_user_playlists()
while results and results['next'] is not None:
    for playlist in results['items']:
        # pprint.pprint(playlist)
        if playlist['name'] == 'Liked Songs (AUTO)':
            target_playlist_id = playlist['id']
            break
    offset += 50
    results = sp.current_user_playlists(offset=offset)

# print(target_playlist_id)
current_playlist_contents = defaultdict(list)

track_batch = sp.playlist_items(target_playlist_id)
offset = 100
while track_batch:
    if len(track_batch['items']) == 0:
        break
    for track_contents in track_batch['items']:
        track_details = track_contents['track']
        artist = track_details['artists'][0]['name']
        track_id = track_details['id']
        if track_id not in current_playlist_contents[artist]:
            current_playlist_contents[artist].append(track_id)
    offset += 100
    track_batch = sp.playlist_items(target_playlist_id, offset=offset)

# pprint.pprint(current_playlist_contents)

results = sp.current_user_saved_tracks()
offset = 0
flag = True
num_consecutive_dups_found = 0
while num_consecutive_dups_found <= 100:
    for track_contents in results['items']:
        track_details = track_contents['track']
        artist = track_details['artists'][0]['name']
        track_id = track_details['id']
        if track_id not in current_playlist_contents[artist]:
            sp.playlist_add_items(target_playlist_id, [track_id])
            num_consecutive_dups_found = 0
        else:
            num_consecutive_dups_found += 1
    offset += 20
    results = sp.current_user_saved_tracks(offset=offset)
