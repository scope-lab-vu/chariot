#from fabric.api import run, env, put, sudo, local, hosts
# source https://phab-riaps.isis.vanderbilt.edu/source/riaps-pycom/browse/ISORC/fab_src/
from fabric.api import *
import time
import socket
env.hosts = ['bbb-eb18.local']

env.password = 'riapspwd'
env.user = 'riaps'
env.sudo_password = 'riapspwd'

env.roledefs = {
  'three' : ['bbb-1f82.local', 'bbb-53b9.local', 'bbb-d5b5'],
  'two' : ['bbb-1f82.local', 'bbb-53b9.local'],
  'one' : ['bbb-1f82.local'],
  'mana' : ['192.168.0.108'],
  'monti': ['bbb-1f82.local'],
  'compute' : ['192.168.0.108', 'bbb-1f82.local', 'bbb-53b9.local', 'bbb-d5b5.local', 'bbb-ff98.local'],
  'egress' : ['bbb-ff98.local'],}
role = 'one'

def find_nodes():
  local("sudo arp-scan --interface=enp0s8 --localnet")
  local("sudo arp-scan --interface=enp0s3 --localnet")

@roles('mana')
def setupMana():
  sudo("pip2 install chariot-runtime")
  #update /etc/hosts

@roles('monti')
def setupMonti():
  """host a ZooKeeper server and a CHARIOT Node Membership Watcher"""
  #Update /etc/hosts with mongo-server and management-engine nodes
  sudo("apt-get install zookeeper")
  sudo("apt-get install zookeeperd")
  sudo("pip2 install chariot-runtime")
  #update configuration file located in /etc/chariot/chariot.conf
  run ("cd /etc/init.d && sudo update-rc.d chariot-nmw defaults 99")
  sudo("reboot")

@roles('compute')
def setupCompute():
  """Setup CHARIOT compute nodes"""
  #Update /etc/hosts with mongo-server and monitoring-server
  sudo("pip2 install chariot-runtime")
  #update configuration file located in /etc/chariot/chariot.conf
  run("cd /etc/init.d && sudo update-rc.d chariot-nm defaults 99")
  run("cd /etc/init.d && sudo update-rc.d chariot-dm defaults 99")
  print("\n after reboot check the MongoDB server for the presence of ConfigSpace database and Nodes collection. This collection should have a document each for every compute node.")
  sudo("reboot")

@roles('mana')
def initMana():
  """run the management engine for initial deployment"""
  run("chariot-me -i")

@roles('compute')
def checkLogs():
  """Check deployment manager logs on compute nodes to verify that deployement actions were taken"""
  run("cat /etc/chariot/logs")#not sure if this is cat-able

@roles('mana')
def testFailure():
  """test node egress (node failure)"""
  run("chariot-me") #Start management-engine without initial deplflag
  egress()

@roles('egress')
def egress():
  """poweroff egress nodes"""
  print("sudo poweroff")
  #sudo("reboot")#I think i prefer reboot because then it does both egress and ingress. 
