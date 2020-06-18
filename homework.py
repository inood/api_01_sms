import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')
client = Client(account_sid, auth_token)


def get_status(user_id):
    params = {
        'access_token': os.getenv("VK_API_TOKEN"),
        'user_ids': user_id,
        'fields': 'online',
        'v': '5.110',
    }
    status_request = requests.post('https://api.vk.com/method/users.get',
                                   params=params).json()['response']
    user_status = status_request[0]['online']
    return user_status


def sms_sender(sms_text):
    message = client.messages.create(
        body=sms_text,
        from_=number_from,
        to=number_to
    )
    return message.sid


if __name__ == "__main__":

    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
