# Mopidy-Slack

[Mopidy](http://www.mopidy.com/>) extension for controlling music from
[Slack](https://api.slack.com/>).

Requires you to create a slack app in your workspace.

## Installation

Install by running: `pip install Mopidy-Slack`

## Configuration

### Slack App

To work you need to [create a Slack App](https://api.slack.com/apps) and install it to your workspace.
This way you get the bot user OAuth access token, useful later
![](docs/bot_token.png)

Then you need to activate the events API. This APi requires the URL on which your mopidy instance is callable. If you are testing it on local you can use [ngork](https://ngrok.com/>) to expose your instance on the web.
![](docs/events.png)

### Mopidy 

In mopidy configuration, you must add your Slack app's Bot User OAuth Access Token and signing_secret.
Signing secret is found there:
![](docs/signing_secret.png)


In Mopidy configuration file:

```
[slack]
bot_token=xoxb-123456789123-1234567891234-xxx
signing_secret=xxxxXXXXxxxxXXXXxxxxXXXXxxxxXXXX
default_playlist_uri=spotify:playlist:2TYKzbVRYsyaVsPrnn2AnY
backend_priority=local,spotify
```

## Bot commands




## Project resources


- [Blog article](https://ablanchard.me)


## Changelog


v0.1.0 (2020-05-13)
-------------------

- Initial release.