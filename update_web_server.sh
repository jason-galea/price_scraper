#!/usr/bin/bash

# This relies on the scraper container from the "proxmox_automation" repo

# Delete
ssh root@172.26.0.125 "rm -rf /var/www/*"
echo

# Push
# scp -r ../price_scraper/* root@172.26.0.125:/var/www/
scp -r ./* root@172.26.0.125:/var/www/
echo

# Display
# ssh root@172.26.0.125 "tree /var/www/"
# echo

# Set folder permissions (matching proxmox_automation/services/scraper.yml)
ssh root@172.26.0.125 "chmod -R 755 /var/www"

# Restart webserver
ssh root@172.26.0.125 "systemctl restart apache2"
ssh root@172.26.0.125 "systemctl status apache2"
echo

