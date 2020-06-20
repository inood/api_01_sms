import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv('account_sid')
AUTH_TOKEN = os.getenv('auth_token')
NUMBER_FROM = os.getenv('number_from')
NUMBER_TO = os.getenv('number_to')
VK_API_VER = os.getenv('vk_api_ver')

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def get_status(user_id):
    params = {
        'access_token': os.getenv("VK_API_TOKEN"),
        'user_ids': user_id,
        'fields': 'online',
        'v': VK_API_VER,
    }
    status_request = requests.post('https://api.vk.com/method/users.get',
                                   params=params).json()['response']
    user_status = status_request[0]['online']
    return user_status


def sms_sender(sms_text):
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid


if __name__ == "__main__":

    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
