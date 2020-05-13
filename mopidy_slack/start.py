# stdlib imports

from . import listener

class StartListener(listener.CommandListener):

    def __init__(self,core, config):
        self.core = core
        self.config = config
        self.started = False

    def command(self):
        return 'start'

    def action(self, msg, user):
        if self.started:
            return 'Already started'

        playlists = self.core.playlists.as_list().get()
        uri = self.find_playlist(playlists, msg[6:])
        self.core.tracklist.add(uris=[uri])
        self.core.tracklist.shuffle()
        self.core.playback.play()
        self.started = True
        return 'On air'

    def usage(self):
        return 'start [playlist_name] - Start the radio broadcast'

    # Search for an existing playlist starting with query
    # Otherwise return the default playlist
    def find_playlist(self, playlists, query):
        if query == "":
            return self.config['default_playlist_uri']

        for playlist in playlists:
            if playlist is not None and playlist.name.lower().startswith(query.lower()):
                return playlist.uri

        # if nothing matches returns default
        return self.config['default_playlist_uri']
