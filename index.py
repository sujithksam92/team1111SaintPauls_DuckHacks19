import json
import datetime
import boto3
import pprint
import urllib.request
import requests
import os
import time
import re
from slackclient import SlackClient
import math

# slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot_id = None
sentiment_1=[]
sentiment_2=[]
sentiment_3=[]

def slack_message(message, channel):
    token = 'xoxp-552862962503-554443790646-553567685525-90ebc2c33b5acccbca061b14804ed3f2'
    sc = SlackClient(token)
    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='duckhacksbot_esin',
                icon_emoji=':robot_face:')

def handler(event, context):
    data = {
        'output': 'Hello World',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

s3 = boto3.resource('s3')

#for bucket in s3.buckets.all():
#    print(bucket.name)

client = boto3.client('transcribe')
client_c = boto3.client('comprehend')


response = client.get_transcription_job(TranscriptionJobName='duckhacks-trans-demo')
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(response)
print("Transcription Name:")
print(response["TranscriptionJob"]["TranscriptionJobName"])
print("TranscriptionJobStatus:")
print(response["TranscriptionJob"]["TranscriptionJobStatus"])
r = requests.get(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"])
d=json.loads(r.text)
for trans in d["results"]["transcripts"]:
        string_1=trans['transcript']
        sentiment_1 = client_c.detect_sentiment(Text=string_1,LanguageCode='en')
        string_1=string_1[0:200]
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(sentiment_1['SentimentScore'])
print("\n")

response = client.get_transcription_job(TranscriptionJobName='duckhacks-trans-demo2')
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(response)
print("Transcription Name:")
print(response["TranscriptionJob"]["TranscriptionJobName"])
print("TranscriptionJobStatus:")
print(response["TranscriptionJob"]["TranscriptionJobStatus"])
r = requests.get(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"])
d=json.loads(r.text)
for trans in d["results"]["transcripts"]:
        string_2=trans['transcript']
        sentiment_2 = client_c.detect_sentiment(Text=string_2,LanguageCode='en')
        string_2=string_2[0:200]
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(sentiment_2['SentimentScore'])
print("\n")

response = client.get_transcription_job(TranscriptionJobName='duckhacks-trans-demo3')
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(response)
print("Transcription Name:")
print(response["TranscriptionJob"]["TranscriptionJobName"])
print("TranscriptionJobStatus:")
print(response["TranscriptionJob"]["TranscriptionJobStatus"])
r = requests.get(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"])
d=json.loads(r.text)
for trans in d["results"]["transcripts"]:
        string_3=trans['transcript']
        sentiment_3 = client_c.detect_sentiment(Text=string_3,LanguageCode='en')
        string_3=string_3[0:200]
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(sentiment_3['SentimentScore'])
#sentiment = client_c.detect_sentiment(Text=d['results']['transcripts']['transcript'],LanguageCode='en')


if(abs(sentiment_1['SentimentScore']['Positive']-sentiment_1['SentimentScore']['Negative'])<0.09):
        status_1="Fairly Neutral"
elif((sentiment_1['SentimentScore']['Positive']-sentiment_1['SentimentScore']['Negative'])<0):
        status_1="Negative"
elif((sentiment_1['SentimentScore']['Positive']-sentiment_1['SentimentScore']['Negative'])>0):
        status_1="Positive"

if(abs(sentiment_2['SentimentScore']['Positive']-sentiment_2['SentimentScore']['Negative'])<0.09):
        status_2="Fairly Neutral"
elif((sentiment_2['SentimentScore']['Positive']-sentiment_2['SentimentScore']['Negative'])<0):
        status_2="Negative"
elif((sentiment_2['SentimentScore']['Positive']-sentiment_2['SentimentScore']['Negative'])>0):
        status_2="Positive"

if(abs(sentiment_3['SentimentScore']['Positive']-sentiment_3['SentimentScore']['Negative'])<0.09):
        status_3="Fairly Neutral"
elif((sentiment_3['SentimentScore']['Positive']-sentiment_3['SentimentScore']['Negative'])<0):
        status_3="Negative"
elif((sentiment_3['SentimentScore']['Positive']-sentiment_3['SentimentScore']['Negative'])>0):
        status_3="Positive"

#if(sentiment_1['SentimentScore']['Positive']>sentiment_1['SentimentScore']['Negative']):
#        status="The conversation from "

message_1="The Tone Of The Below Conversation Is "+status_1+":\n"+string_1+"......"
message_2="The Tone Of The Below Conversation Is "+status_2+":\n"+string_2+"......"
message_3="The Tone Of The Below Conversation Is "+status_3+":\n"+string_3+"......"

slack_message(message_1,"eesalainternshipnamde")
slack_message(message_2,"eesalainternshipnamde")
slack_message(message_3,"eesalainternshipnamde")
