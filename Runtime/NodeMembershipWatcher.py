__author__="Subhav Pradhan, Shweta Khare"

from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.protocol.states import EventType
from pymongo import MongoClient
from InvokeManagementEngine import invoke_management_engine
import json
import logging,time
import sys, getopt

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
        # Handle node join.
        if len(children) > len(CURRENT_MEMBERS):
            for child in children:
                if child not in CURRENT_MEMBERS:
                    CURRENT_MEMBERS.append(child)
                    print "Node: ", child, " has joined!"
                    
                    # Get node information from zookeeper.
                    # NOTE: This returns tuple. First element has data.
                    nodeInfo = ZK_CLIENT.get("/group-membership/"+child)
                    nodeInfoJson = json.loads(nodeInfo[0])

                    handle_join(nodeInfoJson)            
        # Handle node failure.
        else:
            for member in CURRENT_MEMBERS:
                if member not in children:
                    print "Node: ", member, " has failed!"
                    CURRENT_MEMBERS.remove(member)
                    handle_failure(member)
                        
def handle_join(nodeInfo):
    # Create object to store in database.
    nodeToAdd = dict()
    nodeToAdd["name"] = nodeInfo["name"]
    nodeToAdd["nodeTemplate"] = nodeInfo["nodeTemplate"]
    nodeToAdd["status"] = "ACTIVE"

    interfaceToAdd = dict()
    interfaceToAdd["name"] = nodeInfo["interface"]
    interfaceToAdd["address"] = nodeInfo["address"]
    interfaceToAdd["network"] = nodeInfo["network"]

    nodeToAdd["interfaces"] = list()
    nodeToAdd["interfaces"].append(interfaceToAdd)

    nodeToAdd["processes"] = list()

    # Add node to database.
    db = MONGO_CLIENT["ConfigSpace"]
    nColl = db["Nodes"]
    # NOTE: Update used with upsert instead of insert because
    # we might be adding node that had previously failed or
    # been removed.
    nColl.update({"name":nodeInfo["name"]}, nodeToAdd, upsert = True)

    # Check if any application already exists. If there are
    # applications then it means that the node join has to
    # be treated as hardware update and therefore the solver
    # should be invoked. If there are no applications then
    # this node is addition is happening at system initialization
    # time so do not invoke the solver.
    systemInitialization = True
    
    if "GoalDescriptions" in db.collection_names():
        gdColl = db["GoalDescriptions"]
        if gdColl.count() != 0:
            systemInitialization = False
    
    if not systemInitialization:
        invoke_management_engine(MANAGEMENT_ENGINE, True)

def handle_failure(node):
    db = MONGO_CLIENT["ConfigSpace"]
    nColl = db["Nodes"]
    ciColl = db["ComponentInstances"]

    # Mark node faulty in Nodes collection.
    nColl.update({"name": node, "status": "ACTIVE"}, 
                 {"$set": {"status": "FAULTY"}}, 
                 upsert=False)

    # Store names of affected component instances.
    findResults = nColl.find({"name": node, "status": "FAULTY"})
    failedComponentInstances = list()
    
    from SolverBackend import Serialize
    
    for findResult in findResults:
        failedNode = Serialize(**findResult)
        for p in failedNode.processes:
            process = Serialize(**p)
            for c in process.components:
                component = Serialize(**c)
                failedComponentInstances.append(component.name)

    # Update ComponentInstances collection using above collected information.
    for compInst in failedComponentInstances:
        ciColl.update({"name": compInst}, 
                      {"$set": {"status": "FAULTY"}})

    # Pull related processes in Nodes collection.
    nColl.update({"name": node, "status": "FAULTY"}, 
                 {"$pull": {"processes": {"name": {"$ne": "null"}}}})

    # Invoke solver for reconfiguration.
    invoke_management_engine(MANAGEMENT_ENGINE, False)

def print_usage():
    print "USAGE:"
    print "NodeMembershipWatcher --monitoringServer <monitoring server address> --mongoServer <mongo server address>" \
          " --managementEngine <management engine address>"

def main():
    global CURRENT_MEMBERS
    global MONGO_CLIENT         # Mongo client object.
    global ZK_CLIENT            # Zookeeper client object.
    global MANAGEMENT_ENGINE    # Management engine address.
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hmds",
                                    ["help", "monitoringServer=", "mongoServer=", "managementEngine="])
    except getopt.GetoptError:
        print "Cannot retrieve passed parameters."
        print_usage()
        sys.exit()

    monitoringServer = None
    mongoServer = None
    MANAGEMENT_ENGINE = None
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-m", "--monitoringServer"):
            print "Monitoring server address:", arg
            monitoringServer = arg
        elif opt in ("-d", "--mongoServer"):
            print "Mongo server address :", arg
            mongoServer = arg
        elif opt in ("-s", "--managementEngine"):
            print "Management engine address :", arg
            mongoServer = arg
        else:
            print "Invalid command line argument."
            print_usage()
            sys.exit()

    if monitoringServer is None:
        monitoringServer = "localhost"
        print "Using monitoring server: ", monitoringServer

    if mongoServer is None:
        mongoServer = "localhost"
        print "Using mongo server: ", mongoServer

    if MANAGEMENT_ENGINE is None:
        MANAGEMENT_ENGINE = "localhost"
        print "Using management engine: ", MANAGEMENT_ENGINE

    # Setting default logging required to use Kazoo.
    logging.basicConfig()
    
    CURRENT_MEMBERS = list()
    MONGO_CLIENT = MongoClient(mongoServer, 27017)
    ZK_CLIENT = KazooClient(hosts=(monitoringServer+":2181"))
    
    # Add connection state listener to know the state
    # of connection between this client and ZooKeeper
    # server. 
    ZK_CLIENT.add_listener(connection_state_listener)
        
    # Start ZooKeeper client/server connection.
    ZK_CLIENT.start()
    
    # Create root group membership znode if it doesn't
    # already exist. 
    ZK_CLIENT.ensure_path("/group-membership")
    
    # Use watchers recipe to watch for changes in
    # children of group membership znode. Each 
    # child of this node is an ephemeral node that
    # represents a group member. We set send_event
    # to true and set membership_watch as the
    # corresponding callback function.
    ChildrenWatch(client = ZK_CLIENT,
                  path = "/group-membership",
                  func = membership_watch,
                  send_event = True)
    
    # Endless loop to ensure this detector process
    # doesn't die.    
    while True:
        time.sleep(5)

if __name__=='__main__':
    main()
