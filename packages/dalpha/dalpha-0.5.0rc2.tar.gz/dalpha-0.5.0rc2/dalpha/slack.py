import json
import requests
from dalpha.logging import logger

def slack_alert(channel_name, text):
    '''
    channel_name : slack 채널 id 또는 #채널명
    text : 보낼 메세지
    원하는 slack channel에 메세지를 보내는 함수
    '''
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer xoxb-4286174283573-6855321848326-Z2QnHswtlITp5gNQj7eXVHjP'
    }
    payload = {
        "channel": channel_name,
        "text": text
    }
    response = requests.request("POST", 'https://slack.com/api/chat.postMessage', headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        logger.warning(f'error from slack_alert / response status_code {response.status_code}: {response.text}')
