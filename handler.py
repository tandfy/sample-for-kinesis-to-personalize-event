import json
import boto3
import base64
import os

TRACKING_ID = os.environ['TRACKING_ID']

personalize_events = boto3.client('personalize-events')


def handler(event, _):
    for record in event['Records']:
        parsed_event = json.loads(
            base64.b64decode(record['kinesis']['data']))

        personalize_events.put_events(
            trackingId=TRACKING_ID,
            userId=str(parsed_event['userId']),
            sessionId=str(parsed_event['sessionId']),
            eventList=[{
                'sentAt': str(parsed_event['sentAt']),
                'eventType': parsed_event['eventType'],
                'properties': json.dumps({
                    'itemId': str(parsed_event['itemId'])
                })
            }]
        )
