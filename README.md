# Project Title

A quick web parser for investing.com. We store the data for gold and silver in a sqlite database and then use flask in 
order to grab the data from from the db.

## Getting Started

Simply run the following the set up the database.
```bash
$ python3 GoldScrape.py
```
Run the following to start the web server.
```bash
$ export FLASK_APP=web_service.py
$ export FLASK_RUN_PORT=8080
$ flask run
```

If you want to scrape a larger or smaller range of data, change the START_DATE and END_DATE values inside GoldScrape.py.
The default is set to scrape from 1/1/2019 to 6/1/2019

### Prerequisites

Below is a dump of pip freeze of the project

* Python 3
* beautifulsoup4==4.7.1
* certifi==2019.3.9
* chardet==3.0.4
* Click==7.0
* Flask==1.0.3
* idna==2.8
* itsdangerous==1.1.0
* Jinja2==2.10.1
* MarkupSafe==1.1.1
* requests==2.22.0
* soupsieve==1.9.1
* urllib3==1.25.3
* Werkzeug==0.15.4
