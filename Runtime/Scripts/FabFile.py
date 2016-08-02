__author__="Subhav Pradhan"

from fabric.api import *

env.user='ubuntu'

@parallel
def start_node_membership_watcher(monitoringServer, mongoServer, managementEngine):
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/NodeMembershipWatcher.sh start "+monitoringServer+" "+mongoServer+" "+managementEngine)

@parallel
def stop_node_membership_watcher():
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/NodeMembershipWatcher.sh stop")

@parallel
def start_node_membership(interface, network, nodeTemplate, monitoringServer):
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/NodeMembership.sh start "+interface+" "+network+" "+nodeTemplate+" "+monitoringServer)

@parallel
def stop_node_membership():
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/NodeMembership.sh stop")

@parallel
def start_deployment_manager(mongoServer):
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/DeploymentManager.sh start "+mongoServer)

@parallel
def stop_deployment_manager():
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/DeploymentManager.sh stop")

@parallel
def start_resource_monitor():
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/ResourceMonitor.sh start")

@parallel
def stop_resource_monitor():
    run("nohup /home/ubuntu/workspace/chariot/Runtime/Scripts/ResourceMonitor.sh stop")

@parallel
def install_python_packages():
    run('sudo apt-get install -y python-dev; sudo apt-get install -y python-pip; sudo pip install kazoo; sudo pip install pymongo; sudo pip install netifaces; sudo pip install pyzmq; sudo pip install psutil')
