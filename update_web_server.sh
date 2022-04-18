#!/usr/bin/bash

### This relies on the scraper container from the "proxmox_automation" repo
USER="root"
HOST="172.26.0.125"
WWW="/var/www"
TMP="/tmp/apache"



### Delete
ssh $USER@$HOST "rm -rf $WWW/*"
echo

### Push
# scp -r ../price_scraper/* $USER@$HOST:$WWW/
scp -r ./* $USER@$HOST:$WWW/
echo

### Set permissions & ownership
ssh $USER@$HOST "chown -R www-data:www-data $WWW/"
ssh $USER@$HOST "chmod -R 755 $WWW"

### Display
# ssh $USER@$HOST "tree $WWW/"
# echo

### Restart webserver
ssh $USER@$HOST "systemctl restart apache2"
ssh $USER@$HOST "systemctl status apache2"
echo

