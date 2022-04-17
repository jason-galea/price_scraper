#!/usr/bin/bash

# This relies on the scraper container from the "proxmox_automation" repo

# Remove previous contents
# echo "### Removing old /var/www/"
ssh root@172.26.0.125 "rm -rf /var/www/*"
echo

# Copy current changes
# echo "### Pushing new /var/www/"
scp -r ../price_scraper/* root@172.26.0.125:/var/www/
echo

# # Display changes
# echo "### Showing new directory tree"
# ssh root@172.26.0.125 "tree /var/www/"
# echo

# Restart apache
# echo "### Restarting apache"
ssh root@172.26.0.125 "systemctl restart apache2"
ssh root@172.26.0.125 "systemctl status apache2"
echo

