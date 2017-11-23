"""
A REST API for lunch bot in Python
"""
import json
import bot
import lunchbot
from lunchmenu import KeywordAnalyzer
from flask import Flask, request, make_response, render_template
import logging
import auth_token
from configuration import Config

Config.load_config()
pyBot = bot.Bot()
slack = pyBot.client
lunchbot.create_menu()

application = Flask(__name__)


def slack_event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.

    Parameters
    ----------
    event_type : str
        type of event received from Slack
    slack_event : dict
        JSON response from a Slack reaction event

    Returns
    ----------
    obj
        Response object with 200 - ok or 501 - Not implemented

    """
    team_id = slack_event["team_id"]

    if event_type == "message":
        event = slack_event["event"]
        subtype = event.get("subtype")
        timestamp = event.get("ts")
        message = event.get("text")
        channel = event.get("channel")
        is_my_bot = subtype == 'bot_message' and event.get("username") == pyBot.get_name()

        key = team_id + '_' + message + '_' + timestamp

        duplicate_message = key in list(pyBot.get_messages())
        if duplicate_message or is_my_bot:
            logging.debug("Already answered message: " + message)
            return make_response("Already answered", 200)
        analyzer = KeywordAnalyzer(message).analyze()
        pyBot.append_message(key)
        if analyzer.is_triggered():
            logging.info("Triggered bot")
            if analyzer.is_today():
                menu_text = lunchbot.get_menu()
            elif analyzer.is_relative_day():
                menu_text = lunchbot.get_menu(analyzer.get_date())
            else:
                menu_text = lunchbot.get_menu_by_weekday(analyzer.get_day())

            logging.info("Send menu: " + menu_text)
            pyBot.send_message(menu_text, channel, team_id)
            return make_response("Posted food into channel", 200)
    elif event_type == "app_uninstalled":
        logging.info("bot was uninstalled - remove oauth token from database")
        auth_token.remove(team_id)
        return make_response("Removed app", 200)

    # Show not implemented if bot doesnt know how to handle this event
    message = "You have not added an event handler for the %s" % event_type
    logging.warning(message)
    return make_response(message, 501, {"X-Slack-No-Retry": 1})


@application.route("/thanks", methods=["GET", "POST"])
def thanks():
    """
    This route is called by Slack after the user installs our app. It will
    exchange the temporary authorization code Slack sends for an OAuth token
    which we'll save on the bot object to use later.
    To let the user know what's happened it will also render a thank you page.
    """
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')
    # The bot's auth method to handles exchanging the code for an OAuth token
    pyBot.auth(code_arg)
    return render_template("thanks.html")


@application.route("/slack", methods=["GET", "POST"])
def slack_listen():
    """
    This route listens for incoming events from Slack's Events API and uses the event
    handler helper function to route events to our Bot.
    """
    logging.debug("received data: " + str(request.data) + "\n and header: " + str(request.headers))
    slack_event = json.loads(request.data)

    # Send back slack url challenge - For more info: https://api.slack.com/events/url_verification
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })
    # Verify validation-token to prevent man in the middle
    if pyBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off slack's automatic retries
        logging.error(message)
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # Process subscribed slack-event
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        # Then handle the event by event_type and have your bot respond
        return slack_event_handler(event_type, slack_event)

    # If we get something else, send a simple helpful error response
    no_event_message = "[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for."
    logging.warning(no_event_message)
    return make_response(no_event_message, 404, {"X-Slack-No-Retry": 1})


@application.route('/hello')
def hello_world():
    return "hello"


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    application.run(debug=True)
