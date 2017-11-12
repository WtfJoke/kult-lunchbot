# kult-lunchbot

## Overview
This projects aims to scrape the [WTZ-Homepage](http://wtz-tagungszentrum.de) for current lunch menu.
Afterwards it shouts the scraped information (e.g the menu of today) to a slack channel

## Status
In development for personal usage

## Requirement
This project needs python 3.6 and uses [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4) for scraping website, 
[slack-client](https://github.com/slackapi/python-slackclient) for communicating with slack and [pdfminer.six](https://github.com/pdfminer/pdfminer.six) for pdf text extraction.

To install requirements execute:

`pip install -r requirements.txt`

## Add to your slack channel
[![Add to Slack](https://platform.slack-edge.com/img/add_to_slack.png)](https://slack.com/oauth/authorize?scope=bot&client_id=269973088388.270476032388)

