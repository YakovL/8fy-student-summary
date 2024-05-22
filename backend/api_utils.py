import os
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_captions(video_id: str) -> str:
    """ get captions as a single string (bits are separated with linebreaks) """
    srt_array = YouTubeTranscriptApi.get_transcript(video_id)

    srt_text = ""
    for srt_item in srt_array:
        srt_text += srt_item['text'] + "\n"
    return srt_text

load_dotenv()
openai_client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])

def get_cornell_summary(text: str) -> str:
    """ requests OpenAI API to summarize """
    prompt = f"Summarize the following text using Cornell Note-Taking System (using bullet points):\n\n{text}"

    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content
