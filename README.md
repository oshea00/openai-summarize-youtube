## Description
Uses openai to summarize YouTube video transcripts. 
Demonstrates use of moderation api to check optional user-provided prompt.

## Installation
You will need to have OPENAI_API_KEY environment variable set to run this, or create a '.env' file in the directory (or parent) where script is run.

To install dependencies, use pipenv:

`> pipenv install`

Or, use pip3 with the requirements.txt

`> pip3 install -r requirements.txt`

## Usage
To run development server:

`> python server.py`

### API Endpoint: /summarize

#### Description
This endpoint returns a textual summary of the video and takes two parameters:

- `video_url` (required): A valid YouTube URL of the video whose transcript needs to be summarized.
- `prompt` (optional): A user-provided prompt that specifies how the transcript output should be treated.

### API Endpoint: /transcribe

#### Description
This endpoint returns the video transcript and takes takes one parameter:

- `video_url` (required): A valid YouTube URL of the video whose transcript needs to be transcribed.

## Examples

* [Transcribe](http://127.0.0.1:5000/transcribe?video_url=https://www.youtube.com/watch?v=1egAKCKPKCk&t=4s)
* [Summarize](http://127.0.0.1:5000/summarize?video_url=https://www.youtube.com/watch?v=1egAKCKPKCk&t=4s)
* [Summarize with a prompt to translate into Spanish](http://127.0.0.1:5000/summarize?video_url=https://www.youtube.com/watch?v=1egAKCKPKCk&t=4s&prompt=translate%20summary%20into%20Spanish)

## License

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This project is licensed under the [MIT License](LICENSE).