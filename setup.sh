# This is clearly a huge mess.
# It's basically just documenting what the docker image will require.
# Still need to specify package & module versions

script_prereqs() {
    # https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/

    # Packages
    sudo apt update 
    sudo apt -y install unzip xvfb libxi6 libgconf-2-4 default-jdk curl gnupg python3-pip
    # Python modules
    sudo python3 -m pip install selenium beautifulsoup4 mysql-connector-python
    # MySQL connector
    wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-py3_8.0.26-1ubuntu21.04_amd64.deb
    dpkg -i mysql-connector-python-py3_8.0.26-1ubuntu21.04_amd64.deb
    # sudo apt --fix-broken install
    # dpkg -i mysql-connector-python-py3_8.0.26-1ubuntu21.04_amd64.deb

    # Chrome
    sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add 
    sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
    sudo apt -y update 
    sudo apt -y install google-chrome-stable 

    # Chromedriver (ASSUMING CHROME == 94.x)
    wget https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip
    # WAIT FOR DOWNLOAD
    sudo unzip chromedriver_linux64.zip
    sudo chown root:root chromedriver 
    sudo chmod +x chromedriver
    sudo mv chromedriver /usr/bin/chromedriver
    sudo rm chromedriver_linux64.zip
}

database_prereqs() {
    # https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
    # https://docs.rackspace.com/support/how-to/install-mysql-server-on-the-ubuntu-operating-system/

    sudo apt update
    sudo apt install mysql-server

    # TODO:
    # Automate these (Ansible, docker)
    sudo mysql_secure_installation
    # Y
    # 1
    # Enter password twice
    # yes to everything else

    # Configure MYSQL User
    sudo mysql
    # CREATE USER 'scraper'@'%' IDENTIFIED BY 'Password##123';
    # GRANT ALL PRIVILEGES ON PriceScraper.* TO 'scraper'@'%';
    # FLUSH PRIVILEGES;

    # OR:
    # CREATE USER 'scraper'@'10.1.1.160' IDENTIFIED BY 'Password##123';
    # GRANT ALL ON PriceScraper.* TO 'scraper'@'10.1.1.160';
    # FLUSH PRIVILEGES;
    

    ### Allow remote access:
    # /etc/mysql/mysql.conf.d/mysqld.cnf
    # #bind-address           = 127.0.0.1
    # bind-address           = 0.0.0.0

}


website_prereqs() {
    sudo apt update 
    sudo apt -y install apache2 php7.4 php7.4-mysql
}

get_latest_config() {
    # Clone repo
    cd
    git clone https://github.com/jason-galea/price_scraper

    # Move PHP files to website root
    sudo mv ~/price_scraper/website/* /var/www/html/
}

# I'm starting to look forward to docker now :)
