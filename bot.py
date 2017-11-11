from __future__ import print_function
import recastai
import os

client = recastai.Client(os.environ["RECAST_TOKEN"], 'de')
response = client.request.analyse_text('hallo')

if response.intent:
  print(response.intent.slug)
if response.intent.slug == 'YOUR_EXPECTED_INTENT':
  """Do your code..."""