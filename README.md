# wtz-lunchbot

## Overview
This projects aims to scrape the [WTZ-Homepage](http://wtz-tagungszentrum.de) for current lunch menu.
Afterwards it shouts the scraped information (e.g the menu of today) to a slack channel

## Status
In development for personal usage

## Requirement
This project needs python 3 and uses [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4) for scraping website and 
[slack-client](https://github.com/slackapi/python-slackclient) for communicating with slack.

To install requirements execute:

`pip install -r requirements.txt`



## Execution
python scraper.py


