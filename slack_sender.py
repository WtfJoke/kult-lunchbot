from slackclient import SlackClient
import os


def send_message(text):
    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    response = sc.api_call(
        "chat.postMessage",
        channel="#lunch",
        text=text)
    if not response['ok']:
        print("something bad happened: " + response['error'])


send_message("Hello from Lunchbot! :tada:")