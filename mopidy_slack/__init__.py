from __future__ import unicode_literals

import logging
import os

from .reporters import events
from . import help
from . import request
from . import next
from . import keep
from . import start
from . import connector

import tornado.web
from mopidy import config, ext
import json

__version__ = '0.1.0'
logger = logging.getLogger(__name__)

class EventsHandler(tornado.web.RequestHandler):
    def initialize(self, core, config, slack_connector, next_counter):
        self.core = core
        self.config = config
        self.slack_connector = slack_connector
        self.next_counter = next_counter
        self.listeners = []
        self.listeners.append(request.RequestListener(self.core, self.config["slack"]))
        self.listeners.append(next.NextListener(self.core,self.next_counter))
        self.listeners.append(keep.KeepListener(self.core,self.next_counter))
        self.listeners.append(start.StartListener(self.core, self.config["slack"]))
        # list listeners usages
        self.listeners.append(help.HelpListener(self.listeners))

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        callType = data['type']

        if callType == "url_verification":
            self.verify_url(data)
        
        if callType == "event_callback":
            event = data["event"]
            if event["type"] == "message":
                self.apply_message(event)

    def apply_message(self, event):
        text = event["text"]
        logger.debug("got message: " + text)
        for listener in self.listeners:
            if text.startswith(listener.command()):
                self.slack_connector.send_message(listener.action(text, event["user"]), event["channel"])
        self.set_header("Content-type","application/json")
        self.write({ 'status' : 'ok' })

    def verify_url(self, data):
        challenge = data['challenge']
        self.set_header("Content-type","application/json")
        self.write({ 'challenge' : challenge })
       

class Extension(ext.Extension):

    dist_name = 'Mopidy-Slack'
    ext_name = 'slack'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['bot_token'] = config.String()
        schema['signing_secret'] = config.String()
        schema['default_playlist_uri'] = config.String()
        schema['backend_priority'] = config.String()
        return schema
    
    def factory(self, config, core):
        self.slack_connector = connector.SlackConnector(config)
        self.next_counter = next.NextCounter()
        self.event_reporter = events.EventReporter.start(self.slack_connector, self.next_counter)
        return [
            ('/events', EventsHandler, {"core": core, "config": config, "slack_connector": self.slack_connector, "next_counter": self.next_counter})
        ]

    def setup(self, registry):
        registry.add('http:app', {
            'name': self.ext_name,
            'factory': self.factory
        })

