from flask import Flask
from api_utils import get_yt_captions, get_cornell_summary

app = Flask(__name__)

@app.get('/summary/<video_id>')
def get_summary(video_id: str):
    try:
        srt = get_yt_captions(video_id)
    except:
        return "Looks like subtitles are not available for this video. " +\
            "Try another one. We're working on subtitles generation for such cases."

    return get_cornell_summary(srt)
