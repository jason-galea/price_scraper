FROM python:3.11.3-slim-bullseye

### https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /scraper/

### Packages
RUN apt update -y
RUN apt install -y firefox-esr
RUN apt install -y wget libpq-dev gcc

### geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /usr/local/bin

### Python modules
ADD reqs.txt .
RUN python3.11 -m pip install -U pip setuptools wheel
RUN python3.11 -m pip install -r reqs.txt
# RUN python3.11 -m pip install debugpy

# ### .devcontainer nonsense
# RUN apt install -y git gnupg2
# RUN mkdir /root/.ssh/
# RUN touch /root/.ssh/id_rsa /root/.ssh/id_rsa.pub

### Cleanup
RUN apt remove -y gcc
RUN rm -rf geckodriver*
RUN rm reqs.txt
