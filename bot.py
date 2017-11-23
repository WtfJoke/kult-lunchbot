# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2016 Shannon Burns
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Python Slack Bot class for use with the kult lunchbot app
"""
import os
import auth_token
import collections

from slackclient import SlackClient
from supported_apps import Apps


class Bot(object):
    def __init__(self):
        super(Bot, self).__init__()
        self.name = "Kult Lunchbot"
        # When we instantiate a new bot object, we can access the app from environment variables
        self.oauth = {"client_id": "269973088388.270476032388",
                      "client_secret": os.environ.get("SLACK_CLIENT_SECRET"),
                      "scope": "bot"}
        self.verification = os.environ.get("SLACK_VERIFICATION_TOKEN")

        # NOTE: Python-slack requires a client connection to generate
        # an oauth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.see #auth
        self.client = SlackClient("")

        # last 10 messages - for duplicate checks
        self.messages = collections.deque(maxlen=10)
        self.is_logged_in = False

    def auth(self, code):
        """
        Authenticate with OAuth and assign correct scopes.

        Parameters
        ----------
        code : str
            temporary authorization code sent by Slack to be exchanged for an
            OAuth token

        """
        # After the user has authorized this app for use in their Slack team,
        # Slack returns a temporary authorization code that we'll exchange for
        # an OAuth token using the oauth.access endpoint
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )
        # To keep track of authorized teams and their associated OAuth tokens,
        # we will save the team ID and bot tokens to our local database
        team_id = auth_response["team_id"]
        bot_token = auth_response["bot"]["bot_access_token"]
        auth_token.store(team_id, bot_token, Apps.SLACK)
        # Then we'll reconnect to the Slack Client with the correct team's bot token
        self.client = SlackClient(bot_token)
        self.is_logged_in = True

    def send_message(self, message, channel, team_id):
        post_message = self.get_client(team_id).api_call("chat.postMessage",
                                                         channel=channel,
                                                         text=message)
        # TODO add logging and add exception handling
        timestamp = post_message["ts"]

    def get_messages(self):
        return self.messages

    def append_message(self, message_key):
        self.messages.append(message_key)

    def get_client(self, team_id):
        token = auth_token.get(team_id)
        self.client = SlackClient(token)
        return self.client

    def get_name(self):
        return self.name
