import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pprint

scope = "user-library-read user-read-recently-played playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " - ", track['name'])

results = sp.current_user_recently_played()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " - ", track['name'])

offset = 0
results = sp.current_user_playlists()
# pprint.pprint(results)
while results and results['next'] is not None:
    for playlist in results['items']:
        pprint.pprint(playlist)
        if playlist['name'] == 'Liked Songs (AUTO)':
            break
#     # if results['items']['name'] == 'Liked Songs (AUTO)':
#     for idx, item in enumerate(results['items']):
#         pprint.pprint(idx, item)
    results = sp.current_user_playlists(offset=offset)
    offset += 50

# offset = 1
# results = sp.current_user_saved_tracks()
# while results:
#     for idx, item in enumerate(results['items']):
#         track = item['track']
#         print(idx, track['artists'][0]['name'], " - ", track['name'])
#     results = sp.current_user_saved_tracks(offset=offset)
#     offset += 1