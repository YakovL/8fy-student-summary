from flask import Flask
from api_utils import get_yt_captions, get_cornell_summary

app = Flask(__name__)

@app.get('/summary/<video_id>')
def get_summary(video_id: str):
    srt = get_yt_captions(video_id)

    return get_cornell_summary(srt)
