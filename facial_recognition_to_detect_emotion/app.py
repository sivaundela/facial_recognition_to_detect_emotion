from flask import Flask, Response , render_template, request
import requests
from realtime import Video, songs_by_emotion

app=Flask(__name__)
predicted_emotion = 'neutral'
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
    playlist_details = songs_by_emotion(predicted_emotion)
    playlist_link = playlist_details[0]
    playlist_id = playlist_details[1]
    playlist_name = playlist_details[2]
    # songs_list = songs_list[4]
    return render_template('results.html',playlist_details=playlist_details, playlist_link=playlist_link, playlist_name=playlist_name,playlist_id=playlist_id,predicted_emotion=predicted_emotion)

app.run(debug=True)