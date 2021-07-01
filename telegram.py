import os

import requests
import datetime

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def send(chat: str, text: str):
    token = os.environ.get('BOT_TOKEN')
    url = "https://api.telegram.org/bot"
    chat = chat or 'me'
    if chat == 'chat':
        channel_id = os.environ.get('CHAT_ID')
    else:
        channel_id = os.environ.get('MY_ID')

    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")


def send_keep_alive(text: str = "I'm alive"):
    now = datetime.datetime.now()
    if now.minute == 30 or now.minute == 0:
        send('me', text)
