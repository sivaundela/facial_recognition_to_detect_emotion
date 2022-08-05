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
        #print(temp['playlist_spotify_link'])
    return temp['playlist_spotify_link']

def extract(URL):
    client_id = "5356afb958c84e71a2c37c43e2a2cbf2" 
    client_secret = "83e531491e9c458ba658ac30c4c56bc0"

    #use the clint secret and id details
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # the URI is split by ':' to get the username and playlist ID
    playlist_id = URL.split("/")[4].split("?")[0]
    playlist_tracks_data = sp.playlist_tracks(playlist_id)

    #lists that will be filled in with features
    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []

    #go through the dictionary to extract the data
    for track in playlist_tracks_data['items']:
        playlist_tracks_id.append(track['track']['id'])
        playlist_tracks_titles.append(track['track']['name'])
        # adds a list of all artists involved in the song to the list of artists for the playlist
        artist_list = []
        for artist in track['track']['artists']:
            artist_list.append(artist['name'])
        playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])

    #create a dataframe
    features = sp.audio_features(playlist_tracks_id)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['title'] = playlist_tracks_titles
    features_df['first_artist'] = playlist_tracks_first_artists
    features_df['all_artists'] = playlist_tracks_artists
    features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                                'danceability', 'energy', 'key', 'loudness',
                                'mode', 'acousticness', 'instrumentalness',
                                'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]
    
    return features_df

# if __name__ == '__main__':
#     playlist = songs_by_emotion('Happy')
#     print(playlist)

# def print_songs(fnl_playlist_songs):
#     for el in fnl_playlist_songs:
#         print('playlist_name : ' + str(el['playlist_name']))
#         print('playlist_href : ' + str(el['playlist_href']))
#         print('playlist_spotify_link : ' + str(el['playlist_spotify_link']))
#         print('playlist_songs : ' )
#         for i in range(0,len(el['playlist_songs'])):
#             print(str(i+1) + ') ' + el['playlist_songs'][i])
#         print('-----------------------------------------------')