import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="86889b60e92f45c288c8182c90e62fa8", client_secret="a966ae985bad4e4d9a634012e6f891e6"))

facedata = "haarcascade_frontalface_default.xml"       
cascade = cv2.CascadeClassifier(facedata)

model = load_model('model_weights.h5')

playlist_limit = 3
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
        gs.append(temp)
    fnl_playlist_songs = gs
    
    for i in range(0,len(gs)):
        res = sp.playlist(playlist_id = gs[i]['playlist_id'])
        srn = res['tracks']['items'][0:song_limit_per_playlist]
        tlist = []
        for el in srn:
            tlist.append(el['track']['name'])
        fnl_playlist_songs[i]['playlist_songs'] = tlist

    return fnl_playlist_songs

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()
        
        gray_img= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
        
        faces_detected = cascade.detectMultiScale(gray_img)  
        
        for (x,y,w,h) in faces_detected:  
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),thickness=2)  
            roi_gray=gray_img[y:y+w,x:x+h]  #cropping region of interest i.e. face area from  image 
            roi_gray=cv2.resize(roi_gray,(48,48))
                
            if np.sum([roi_gray])!=0:
                img_pixels = roi_gray.astype('float')/255
                img_pixels = tf.keras.utils.img_to_array(img_pixels)
                img_pixels = np.expand_dims(img_pixels, axis = 0)
                    
                predictions = model.predict(img_pixels)
                predictions_accuracy = np.amax(predictions)
        
                #find max indexed array  
                max_index = np.argmax(predictions[0])  
        
                emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')  
                predicted_emotion = emotions[max_index]
                #print("predicted_emotion:",predicted_emotion)
            
                cv2.putText(frame, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.putText(frame, str(round(predictions_accuracy*100, 2))+"%", (180, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
                #print("predicted_emotion:",playlist_link)

        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()


