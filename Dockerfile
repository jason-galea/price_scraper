FROM python:3.11.3-slim-bullseye

RUN apt update -y
RUN apt install -y firefox-esr
RUN apt install -y wget libpq-dev gcc

### .devcontainer nonsense
# RUN apt install -y git gnupg2
# RUN mkdir /root/.ssh/
# RUN touch /root/.ssh/id_rsa /root/.ssh/id_rsa.pub

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /usr/local/bin

ADD reqs.txt .

RUN python3.11 -m pip install -U pip setuptools wheel
RUN python3.11 -m pip install -r reqs.txt

RUN rm reqs.txt
