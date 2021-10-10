# This is clearly a huge mess.
# It's basically pseudo-code, just documenting what the docker image will require.
# Final note for the docker image will be to record package/module versions

install_python_requirements() {
    # https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/

    # Packages
    sudo apt update 
    sudo apt -y install unzip xvfb libxi6 libgconf-2-4 default-jdk curl gnupg python3-pip
    # Python modules
    sudo python3 -m pip install selenium beautifulsoup4 mysql-connector-python

    # Chrome
    sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add 
    sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
    sudo apt -y update 
    sudo apt -y install google-chrome-stable 

    # Chromedriver (ASSUMING CHROME == 94.x)
    sudo wget https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip
    # WAIT FOR DOWNLOAD
    sudo unzip chromedriver_linux64.zip
    sudo chown root:root chromedriver 
    sudo chmod +x chromedriver
    sudo mv chromedriver /usr/bin/chromedriver
    sudo rm chromedriver_linux64.zip
}

install_mysql() {
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
    # CREATE USER 'scraper'@'localhost' IDENTIFIED BY 'password';
    # GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'scraper'@'localhost'
    # FLUSH PRIVILEGES;
    # exit

}

configure_mysql_tables() {
    # TODO:
    # Execute the contents of ./database/setup.sql
    pass
}

get_latest_config() {
    # Clone repo
    cd
    git clone https://github.com/jason-galea/price_scraper

    # Move folders
    sudo mv ~/price_scraper/website/* /var/www/html/
}
