import tweepy
import keys
import io
import os
from google.cloud import vision
from google.cloud.vision import types

def vision_feed(success):
    try:
        auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
        auth.set_access_token(keys.access_token, keys.access_token_secret)

        api = tweepy.API(auth)

        public_tweets = api.home_timeline()
        for tweet in public_tweets:
            print(tweet.text)

            media_files = set()

        #as shown on google tutorial
        for status in public_tweets:
            media = status.entities.get('media', [])
            if(len(media) > 0):
                media_files.add(media[0]['media_url'])

        for media_file in media_files:
            test = wget.download(media_file)
            # Instantiates a client
            client = vision.ImageAnnotatorClient()
            # The name of the image file to annotate
            file_name = os.path.abspath(test)
            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
            image = types.Image(content=content)
            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations
            print('')
            print('Description ' + test + ':')
            for label in labels:
                print(label.description)

            success = 1

    except ValueError:
        success = 0

success = 0
vision_feed(success)