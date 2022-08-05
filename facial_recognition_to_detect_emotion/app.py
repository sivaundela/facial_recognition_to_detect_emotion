from flask import Flask, Response , render_template, request
import requests
from realtime import Video
from spotify_api import extract

playlist = ""

app=Flask(__name__)

@app.route('/',)
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame=camera.get_frame()
        global playlist
        playlist = frame[1]
        print("playlist:",playlist)
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video')
def video():
    res=gen(Video())
    return Response((res),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recommend')
def recommend():
   #requesting the URL from the HTML form
#    req = requests.get('https://open.spotify.com/playlist/5sE9Ah4fCG2ZhFfDFVlEQ7')
#    data = req.content
#    print(data)
   URL = playlist
   return render_template('results.html')

app.run(debug=True)