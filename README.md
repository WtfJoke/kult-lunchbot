[![Build Status](https://travis-ci.org/WtfJoke/kult-lunchbot.svg?branch=develop)](https://travis-ci.org/WtfJoke/kult-lunchbot)  [![Build status](https://ci.appveyor.com/api/projects/status/pwxgn4mpgrue13mb?svg=true)](https://ci.appveyor.com/project/WtfJoke/kult-lunchbot) 
[![codecov](https://codecov.io/gh/WtfJoke/kult-lunchbot/branch/develop/graph/badge.svg)](https://codecov.io/gh/WtfJoke/kult-lunchbot) [![Maintainability](https://api.codeclimate.com/v1/badges/4911a6d625e8bc609577/maintainability)](https://codeclimate.com/github/WtfJoke/kult-lunchbot/maintainability)
[![Python 3](https://pyup.io/repos/github/WtfJoke/kult-lunchbot/python-3-shield.svg)](https://pyup.io/repos/github/WtfJoke/kult-lunchbot/)
[![Updates](https://pyup.io/repos/github/WtfJoke/kult-lunchbot/shield.svg)](https://pyup.io/repos/github/WtfJoke/kult-lunchbot/) 

# kult-lunchbot [<img src="https://raw.githubusercontent.com/WtfJoke/kult-lunchbot/master/resources/icons/lunchbot_icon_fullbackground.png" width="40" height="40">](https://lunchbot-hn.slack.com/apps/A7YE00YBE-kult-lunchbot?page=1)

## Overview
This projects aims to scrape the [WTZ-Homepage](http://wtz-tagungszentrum.de) for current lunch menu.
Afterwards it shouts the scraped information (e.g the menu of today) to a slack channel

##### Development-Status
In development

## Requirement
This project requires python 3.6 (it wont run with 3.5 or lower) and a postgres database,
It uses following libraries:
* [Flask](http://flask.pocoo.org/) for providing various REST Interfaces (like [Slack-Events REST API](https://api.slack.com/events-api)).
* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4) for scraping website
* [pdfminer.six](https://github.com/pdfminer/pdfminer.six) for pdf text extraction
* [Slack-Client](https://github.com/slackapi/python-slackclient) for communicating with slack
* [psycopg2](http://initd.org/psycopg/) for postgres db access
* [peewee](http://docs.peewee-orm.com/en/latest/) as [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping)


To install requirements execute:

`pip install -r requirements.txt`

You also need to set following environment variables to make it work:
* SLACK_CLIENT_ID
* SLACK_CLIENT_SECRET
* SLACK_VERIFICATION_TOKEN
* (optional) if not provided in config.yml - Postgres Database-Config:
    * RDS_HOSTNAME
    * RDS_PORT
    * RDS_DB_NAME
    * RDS_USERNAME
    * RDS_PASSWORD

## Bot-Commands
Bot listens for messages which have following pattern (where date is optional): keyword + (date)
It is sufficient that the keyword (and the optional date) is somewhere in the message.
Keywords and dates are in german, because the whole output is german as well.

Currently supported keywords are:
* essen
* kult
* menü
* mittag

Currently supported date's are:
* week days
  * Montag
  * Dienstag
  * Mittwoch
  * Donnerstag
  * Freitag
* relative days
  * Morgen
  * Übermorgen
  * Gestern
  * Vorgestern
  
## Poor man every day scheduler
`/remind me Was gibt es heute zu essen? at 11:00 every weekday`

Or for a whole channel:

`/remind #channel Was gibt es heute zu essen? at 11:00 every weekday`


## Add to your slack channel
[![Add to Slack](https://platform.slack-edge.com/img/add_to_slack.png)](https://slack.com/oauth/authorize?scope=bot&client_id=269973088388.270476032388)

## Bot in Action
<img src="https://github.com/WtfJoke/kult-lunchbot/raw/master/resources/app_screenshot.png" width="587" height="420"> 


## Contribute

1. [Fork it](https://github.com/WtfJoke/kult-lunchbot#fork-destination-box)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
