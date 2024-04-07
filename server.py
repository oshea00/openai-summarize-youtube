from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from urllib.parse import urlparse
import re
import markdown

GPT_MODEL = "gpt-4-turbo-preview"
GPT_MAX_TOKENS = 128000
MAX_PROMPT_LENGTH = 2000
client = OpenAI()

app = Flask(__name__)

def moderated_text_OK(text):
    # Call the OpenAI Moderation API to score the text
    response = client.moderations.create(input=text)
    moderation_score = response.results[0]
    return not moderation_score.flagged

def get_videoid(video_url):
    try:
        video_id = re.search('v=([^&]*)', video_url).group(1)
        return video_id
    except Exception as e:
        print(f"Error getting video ID from URL: {e}")
        return None

def get_video_transcript(video_url):
    parsed_url = urlparse(video_url)
    if parsed_url.scheme and parsed_url.netloc:
        # video_url is a valid URL format
        video_id = get_videoid(video_url)
        if video_id and len(video_id) > 0:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        else:
            return "Please provide a valid YouTube video"
    else:
        return "Invalid video_url format. Please provide a valid YouTube video"

    return ' '.join([t['text'] for t in transcript])

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

@app.route('/')
def index():
    # return the README.md content rendered as HTML
    with open("README.md", "r") as f:
        content = f.read()
    return markdown.markdown(content)

@app.route('/transcribe', methods=['GET'])
def transcribe_video():
    video_url = request.args.get('video_url')
    transcript = get_video_transcript(video_url)
    return transcript

@app.route('/summarize', methods=['GET'])
def summarize_video():
    video_url = request.args.get('video_url')
    transcript = get_video_transcript(video_url)
    messages = []
    default_system_message = "Summarize the text provided by the user"
    prompt = request.args.get('prompt')
    if prompt and len(prompt) < MAX_PROMPT_LENGTH:
        if moderated_text_OK(prompt):
            messages.append({"role": "system", "content": prompt})
        else:
            messages.append({"role": "system", "content": default_system_message})
    else:
        messages.append({"role": "system", "content": default_system_message})
    messages.append({"role": "user", "content": transcript})

    summarized_text = summarize_text(messages)
    return summarized_text

def summarize_text(messages):
    try:
        chat_response = chat_completion_request(messages)
        assistant_message = chat_response.choices[0].message
        summarized_text = assistant_message.content
        return summarized_text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary"

if __name__ == '__main__':
    app.run()