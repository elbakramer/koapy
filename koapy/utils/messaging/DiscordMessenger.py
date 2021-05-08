import json

import requests

from discord import RequestsWebhookAdapter, Webhook

from koapy.config import config
from koapy.utils.messaging.Messenger import Messenger


class DiscordWebhookMessenger(Messenger):
    def __init__(self, url=None):
        self._url = url or config.get_string(
            "koapy.utils.messaging.discord.webhook_url"
        )
        assert self._url is not None and len(self._url) > 0
        self._webhook = Webhook.from_url(self._url, adapter=RequestsWebhookAdapter())

    def send_message(self, content):
        return self._webhook.send(content)


class DoItYourselfDiscordWebhookMessenger(Messenger):
    def __init__(self, url=None):
        self._url = url or config.get_string(
            "koapy.utils.messaging.discord.webhook_url"
        )
        assert self._url is not None and len(self._url) > 0

    def send_message(self, content):
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "content": content,
        }
        data = json.dumps(data)
        response = requests.post(
            self._url, headers=headers, data=data, params={"wait": "true"}
        )
        return response
