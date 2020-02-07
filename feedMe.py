import tweepy
import keys
import io
import os
import json
import wget
from google.cloud import vision
from google.cloud.vision import types

def vision_feed(success):

    data = {}
    data['tweets'] = []

    try:
        auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
        auth.set_access_token(keys.access_token, keys.access_token_secret)
        api = tweepy.API(auth)
        public_tweets = api.home_timeline()
        
        for tweet in public_tweets:
            print(tweet.text)
            media_files = set()
            media = tweet.entities.get('media', [])
            if(len(media) > 0):
                media_files.add(media[0]['media_url'])           
            
            for media_file in media_files:
                test = wget.download(media_file)
                client = vision.ImageAnnotatorClient()
                file_name = os.path.abspath(test)
                with io.open(file_name, 'rb') as image_file:
                    content = image_file.read()
                image = types.Image(content=content)
                response = client.label_detection(image=image)
                labels = response.label_annotations
                print('')
                print('Description ' + test + ':')
                labelDescr = ""
                for label in labels:
                    print(label.description)
                    labelDescr = labelDescr + (label.description)

                data['tweets'].append({
                    'tweet': tweet.text,
                    'img': test,
                    'description': labelDescr
                })
            
        with open('feed.json', 'w') as feed_res:
            json.dump(data, feed_res)   
        success = 1

    except ValueError:
        success = 0

success = 0
vision_feed(success)