# https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/


echo "Install Xvfb headless X11 display"
sudo apt update 
sudo apt -y install unzip xvfb libxi6 libgconf-2-4 


echo "Install Java"
sudo apt -y install default-jdk


echo "Install Google Chrome"
sudo apt -y install curl gnupg
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add 
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
sudo apt -y update 
sudo apt -y install google-chrome-stable 


# CHECK VERSION == 94.x


echo "Install Chromedriver"
sudo wget https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip
# NEED TO WAIT FOR DOWNLOAD
sudo unzip chromedriver_linux64.zip
sudo chown root:root chromedriver 
sudo chmod +x chromedriver
sudo mv chromedriver /usr/bin/chromedriver
sudo rm chromedriver_linux64.zip


# echo ""
