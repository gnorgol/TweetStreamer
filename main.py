import requests
import tweepy
import time
from io import BytesIO
from PIL import Image
import os

# Twitch authentication information
TWITCH_CLIENT_ID = 'YOUR_TWITCH_CLIENT_ID'
TWITCH_CLIENT_SECRET = 'YOUR_TWITCH_CLIENT_SECRET'
TWITCH_USERNAME = 'TWITCH_USERNAME'

# Twitter authentication information
TWITTER_API_KEY = 'YOUR_TWITTER_API_KEY'
TWITTER_API_SECRET_KEY = 'YOUR_TWITTER_API_SECRET_KEY'
TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get Twitter connection 2.0"""
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

# Twitter API configuration
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
client = get_twitter_conn_v2(
    TWITTER_API_KEY, TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
twitter_api = tweepy.API(auth)

# Download an image from a URL
def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

# Get a Twitch access token
def get_twitch_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()['access_token']

# Get the stream information
def get_stream_info(access_token):
    url = f'https://api.twitch.tv/helix/streams?user_login={TWITCH_USERNAME}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

# Tweet the game status with an image
def tweet_game_status_v2(api, client, game_name, thumbnail_url):
    try:
        # Download the image
        image = download_image(thumbnail_url)

        # Save the image temporarily
        image_path = 'thumbnail.jpg'
        image.save(image_path)

        # Upload the image to Twitter
        media = api.media_upload(image_path)

        # Create the tweet with the image
        tweet = f"🎮 I am live on Twitch! Join me for a game of {game_name}! 🎥 👉 https://www.twitch.tv/{TWITCH_USERNAME} #{game_name.replace(' ', '')} #Twitch #Live"
        client.create_tweet(text=tweet, media_ids=[media.media_id])

        print(f"Tweet sent with image: {tweet}")

    except tweepy.TweepyException as e:
        print(f"Error: Forbidden access during image upload. Details: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    access_token = get_twitch_access_token()
    stream_live = False
    while True:
        stream_info = get_stream_info(access_token)

        if stream_info:
            if not stream_live:
                game_name = stream_info[0]['game_name']
                thumbnail_url = stream_info[0]['thumbnail_url'].replace('{width}', '1280').replace('{height}', '720')
                tweet_game_status_v2(twitter_api, client, game_name, thumbnail_url)
                stream_live = True
            else:
                print("The stream is ongoing.")
        else:
            if stream_live:
                print("The stream has ended.")
                stream_live = False
            else:
                print("No stream is ongoing.")

        time.sleep(300) # Check every 5 minutes

if __name__ == "__main__":
    main()