# Install python >= 3.9.4

echo "Install Pip"
sudo apt update
sudo apt -y install python3-pip


echo "Install required python modules"
sudo python3 -m pip install selenium beautifulsoup4