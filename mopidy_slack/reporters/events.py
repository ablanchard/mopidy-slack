# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka
from mopidy.core import CoreListener
from ..utils import title_dash_artist


logger = logging.getLogger(__name__)


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, slack_connector, next_counter):
        super(EventReporter, self).__init__()
        self.slack_connector = slack_connector
        self.next_counter = next_counter

    def on_start(self):
        logger.info('EventReporter started.')

    def track_playback_started(self, tl_track):
        logger.info('Track started {0}'.format(tl_track))

        current_track = tl_track.track
        current_track = "None" if current_track is None else title_dash_artist(current_track)
        self.slack_connector.send_message(body=current_track)
        self.next_counter.reset()
