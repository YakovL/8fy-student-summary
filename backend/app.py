from flask import Flask, Response
from api_utils import get_yt_captions, get_cornell_summary

app = Flask(__name__)

@app.get('/summary/<video_id>')
def get_summary_stream(video_id: str):
    try:
        srt = get_yt_captions(video_id)
    except:
        return "Looks like subtitles are not available for this video. " +\
            "Try another one. We're working on subtitles generation for such cases."
    #TODO: indicate result status somehow to distinguish summary from problem
    # maybe use first char like 0 for summary and 1 for error

    def generate_response():
        summary_generator = get_cornell_summary(srt)
        for chunk in summary_generator:
            yield chunk
    return Response(generate_response(), mimetype='text/plain')

