FROM ubuntu:20.04

# RUN apt update -y
# RUN apt upgrade -y
# RUN apt install -y tzdata libgtk

RUN echo 'deb http://ftp.iinet.net.au/pub/ubuntu/ focal main restricted universe multiverse' > /etc/apt/sources.list
RUN echo 'Australia/Melbourne' > /etc/timezone

RUN apt update -y
RUN apt upgrade -y
RUN apt install -y libgtk-3-0 firefox firefox-geckodriver python3-pip


WORKDIR /opt/price_scraper
COPY . .

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install -r ./misc/reqs.txt

CMD ./run.py
