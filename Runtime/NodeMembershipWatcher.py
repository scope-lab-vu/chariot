__author__="Subhav Pradhan, Shweta Khare"

from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.protocol.states import EventType
import logging,time
import sys
from pymongo import MongoClient

def connection_state_listener(state):
    if state == KazooState.LOST:
        print "Connection to server lost!"
        sys.exit()
    elif state == KazooState.SUSPENDED:
        print "Connection to server has been suspended!"
        sys.exit()

def membership_watch(children,event):
    global CURRENT_MEMBERS

    if event and event.type==EventType.CHILD:
        # Check if new node(s) added. If so, add the new 
        # node(s) to CURRENT_MEMBERS.
        if len(children) > len(CURRENT_MEMBERS):
            for child in children:
                if child not in CURRENT_MEMBERS:
                    CURRENT_MEMBERS[child] = "ALIVE"
                    print "Node: ", child, " has joined!"
        else:
            # If new node(s) hasn't been added then it means
            # either node(s) have failed, or previously         
            # failed nodes have come alive.
            for member in CURRENT_MEMBERS:
                # Check failure scenario.
                if member not in children and 
                   CURRENT_MEMBERS.get(member) == "ACTIVE":
                    CURRENT_MEMBERS[member] = "FAULTY"
                    print "Node: ", member, " has failed!"
                    handle_failure(member)
                else:
                    # This is the scenario where previously
                    # failed node has come alive.
                    if CURRENT_MEMBERS.get(member) == "FAULTY":
                        CURRENT_MEMBERS[member] = "ACTIVE"
                        print "Node: ", member, " has re-joined!"
                        handle_rejoin(member)
                        
def handle_rejoin(node):
    db = MONGO_CLIENT["ConfigSpace"]
    lsColl = db["LiveSystem"]
    
    lsColl.update({"name":str(key), "status":"FAULTY"},
                  {"$set":{"status": "ACTIVE"}},
                  upsert = False)

def handle_failure(node):
    db = MONGO_CLIENT["ConfigSpace"]
    lsColl = db["LiveSystem"]
    failureColl = db["Failures"]
    ciColl = db["ComponentInstances"]
    
    # Add failure detection information in Failures collection.
    failureColl.update({"failedEntity": NODE_NAME}, 
                       {"$currentDate": {"detectionTime": {"$type": "date"}}, 
                        "$set": {"solutionFoundTime": 0, "reconfiguredTime": 0}}, 
                       upsert=True)
                
    # Mark node faulty and pull related processes in LiveSystem collection.
    lsColl.update({"name": NODE_NAME, "status": "ACTIVE"}, 
                  {"$set": {"status": "FAULTY"}}, 
                  upsert=False)
    
    lsColl.update({"name": NODE_NAME, "status": "FAULTY"}, 
                  {"$pull": {"processes": {"name": {"$ne": "null"}}}})

    # Store names of affected component instances.
    findResults = lsColl.find({"name": NODE_NAME, "status": "FAULTY"})
    failedComponentInstances = list()
    
    from SolverBackend import Serialize
    
    for findResult in findResults:
        node = Serialize(**findResult)
        for p in node.processes:
            process = Serialize(**p)
            for c in process.components:
                component = Serialize(**c)
                failedComponentInstances.append(component.name)

    # Update ComponentInstances collection using above collected information.
    for compInst in failedComponentInstances:
        ciColl.update({"name": compInst}, 
                      {"$set": {"status": "FAULTY"}})

    # Invoke solver for reconfiguration.
    invoke_solver()


def invoke_solver():
    SOLVER_IP = "master"
    SOLVER_PORT = 7778
    MY_PORT = 8888
    PING = "PING"
    PING_RESPONSE_READY = "READY"
    PING_RESPONSE_BUSY = "BUSY"
    SOLVE = "SOLVE"
    SOLVE_RESPONSE_OK = "OK"

    sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((SOLVER_IP, MY_PORT))

    print "Pinging solver for status"

    # First, ping solver and see if its is ready or busy.
    sock.sendto(PING, (SOLVER_IP, SOLVER_PORT))

    print "Waiting for solver response..."
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

    print "Solver response message:", data

    # If ready, ask solver to solve.
    if data == PING_RESPONSE_READY:
        print "Requesting solver for solution"
        sock.sendto(SOLVE, (SOLVER_IP, SOLVER_PORT))

        print "Waiting for solver response..."
        data, addr = sock.recvfrom(1024)

        print "Solver response message:", data
            
if __name__=='__main__':
    global CURRENT_MEMBERS
    global MONGO_CLIENT

    CURRENT_MEMBERS = dict()
    MONGO_CLIENT = MongoClient("mongo", 27017)

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
    
    # Use watchers recipe to watch for changes in
    # children of group membership znode. Each 
    # child of this node is an ephemeral node that
    # represents a group member. We set send_event
    # to true and set membership_watch as the
    # corresponding callback function.
    ChildrenWatch(client = zkClient,
                  path = "/test/group-membership",
                  func = membership_watch,
                  send_event = True)
    
    # Endless loop to ensure this detector process
    # doesn't die.    
    while True:
        time.sleep(30)
