from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_captions(video_id: str):
    """ get captions as a single string (bits are separated with linebreaks) """
    srt_array = YouTubeTranscriptApi.get_transcript(video_id)

    srt_text = ""
    for srt_item in srt_array:
        srt_text += srt_item['text'] + "\n"
    return srt_text
