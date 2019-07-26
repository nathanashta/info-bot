import os
import json

import requests

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    # We don't want to reply to ourselves!
    if data['text'] == 'weather':
        weather = requests.get("api.openweathermap.org/data/2.5/weather?q=Chicago&APPID={3887bd167e909f96b57808bda8f98bbd}")
        send_message(weather['main']['temp'])
    return "ok", 200


def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id': os.getenv('GROUPME_BOT_ID'),
        'text': msg,
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()