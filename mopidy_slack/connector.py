# future imports
from __future__ import unicode_literals

# stdlib imports
import logging

from slack import WebClient

logger = logging.getLogger(__name__)

class SlackConnector():

    def __init__(self, config):
        self.config = config
        self.slack_client = WebClient(token=config["slack"]['bot_token'], run_async=True)
        self.channel = ""

    
    def send_message(self, body, channel=None):
        if channel is None:
            channel = self.channel
        else:
            self.channel = channel
        message = {
            "channel": channel,
            "username": "Radio Bot",
            "icon_emoji": ":robot_face",
            "text": body,
        }
        response = self.slack_client.chat_postMessage(**message)
