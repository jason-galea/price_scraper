### Some commands separated for docker caching

FROM python:3.11.3-slim-bullseye

RUN apt update -y
RUN apt install -y firefox-esr 
RUN apt install -y wget libpq-dev gcc

### be very very careful
RUN apt install -y git

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /usr/local/bin

RUN python3.11 -m pip install -U pip setuptools wheel
RUN python3.11 -m pip install flask pandas selenium beautifulsoup4
RUN python3.11 -m pip install psycopg2
