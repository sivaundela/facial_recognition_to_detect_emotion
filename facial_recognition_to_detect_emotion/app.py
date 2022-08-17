from flask import Flask, Response , render_template, request
import requests
from realtime import Video, songs_by_emotion

app=Flask(__name__)
@app.route('/',)
def index():
    return render_template('video.html')

def gen(camera):
    while True:
        frame=camera.get_frame()
        #print("playlist:",frame[1])
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def video():
    res=gen(Video())
    return Response((res),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recommend')
def recommend():
    v = Video()
    v.get_frame()
    playlist_details = songs_by_emotion(v.predicted_emotion)
    playlist_1 = playlist_details[0]
    playlist_2 = playlist_details[1]
    playlist_3 = playlist_details[2]
    # songs_list = songs_list[4]
    return render_template('results.html',playlist_details=playlist_details, playlist_1=playlist_1, playlist_2=playlist_2,playlist_3=playlist_3,predicted_emotion=v.predicted_emotion)

app.run(debug=True)