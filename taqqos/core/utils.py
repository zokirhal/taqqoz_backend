import json
import requests
from hashlib import md5
from random import randint
from uuid import uuid4

from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.utils import timezone

BASE_URL = settings.SMS_GATEWAY_WITH_PLAY_MARKET["BASE_URL"]
LOGIN = settings.SMS_GATEWAY_WITH_PLAY_MARKET["LOGIN"]
PASSWORD = settings.SMS_GATEWAY_WITH_PLAY_MARKET["PASSWORD"]


def send_sms_with_play_mobile(phone_number, text):
    hash_key = md5(str(uuid4()).encode()).hexdigest()[:17]
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "messages": [
            {
                "recipient": phone_number.replace("+", ""),
                "message-id": "abs%s" % hash_key,
                "sms": {
                    "originator": "3700",
                    "content": {"text": text},
                },
            }
        ]
    }
    data = json.dumps(data, cls=DjangoJSONEncoder)
    requests.post(
        BASE_URL,
        auth=requests.auth.HTTPBasicAuth(LOGIN, PASSWORD),
        data=data,
        headers=headers,
        timeout=30,
    )


def send_sms_verification(instance, phone_number, text):
    is_demo = instance.is_demo
    sms_code = 4444 if is_demo else str(randint(1000, 9999))
    instance.sms_code = sms_code
    instance.sms_date = timezone.now()
    instance.save()

    if settings.ENVIRONMENT == "DEV" or is_demo:
        print(text % sms_code)
        return

    send_sms_with_play_mobile(phone_number, text % sms_code)


def send_sms(phone_number, text):
    if settings.ENVIRONMENT == "DEV":
        print(text)
        return

    send_sms_with_play_mobile(phone_number, text)