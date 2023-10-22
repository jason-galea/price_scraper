# price_scraper

A Flask-based webserver which extracts PC component data from a few Australian retailers.

## Requirements

Python 3.10 or higher.

## Instructions

Run locally:

    cp db.conf.example db.conf
    <edit db.conf>
    ./setup.sh
    ./run.py

Run via docker:

    cp db.conf.example db.conf
    <edit db.conf>
    docker compose up -d
