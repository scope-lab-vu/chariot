# from fabric.api import run, env, put, sudo, local, hosts
# source https://phab-riaps.isis.vanderbilt.edu/source/riaps-pycom/browse/ISORC/fab_src/
from fabric.api import *
import time
import socket
import re
from fabric.contrib.files import exists
from fabric.decorators import parallel
env.hosts = ['bbb-1f82.local']

env.password = 'riapspwd'
env.user = 'riaps'
env.sudo_password = 'riapspwd'

APPS_HOME = '/home/riaps/riaps_apps'
mongoServer = '192.168.0.108'
managementEngine = '192.168.0.108'
monitoringServer = '192.168.0.103' #'bbb-1f82.local'
re_MongoServer = re.compile('MongoServer: localhost')
re_MonitoringServer = re.compile('MonitoringServer: localhost')
re_ManagementEngine = re.compile('ManagementEngine: localhost')
re_NodeName = re.compile('NodeName: default_name')
re_NodeTemplate = re.compile('NodeTemplate: default_template')

env.roledefs = {
  'four' : ['bbb-1f82.local', 'bbb-53b9.local', 'bbb-d5b5.local', 'bbb-ff98.local'],
  'three' : ['bbb-1f82.local', 'bbb-53b9.local', 'bbb-d5b5.local'],
  'two' : ['bbb-1f82.local', 'bbb-53b9.local'],
  'one' : ['bbb-1f82.local'],
  'mana' : [managementEngine],
  'monti': [monitoringServer],
  'compute' : ['bbb-53b9.local', 'bbb-d5b5.local', 'bbb-ff98.local'],
  'egress' : ['bbb-ff98.local'], }
role = 'one'

def find_nodes():
  local("sudo arp-scan --interface=enp0s8 --localnet")
  local("sudo arp-scan --interface=enp0s3 --localnet")
  
@roles('four')
@parallel
def reboot():
    sudo('reboot')

@roles('four')
@parallel
def setupNodes():
    """ installs pip2, and  copies and installs version of chariot from local ~/chariot"""
    #UNCOMMENT FOR NEW INSTALL
    #sudo("apt install python-pip -y")
    if not exists('~/chariot'):
        run('mkdir chariot')
    put('~/chariot', '~/')
    # Install edge CHARIOT runtime
    sudo("cd ~/chariot/Runtime && sudo pip2 install --upgrade .")
    #Install mongo client for testing UNCOMMENT FOR NEW INSTALL
    #sudo("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6")
    #run ('echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list')
    #sudo ('apt-get update')
    #sudo("apt-get install -y mongodb-clients")
    
    

@roles('mana')
def testMongoCommand():
    #local("mongo admin -u admin -p admin --eval \"db.getSiblingDB('dummydb').addUser('dummyuser', 'dummysecret')\"")
    if exists('/etc/mongod.conf_bak'):
        sudo('mv /etc/mongod.conf_bak /etc/mongod.conf')
    sudo('cp /etc/mongod.conf /etc/mongod.conf_bak')  # in case I screw up
    #Allow LAN connections
    local("sudo sed -i 's/127.0.0.1/127.0.0.1,192.168.0.111/g' /etc/mongod.conf")
    #Trying to allow remote connections. Didn't get it working. 
    #local("sudo sed -i 's/bindIp/#bindIp/g' /etc/mongod.conf")
    #local(r"sudo sed -i 's/#security:/security:\n authorization: '\''enabled'\''/g' /etc/mongod.conf")
    local("sudo systemctl restart mongod.service")

#@roles('mana')
def setupManagementEngine():
    """ Installs the server chariot runtime, and specifies location of mongoDB server"""
    # update /etc/hosts
    if not exists('/etc/hosts_bak'):
        local('sudo cp /etc/hosts /etc/hosts_bak')
    local('sudo cp /etc/hosts_bak /etc/hosts')  # in case I screw up
    #local('echo "' + mongoServer + ' MongoServer" >> /etc/hosts')
    local('echo "' + mongoServer + ' MongoServer" | sudo tee --append /etc/hosts')
    # Change from local if z3 server is being run remotely. 
    local('sudo -H pip2 install --upgrade chariot-runtime')
    
@roles('monti')
def testMonitor():
    sudo('hostname')

@roles('monti')
def setupMonitor():
  """host a ZooKeeper server and a CHARIOT Node Membership Watcher"""
  # Update /etc/hosts with mongo-server and management-engine nodes
  if not exists('/etc/hosts_bak'):
        sudo('cp /etc/hosts /etc/hosts_bak')
  sudo('cp /etc/hosts_bak /etc/hosts')  # in case I screw up
  sudo('echo "' + mongoServer + ' MongoServer" >> /etc/hosts')
  sudo('echo "' + managementEngine + ' ManagementEngine" >> /etc/hosts')
  # Install ZooKeeper UNCOMMENT FOR NEW NODES
  #sudo('apt update')
  #sudo("apt install zookeeper -y")
  #sudo("apt install zookeeperd -y")
  # update configuration file located in /etc/chariot/chariot.conf
  updateChariotConf()  
  sudo("systemctl enable chariot-nmw")
  sudo("systemctl restart chariot-nmw.service")

@roles('monti')
def ruok():
    """run this after booting a node if you want to know when zookeeper is available"""
    run('echo type ruok when prompted, zookeeper will eventually respond with imok')
    run('telnet localhost 2181')

@roles('compute')
@parallel
def setupCompute():
  """Setup CHARIOT compute nodes"""
  # Update /etc/hosts with mongo-server and monitoring-server
  #if exists('~/.bashrc'):
  #      sudo('mv ~/.bashrc ~/.bashrc_bak')        
  sudo('cp ~/.bashrc_bak ~/.bashrc')
  sudo('echo export APP_HOME=$HOME/riaps_apps >> ~/.bashrc')
  
  if not exists('/etc/hosts_bak'):
        sudo('cp /etc/hosts /etc/hosts_bak')
  sudo('cp /etc/hosts_bak /etc/hosts')  # in case I screw up
  sudo('echo "' + mongoServer + ' MongoServer" >> /etc/hosts')
  sudo('echo "' + monitoringServer + ' MonitoringServer" >> /etc/hosts')
  # Install edge CHARIOT runtime, handled in setupNodes
  updateChariotConf()  
  sudo("systemctl enable chariot-nm")
  sudo("systemctl enable chariot-dm")
  sudo("systemctl restart chariot-nm.service")
  sudo("systemctl restart chariot-dm.service")
  #print("\n reboot. after reboot check the MongoDB server for the presence of ConfigSpace database and Nodes collection. This collection should have a document each for every compute node.")
 
@roles('mana')
def initMana():
  """run the management engine for initial deployment"""
  run("chariot-me -i")

@roles('compute')
def checkLogs():
  """Check deployment manager logs on compute nodes to verify that deployement actions were taken"""
  run("cat /etc/chariot/logs")  # not sure if this is cat-able

@roles('mana')
def testFailure():
  """test node egress (node failure)"""
  run("chariot-me")  # Start management-engine without initial deplflag
  egress()

@roles('egress')
def egress():
  """poweroff egress nodes"""
  print("sudo poweroff")
  # sudo("reboot")#I think i prefer reboot because then it does both egress and ingress. 
  
#@roles('monti')
@roles('mana')
def updateChariotConf():   
    """replace default names in chariot.conf """ 
    if exists('/etc/chariot/chariot.conf_bak'):
        sudo('mv etc/chariot/chariot.conf_bak etc/chariot/chariot.conf')
    sudo('cp /etc/chariot/chariot.conf /etc/chariot/chariot.conf.bak')
    sudo("sed -i 's/default_template/BBB/g' /etc/chariot/chariot.conf")
    sudo("sed -i 's/MongoServer: localhost/MongoServer: " + mongoServer + "/g' /etc/chariot/chariot.conf")
    sudo("sed -i 's/MonitoringServer: localhost/MonitoringServer: " + monitoringServer + "/g' /etc/chariot/chariot.conf")
    sudo("sed -i 's/ManagementEngine: localhost/ManagementEngine: " + managementEngine + "/g' /etc/chariot/chariot.conf")
    hostName = run("hostname")
    sudo("sed -i 's/default_name/" + hostName + "/g' /etc/chariot/chariot.conf")
    
    #sed -i 's/original/new/g' file.txt
          
      # update configuration file located in /etc/chariot/chariot.conf
#     [Base]
#     NodeName: default_name
#     NodeTemplate: default_template
#     Interface: eth0
#     Network: chariot
#     
#     [Services]
#     MongoServer: localhost
#     MonitoringServer: localhost
#     ManagementEngine: localhost
    
