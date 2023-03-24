#!/usr/bin/env bash

echo -e "\n==> Link service to /etc/systemd/system/price_scraper.service"
sudo ln -s ./misc/price_scraper.service /etc/systemd/system/price_scraper.service

echo -e "\n==> Enable service"
sudo systemctl enable --now price_scraper
