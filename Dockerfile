FROM python:3.12.1-slim-bullseye

### https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

### Packages
RUN apt update -y
RUN apt install -y firefox-esr
RUN apt install -y wget libpq-dev g++

### geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /usr/local/bin

### Python modules
ADD reqs.txt .
RUN python3.12 -m pip install -U pip setuptools wheel
RUN python3.12 -m pip install -r reqs.txt

### Cleanup
RUN apt remove -y wget g++
RUN apt autoremove -y
RUN rm -rf geckodriver*
RUN rm reqs.txt

WORKDIR /scraper/
