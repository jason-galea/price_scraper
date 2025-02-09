FROM python:3.12.1-slim-bullseye


ENV GECKODRIVER_VERSION=v0.35.0
ENV GECKODRIVER_URL=https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz


RUN apt update -y \
    && apt install -y firefox-esr \
    && apt install -y wget libpq-dev g++ \
    && wget $GECKODRIVER_URL \
    && tar -xvzf geckodriver* \
    && mv geckodriver /usr/local/bin \
    && rm -rf geckodriver* \
    && python3.12 -m pip install -U pip setuptools wheel \
    && python3.12 -m pip install \
        flask flask_sqlalchemy flask_migrate pandas selenium beautifulsoup4 psycopg2 \
    && apt remove -y wget g++ \
    && apt autoremove -y


WORKDIR /scraper/
