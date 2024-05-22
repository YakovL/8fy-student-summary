import os
from dotenv import load_dotenv
from together import Together
from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_captions(video_id: str) -> str:
    """ get captions as a single string (bits are separated with linebreaks) """
    srt_array = YouTubeTranscriptApi.get_transcript(video_id)

    srt_text = ""
    for srt_item in srt_array:
        srt_text += srt_item["text"] + "\n"
    return srt_text

load_dotenv()
together_client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

def get_together_response(prompt: str) -> str:
    """ requests Together API to reply """
    response = together_client.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def get_cornell_summary(text: str) -> str:
    """ requests Together API to summarize """
    llama_max_context = 8000
    promt_start = "Summarize the following text using Cornell Note-Taking System. Use bullet points, add short summary in the end:\n\n"
    prompt = promt_start + text

    if len(prompt) < llama_max_context:
        return get_together_response(prompt)

    # have to split into chunks
    chunk_prompt_start = "Summarize the following text using Cornell Note-Taking System. " + \
        "Use bullet points."

    response_parts = ""
    pause_index: int = 0
    while pause_index < len(text) - 1:
        next_pause_index = min(
            pause_index + llama_max_context - len(chunk_prompt_start),
            len(text) - 1
        )

        # don't split words
        while not text[next_pause_index] in (" ", "\n"):
            next_pause_index -= 1
        # unlikely edge case
        if next_pause_index == pause_index:
            return "Error: The word is too long to summarize"

        chunk = text[pause_index:next_pause_index]
        chunk_response = get_together_response(chunk_prompt_start + chunk)
        response_parts += "\n\n" + chunk_response
        pause_index = next_pause_index

    summary_prompt_start = "These bullet points were created following the Cornell Note-Taking System. " + \
        "Please provide a short summary for them:\n\n" + response_parts

    #TODO: estimate the size of text/video that will cause this edge case to occur
    # presumably, this will never happen for real videos
    if len(summary_prompt_start) > llama_max_context:
        return response_parts

    summary_response = get_together_response(summary_prompt_start)
    return response_parts + "\n\n" + summary_response
