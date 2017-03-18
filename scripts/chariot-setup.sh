sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927

echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

sudo apt-get update

sudo apt-get install -y mongodb-org

echo "[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target

[Service]
User=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/mongodb.service

sudo systemctl start mongodb

sudo systemctl enable mongodb

wget https://download.robomongo.org/1.0.0-rc1/linux/robomongo-1.0.0-rc1-linux-x86_64-496f5c2.tar.gz

tar -xvf robomongo-1.0.0-rc1-linux-x86_64-496f5c2.tar.gz -C ~/

rm robomongo-1.0.0-rc1-linux-x86_64-496f5c2.tar.gz

git clone https://github.com/visor-vu/chariot-examples.git ~/chariot-examples

#sudo pip2 install chariot-runtime
