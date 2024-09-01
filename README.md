# TweetStreamer

This project is a Python script that integrates Twitch and Twitter APIs to automatically tweet when a Twitch stream goes live. The script downloads the stream's thumbnail, uploads it to Twitter, and posts a tweet with the stream's game name and a link to the Twitch stream.

## Features

- **Twitch API Integration**: Fetches stream information using Twitch API.
- **Twitter API Integration**: Posts tweets with stream information and thumbnail using Twitter API.
- **Automated Process**: Continuously checks for live streams and tweets when a stream goes live.

## Requirements

- Python 3.x
- `requests` library
- `tweepy` library
- `Pillow` library
- `Image` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/gnorgol/TweetStreamer.git
    cd TweetStreamer
    ```

2. Install the required libraries:
    ```sh
    pip install requests tweepy Pillow Image
    ```

3. Set up your authentication information in the script:
    ```python
    # Twitch authentication information
    TWITCH_CLIENT_ID = 'YOUR_TWITCH_CLIENT_ID'
    TWITCH_CLIENT_SECRET = 'YOUR_TWITCH_CLIENT_SECRET'
    TWITCH_USERNAME = 'TWITCH_USERNAME'

    # Twitter authentication information
    TWITTER_API_KEY = 'YOUR_TWITTER_API_KEY'
    TWITTER_API_SECRET_KEY = 'YOUR_TWITTER_API_SECRET_KEY'
    TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
    TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'
    ```

## Usage

Run the script:
```sh
python main.py