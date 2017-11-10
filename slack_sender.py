from slackclient import SlackClient
import os

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

response = sc.api_call(
  "chat.postMessage",
  channel="#lunch",
  text="Hello from Lunchbot! :tada:"
)

print(response)