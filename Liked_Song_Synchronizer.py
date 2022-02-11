import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pprint
from collections import defaultdict

scope = "user-library-read user-read-recently-played playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " - ", track['name'])

# results = sp.current_user_recently_played()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " - ", track['name'])

target_playlist_id = None
offset = 0
results = sp.current_user_playlists()
while results and results['next'] is not None:
    for playlist in results['items']:
        pprint.pprint(playlist)
        if playlist['name'] == 'Liked Songs (AUTO)':
            target_playlist_id = playlist['id']
            break
    results = sp.current_user_playlists(offset=offset)
    offset += 50

# print(target_playlist_id)
current_playlist_contents = defaultdict(list)

track_batch = sp.playlist_items(target_playlist_id)
offset = 1
while track_batch:
    if len(track_batch['items']) == 0:
        break
    for track_contents in track_batch['items']:
        track_details = track_contents['track']
        artist = track_details['artists'][0]['name']
        track_id = track_details['id']
        if track_id not in current_playlist_contents[artist]:
            current_playlist_contents[artist].append(track_id)
    track_batch = sp.playlist_items(target_playlist_id, offset=offset)
    offset += 100
    print(offset)

# results = sp.current_user_saved_tracks()
# offset = 1
# while results:
#     item = results['items'][1]
#     track = item['track']
#     print(track['artists'][0]['name'], " - ", track['name'])
#     results = sp.current_user_saved_tracks(offset=offset)
#     offset += 1
