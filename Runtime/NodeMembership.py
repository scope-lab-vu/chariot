__author__="Subhav Pradhan, Shweta Khare"

from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import NodeExistsError
import json
import logging, netifaces, socket, time, datetime
import sys, getopt

def connection_state_listener(state):
    if state == KazooState.LOST:
        print "Connection to server lost!"
        sys.exit()
    elif state == KazooState.SUSPENDED:
        print "Connection to server has been suspended!"
        sys.exit()

def print_usage():
    print "USAGE:"
    print "NodeMembership --interface <network interface name> --templateName <node template name> --monitoringServer"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hitm",
                                    ["help", "interface=", "templateName=", "monitoringServer="])
    except getopt.GetoptError:
        print "Cannot retrieve passed parameters."
        print_usage()
        sys.exit()

    interface = None
    templateName = None
    monitoringServer = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-i", "--interface"):
            print "Interface name:", arg
            interface = arg
        elif opt in ("-t", "--templateName"):
            print "Node template name:", arg
            templateName = arg
        elif opt in ("-m", "--monitoringServer"):
            print "Monitoring server address:", arg
            monitoringServer = arg
        else:
            print "Invalid command line argument."
            print_usage()
            sys.exit()

    if interface is None or templateName is None:
        print "Network interface or node template name not provided!"
        sys.exit()

    if monitoringServer is None or monitoringServer == "localhost":
        monitoringServer = "127.0.0.1"
        print "Using monitoring server: ", monitoringServer

    # Get IP address associated with given interface name.
    addrs = netifaces.ifaddresses(interface)
    afinet = addrs[netifaces.AF_INET]
    ipaddress = afinet[0]['addr']

    # Setting default logging required to use Kazoo.
    logging.basicConfig()
    
    # Connect to ZooKeeper server residing at a known IP.
    # Set session timeout to 5 seconds; so a failure will
    # be detected in <= 5 seconds.
    zkClient = KazooClient(hosts=(monitoringServer+":2181"), timeout=5.0)

    # Add connection state listener to know the state
    # of connection between this client and ZooKeeper
    # server. 
    zkClient.add_listener(connection_state_listener)
    
    # Start ZooKeeper client/server connection.
    zkClient.start()
        
    # Store node name (has to be unique) that will be used 
    # to create ephemeral znode.
    name = socket.getfqdn()
    
    # Create root group membership znode if it doesn't
    # already exist. 
    zkClient.ensure_path("/group-membership")
    
    # Create node-specific ephemeral znode under above created 
    # root node.
    node_info = {}
    node_info["name"] = name
    node_info["nodeTemplate"] = templateName
    node_info["address"] = ipaddress
    node_info_json = json.dumps(node_info)
    try:
        zkClient.create("/group-membership/"+name, node_info_json, ephemeral=True)
    except NodeExistsError:
        print "ERROR: Node with name: ", name, " already exists!"
        sys.exit()

    # Endless loop to ensure client is alive in order
    # to keep associated (ephemeral) znode alive.
    while True:
        time.sleep(1)

if __name__=='__main__':
    main()
