__author__="Shweta Khare, Subhav Pradhan"

from kazoo.client import KazooClient
import logging, uuid, socket, time, datetime
import sys

def connection_state_listener(state):
    if state == KazooState.LOST:
        print "Connection to server lost!"
        sys.exit()
    elif state == KazooState.SUSPENDED:
        print "Connection to server has been suspended!"
        sys.exit()
        

if __name__=='__main__':
    # Setting default logging required to use Kazoo.
    logging.basicConfig()
    
    # Connect to ZooKeeper server residing at a known IP.
    zkClient = KazooClient(hosts='10.2.65.52:2181')

    # Add connection state listener to know the state
    # of connection between this client and ZooKeeper
    # server. 
    zkClient.add_listener(connection_state_listener)
    
    # Start ZooKeeper client/server connection.
    zkClient.start()
        
    # Set a unique name that will be used to create
    # ephemeral znode.
    name = "child_"+socket.getfqdn()+"_"+uuid.uuid4().hex
    
    # Create root group membership znode if it doesn't
    # already exist. 
    zkClient.ensure_path("/test/group-membership")
    
    # Create node specific ephemeral znode under above
    # created root node.
    zk.create("/test/group-membership/"+name,ephemeral=True)

    # Endless loop to ensure client is alive in order
    # to keep associated (ephemeral) znode alive.
    while True:
        time.sleep(30)
