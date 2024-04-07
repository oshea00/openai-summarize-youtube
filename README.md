## Description
Uses openai to summarize YouTube video transcripts. 
Demonstrates use of moderation api to check optional user-provided prompt.

## Installation
You will need to have OPENAI_API_KEY environment variable set to run this, or create a '.env' file in the directory (or parent) where script is run.

To install dependencies, use pipenv:

```
> pipenv install
```
Or, use pip3 with the requirements.txt
```
pip3 install -r requirements.txt
```

## Usage
To run development server:
```
> python server.py
```

## API Endpoint: /summarize

### Description
This endpoint takes two parameters:

- `video_url` (required): A valid YouTube URL of the video whose transcript needs to be summarized.

- `prompt` (optional): A user-provided prompt that specifies how the transcript output should be treated.

## License

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This project is licensed under the [MIT License](LICENSE).