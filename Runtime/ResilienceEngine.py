__author__ = "Subhav Pradhan"

import sys, time, getopt
import pymongo
import socket, zmq, json
import copy
from SolverBackend import Serialize

def solver_loop (db, zmq_socket):
    print "Solver loop started"
    sock = None
    try:
        sock = socket.socket(socket.AF_INET,    # Internet
                             socket.SOCK_DGRAM) # UDP
        #sock.bind((socket.gethostname(), SOLVER_PORT))
        sock.bind(("127.0.0.1", SOLVER_PORT))
        print socket.gethostname()
        inComputation = False
        while True:
            print "Waiting for request..."
            data, addr = sock.recvfrom(1024)    # buffer size is 1024 bytes

            if data == PING:
                print "Solver received a ping message"
                sock.sendto(PING_RESPONSE_READY, addr)
            elif data == SOLVE:
                print "Solver received solve request"
                if inComputation:
                    sock.sendto(PING_RESPONSE_BUSY, addr)
                else:
                    inComputation = True
                    sock.sendto(SOLVE_RESPONSE_OK, addr)
                    find_solution(db, zmq_socket)
                    inComputation = False
            else: # ID
                if addr is not None:
                    sock.sendto(data, addr)
                inComputation = False

    except Exception, e:
        print e.message
    except:
        #print "Unexpected error:", sys.exc_info()[0]
        if sock != None:
        #   sock.shutdown(socket.SHUT_RDWR)
            sock.close()

def mongo_connect(serverName):
    try:
        client = pymongo.MongoClient(serverName)
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB server: %s" % e
        raise
    except pymongo.errors.ConfigurationError, e:
        print "Could not connect to MongoDB server: %s" % e
        raise
    print "Connected to MongoDB server"
    return client

def find_solution(db, zmq_socket):
    if (LOOK_AHEAD):
        # Current implementation only does look ahead for node failures, so look for nodes that
        # has failed, find corresponding solution in LookAhead collection, send solution
        # actions to related DM, and store solution actions in DeploymentActions collection.
        nColl = db["Nodes"]
        nResult = nColl.find({"status":"FAULTY"})

        faultyNodes = list()
        for r in nResult:
            faultyNodes.append(r["name"])

        laColl = db["LookAhead"]
        daColl = db["DeploymentActions"]
        deploymentActions = list()
        for node in faultyNodes:
            print "Searching pre-computed solution for failure of node:", node
            laResult = laColl.find_one({"failedEntity":node})

            # If solution found, store time, get deployment actions and send them out.
            if laResult is not None:
                print "Pre-computed solution found."
                reColl = db["ReconfigurationEvents"]

                # Check number of recovery actions to set actionCount.
                numOfActions = len(laResult["recoveryActions"])

                # If number of recovery actions is 0 then no actions required, mark
                # reconfiguration event as completed.
                if numOfActions == 0:
                    reColl.update({"entity":node, "completed":False},
                                  {"$currentDate":{"solutionFoundTime":{"$type":"date"}},
                                   "$currentDate":{"reconfiguredTime":{"$type":"date"}},
                                   "$set": {"completed":True,
                                            "actionCount":0}})
                else:
                    reColl.update({"entity":node, "completed":False},
                                  {"$currentDate":{"solutionFoundTime":{"$type":"date"}},
                                   "$set": {"actionCount":numOfActions}})

                    for action in laResult["recoveryActions"]:
                        # Store action.
                        daColl.insert(action)
                        deploymentActions.append(action)

                        # Send action.
                        if send_action(db, action, zmq_socket) is False:
                            return
            else:
                print "Pre-computed solution not found. Invoking solver."
                # If (pre-computed) solution not found, invoke solver.
                invoke_solver(db, zmq_socket, False)

        # Failure handle attempt done. Look ahead again.
        look_ahead(db, deploymentActions)
    else:
        invoke_solver(db, zmq_socket, False)

# Returns true if send succeeds, false otherwise.
def send_action (db, action, zmq_socket):
     # Get address of node to send action to.
    addr, port = get_node_address(db, action["node"])

    zmq_addr = None
    if (addr is not None and port is not None):
        zmq_addr = "tcp://%s:%d"%(str(addr), int(port))
    elif (addr is not None and port is None):
        zmq_addr = "tcp://%s:%d"%(str(addr), ZMQ_PORT)

    print "Sending action to DeploymentManager in node: ", str(action["node"])

    try:
        zmq_socket.connect(zmq_addr)
        zmq_socket.send(json.dumps(action))
        response = zmq_socket.recv()
        zmq_socket.disconnect(zmq_addr)
    except zmq.error.Again as e:
        print "Caught exception: ", e
        print "Error: Cannot reach DeploymentManager in node: ", str(action["node"])
        return False
    return True

# This function gets current configuration and invokes the solver. No looking ahead.
# This function returns list of deployment actions if solution found.
def invoke_solver(db, zmq_socket, initial):
    from SolverBackend import SolverBackend

    backend = SolverBackend()

    print "Loading ConfigSpace."
    backend.load_state(db)
    print "Successfully loaded ConfigSpace and computed all component instances that needs to be deployed."

    print "Populating ConfigSpace with new component instances that needs to be deployed."
    backend.dump_component_instances(db)
    print "Successfully populated ConfigSpace with component instances."

    print "Computing new deployment."

    from NewConfigurationSolverBound import NewConfigurationSolverBound
    solver = NewConfigurationSolverBound(backend)

    # Store current deployment.
    solver.c2n_old = backend.c2n

    # Add component instance dependencies.
    backend.add_component_instance_dependencies(solver)

    # Add failure constraints.
    backend.add_failure_constraints(solver)

    # Add replication constraints.
    backend.add_replication_constraints(solver)

    # TODO: Check if current deployment is valid. If valid, no need to invoke solver.
    #solver.check_valid()

    # Get new deployment.
    result = solver.get_difference(initial)

    # List of actions to return.
    actions = None

    if(result is not None):
        [componentsToShutDown, componentsToStart, model, dist] = result
        if (dist == None):
            print "No deployment found!"
            return None
        else:
            # Get failed node.
            # NOTE: Important to get failed nodes from backend solver and not from the database as
            # the latter could have changed from the time solver initiated its computation. We only
            # want nodes for which the solver computed the solution.
            failedNodeIndexes = backend.get_failed_nodes()

            reColl = db["ReconfigurationEvents"]

            if dist !=0:
                print "Deployment computation done"
                if (model is not None):
                    print "Computing new deployment actions and populating DeploymentActions collection."
                    actions = compute_deployment_actions(db, backend, solver, componentsToStart, componentsToShutDown)

                    # If distance != 0, there has to be some actions. So, update reconfiguration event
                    # appropriately.
                    if not LOOK_AHEAD:
                        for nodeIndex in failedNodeIndexes:
                            reColl.update({"entity":solver.nodeNames[nodeIndex], "completed":False},
                                          {"$currentDate":{"solutionFoundTime": {"$type": "date"}},
                                           "$set":{"actionCount":len(actions)}})

                    solver.print_difference(componentsToShutDown, componentsToStart)

                    print "Populating Nodes collection with information with processes and component instances"
                    populate_nodes(db, backend, solver, componentsToStart, componentsToShutDown)

                    # Send actions using zeromq if not lookahead.
                    if not LOOK_AHEAD:
                        for action in actions:
                            if send_action(db, action, zmq_socket) is False:
                                return
                    else:
                        # If lookahead then do initial lookahead for initial deployment.
                        if initial:
                            print "Initial lookahead mechanism"
                            look_ahead(db, actions)
            elif dist == 0:
                print "Same deployment as before. No need for any changes."

                # No action so update reconfiguration event.
                if not LOOK_AHEAD:
                    for nodeIndex in failedNodeIndexes:
                        reColl.update({"entity":solver.nodeNames[nodeIndex], "completed":False},
                                      {"$currentDate":{"solutionFoundTime": {"$type": "date"}, "reconfiguredTime": {"$type": "date"}},
                                       "$set":{"completed":True,
                                               "actionCount":0}})
                return None
    return actions

# Get node IP and port as a pair.
def get_node_address(db, node):
    nColl = db["Nodes"]
    result = nColl.find_one({"name":node})
    nodeSerialized = Serialize(**result)
    if (len(nodeSerialized.interfaces) > 0):
        # NOTE: We currently expect a node to have one interface.
        interfaceSerialized = Serialize(**nodeSerialized.interfaces[0])
        address = interfaceSerialized.address
        seperatorIndex = address.find(":")
        if (seperatorIndex is not None):
            ip = address[:(seperatorIndex)]
            port = address[(seperatorIndex+1):]
        else:
            ip = address
            port = None
        return ip, port
    else:
        return None, None

def look_ahead(db, actions):
    startTime = time.time()
    # Empty all existing documents from LookAhead collection.
    laColl = db["LookAhead"]
    laColl.remove({})

    # Get list of nodes that are currently available (and therefore can fail).
    nColl = db["Nodes"]
    result = nColl.find({"status":"ACTIVE"})
    aliveNodes = list()
    for r in result:
        nodeName = r["name"]
        aliveNodes.append(nodeName)

    for node in aliveNodes:
        print "**Looking ahead for failure of node: ", node
        # Copy database.
        client = db.client
        client.admin.command('copydb',
                             fromdb='ConfigSpace',
                             todb='LookAhead_'+node)

        tmpDb = client["LookAhead_"+node]

        # Play actions in above created tmpDb so that it reflects what the config space should be after
        # execution of deployment actions.
        for action in actions:
            handle_action(tmpDb, action)

        # Mark node as FAULTY and invoke solver.
        mark_node_failure(tmpDb, node)

        # If solver found solution, query deployment actions to get solution.
        recoveryActions = invoke_solver(tmpDb, None, False)
        if (recoveryActions is not None):
            # Store solution in main (ConfigSpace) db.
            entry = dict()
            entry["failedEntity"] = node
            entry["recoveryActions"] = list()

            for action in recoveryActions:
                entry["recoveryActions"].append(action)

            laColl.insert(entry)

        client.drop_database("LookAhead_"+node)

    elapsedTime = time.time() - startTime
    print "** TIME TAKEN TO LOOK AHEAD: ", elapsedTime

def mark_node_failure(db, nodeName):
    nColl = db["Nodes"]

    result = nColl.update({"name":nodeName, "status":"ACTIVE"},
                          {"$set": {"status":"FAULTY"}},
                          upsert = False)

    # Store names of affected component instances.
    findResults = nColl.find({"name":nodeName, "status":"FAULTY"})
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
    ciColl = db["ComponentInstances"]
    for compInst in failedComponentInstances:
        result = ciColl.update({"name":compInst},
                               {"$set":{"status":"FAULTY"}})

    # Pull all processes.
    result = nColl.update({"name":nodeName, "status":"FAULTY"},
                          {"$pull":{"processes":{"name":{"$ne":"null"}}}})

def handle_action(db, actionDoc):
    action = actionDoc["action"]
    actionCompleted = actionDoc["completed"]
    actionNode = actionDoc["node"]
    actionProcess = actionDoc["process"]
    actionStartScript = actionDoc["startScript"]
    actionStopScript = actionDoc["stopScript"]

    if action == "START" and not actionCompleted:
        # Update database to reflect affect of above start action.
        from DeploymentManager import update_start_action
        update_start_action(db, actionNode, actionProcess, actionStartScript, actionStopScript, 0)
    elif action == "STOP" and not actionCompleted:
        from DeploymentManager import update_stop_action
        # Update database to reflect affect of above stop action.
        update_stop_action(db, actionNode, actionProcess, actionStartScript, actionStopScript)

def populate_nodes(db, backend, solver, componentsToStart, componentsToShutDown):
    nColl = db["Nodes"]

    for info in componentsToStart:
        componentInstanceToAddName = solver.componentNames[info[0]]
        componentInstanceToAdd = backend.get_component_instance(componentInstanceToAddName)
        if componentInstanceToAdd is not None:
            startScript = ""
            stopScript = ""
            if (componentInstanceToAdd.type != ""):
                startScript, stopScript = backend.get_component_scripts(componentInstanceToAdd.type)

            # Generate start and stop scripts for CHARIOT components.
            if startScript == "":
                startScript = "start_" + componentInstanceToAdd.name
            if stopScript == "":
                stopScript = "stop_" + componentInstanceToAdd.name

            processDocument = dict()
            processDocument["name"] = "process_" + componentInstanceToAdd.name
            processDocument["pid"] = long(0)
            processDocument["status"] = "TO_BE_DEPLOYED"
            processDocument["startScript"] = startScript
            processDocument["stopScript"] = stopScript
            processDocument["components"] = list()

            liveComponentInstDocument = dict()
            liveComponentInstDocument["name"] = componentInstanceToAdd.name
            liveComponentInstDocument["status"] = "TO_BE_DEPLOYED"
            liveComponentInstDocument["type"] = componentInstanceToAdd.type
            liveComponentInstDocument["functionalityInstanceName"] = componentInstanceToAdd.functionalityInstanceName
            liveComponentInstDocument["node"] = componentInstanceToAdd.node
            liveComponentInstDocument["mustDeploy"] = componentInstanceToAdd.mustDeploy

            processDocument["components"].append(liveComponentInstDocument)

            nColl.update({"name":solver.nodeNames[info[1]], "status":"ACTIVE"},
                         {"$push":{"processes":processDocument}},
                         upsert = False)
        else:
            print "WARNING: Component instance with name:", componentInstanceToAddName, "not found!"

def compute_deployment_actions(db, backend, solver, componentsToStart, componentsToShutDown):
    actions = list()

    # Add all start actions.
    for startAction in componentsToStart:
        componentInstanceName = solver.componentNames[startAction[0]]
        componentInstance = backend.get_component_instance(componentInstanceName)
        if componentInstance is not None:
            startScript = ""
            stopScript = ""
            if (componentInstance.type != ""):
                startScript, stopScript = backend.get_component_scripts(componentInstance.type)

        action = dict()
        action["action"] = "START"
        action["completed"] = False
        action["process"] = "process_" + solver.componentNames[startAction[0]]
        action["node"] = solver.nodeNames[startAction[1]]
        action["startScript"] = startScript
        action["stopScript"] = stopScript

        actions.append(action)

    # Add all stop actions.
    for stopAction in componentsToShutDown:
        componentInstanceName = solver.componentNames[startAction[0]]
        componentInstance = backend.get_component_instance(componentInstanceName)
        if componentInstance is not None:
            startScript = ""
            stopScript = ""
            if (componentInstance.type != ""):
                startScript, stopScript = backend.get_component_scripts(componentInstance.type)

        action = dict()
        action["action"] = "STOP"
        action["completed"] = False
        action["process"] = "process_" + solver.componentNames[stopAction[0]]
        action["node"] = solver.nodeNames[stopAction[1]]
        action["startScript"] = startScript
        action["stopScript"] = stopScript

        actions.append(action)

    actionsToInsert = copy.deepcopy(actions) # Making a copy as db insert below will modify by adding _id.

    deplActionsColl = db["DeploymentActions"]
    for action in actionsToInsert:
        deplActionsColl.insert(action)

    return actions

def print_usage():
    print "USAGE:"
    print "ResilienceEngine --mongoServer <mongo server address> [--initialDeployment] [--lookAhead]"

def main():
    global LOOK_AHEAD
    global SOLVER_PORT
    global ZMQ_PORT
    global INITIAL_DEPLOYMENT

    # Defining types of messages exchanged between failure monitor and solver.
    global PING
    global PING_RESPONSE_READY
    global PING_RESPONSE_BUSY
    global SOLVE
    global SOLVE_RESPONSE_OK

    LOOK_AHEAD = False
    SOLVER_PORT = 7000
    ZMQ_PORT = 8000
    INITIAL_DEPLOYMENT = False


    PING = "PING"
    PING_RESPONSE_READY = "READY"
    PING_RESPONSE_BUSY = "BUSY"
    SOLVE = "SOLVE"
    SOLVE_RESPONSE_OK = "OK"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hmil",
                                   ["help", "mongoServer=", "initialDeployment", "lookAhead"])
    except getopt.GetoptError:
        print "Cannot retrieve passed parameters."
        print_usage()
        sys.exit()

    mongoServer = None
    initialDeployment = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-m", "--mongoServer"):
            print "Mongo server address:", arg
            mongoServer = arg
        elif opt in ("-i", "--initialDeployment"):
            print "Initial deployment"
            initialDeployment = True
        elif opt in ("-l", "--lookAhead"):
            print "Lookahead enabled"
            LOOK_AHEAD = True
        else:
            print "Invalid command line argument."
            print_usage()
            sys.exit()

    # If no mongoServer given then use default.
    if (mongoServer is None):
        #mongoServer = "mongo"
        mongoServer = "localhost"
        print "Using mongo server: ", mongoServer

    client = None
    db = None

    print "Connecting to mongo server:", mongoServer
    client = mongo_connect(mongoServer)

    if client is not None:
        if "ConfigSpace" in client.database_names():
            db = client["ConfigSpace"]
        else:
            print "ConfigSpace collection does not exists in database"
            sys.exit()
    else:
        print "MongoClient not constructed correctly"
        sys.exit()

    # Creating ZeroMQ context and client socket.
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REQ)

    # Set receive timeout of 3 seconds and set linger for clean termination.
    zmq_socket.setsockopt(zmq.RCVTIMEO, 3000)
    zmq_socket.setsockopt(zmq.LINGER, 0)

    if initialDeployment:
        invoke_solver(db, zmq_socket, True)
    else:
        solver_loop(db, zmq_socket)

    # Close socket and terminate context.
    zmq_socket.close()
    zmq_context.term()

if __name__ == "__main__":
    main()
