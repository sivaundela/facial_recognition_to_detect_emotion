import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="86889b60e92f45c288c8182c90e62fa8", client_secret="a966ae985bad4e4d9a634012e6f891e6"))

playlist_limit = 1
song_limit_per_playlist = 2

def songs_by_emotion(emotion):
    results = sp.search(q=emotion,type='playlist', limit=playlist_limit)
    gs = []
    
    for el in results['playlists']['items']:
        temp = {}
        temp['playlist_name'] = el['name']
        temp['playlist_href'] = el['href']
        temp['playlist_id'] = el['id']
        temp['playlist_spotify_link'] = el['external_urls']['spotify']
        print(temp['playlist_spotify_link'])
        gs.append(temp)
    
    fnl_playlist_songs = gs
    
    for i in range(0,len(gs)):
        res = sp.playlist(playlist_id = gs[i]['playlist_id'])
        srn = res['tracks']['items'][0:song_limit_per_playlist]
        tlist = []
        for el in srn:
            tlist.append(el['track']['name'])
        fnl_playlist_songs[i]['playlist_songs'] = tlist
    
    for el in fnl_playlist_songs:
        print('playlist_name : ' + str(el['playlist_name']))
        print('playlist_href : ' + str(el['playlist_href']))
        print('playlist_spotify_link : ' + str(el['playlist_spotify_link']))
        print('playlist_songs : ' )
        for i in range(0,len(el['playlist_songs'])):
            print(str(i+1) + ') ' + el['playlist_songs'][i])
        print('-----------------------------------------------')

if __name__ == '__main__':
    songs_by_emotion('Happy')

# def print_songs(fnl_playlist_songs):
#     for el in fnl_playlist_songs:
#         print('playlist_name : ' + str(el['playlist_name']))
#         print('playlist_href : ' + str(el['playlist_href']))
#         print('playlist_spotify_link : ' + str(el['playlist_spotify_link']))
#         print('playlist_songs : ' )
#         for i in range(0,len(el['playlist_songs'])):
#             print(str(i+1) + ') ' + el['playlist_songs'][i])
#         print('-----------------------------------------------')