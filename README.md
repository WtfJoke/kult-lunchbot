# wtz-lunchbot

## Overview
This projects aims to scrape the WTZ-Homepage (http://wtz-tagungszentrum.de) for current lunch menu.
Afterwards it shouts the scraped information (e.g the menu of today) to a slack channel

## Status
In development for personal usage

## Requirement
This project needs python3 and uses BeautifulSoup4


`pip install BeautifulSoup4`

`pip install git+https://github.com/deanmalmgren/textract.git` 

 
### Why doesnt pip install textract work?
Published version has codec error which is not python3 compatible. Master is compatible
see https://github.com/deanmalmgren/textract/issues/176

### On Windows before texttract
Download swig (http://prdownloads.sourceforge.net/swig/swigwin-3.0.12.zip) and add it to your path



## Execution
python scraper.py


