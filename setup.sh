#!/usr/bin/env bash

echo -e "\n==> Update apt package lists"
sudo apt update -y

echo -e "\n==> Upgrade apt packages"
sudo apt upgrade -y

echo -e "\n==> Install apt packages"
# sudo apt install -y selenium beautifulsoup4 firefox firefox-geckodriver
sudo apt install -y firefox firefox-geckodriver python3-pip

echo -e "\n==> Show python3 versions"
python3 --version

echo -e "\n==> Show pip versions"
python3 -m pip --version

echo -e "\n==> Upgrade pip base packages"
python3 -m pip install -U pip setuptools wheel

echo -e "\n==> Install pip requirements"
python3 -m pip install -r ./misc/reqs.txt
