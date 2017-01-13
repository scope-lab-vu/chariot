__author__ = "Subhav Pradhan"

import time
import socket, zmq, json
import copy, re
from solver_backend import SolverBackend
from new_configuration_solver_bound import NewConfigurationSolverBound
from chariot_helpers import Serialize, get_node_address
from deployment_manager import update_start_action, update_stop_action
from logger import get_logger

logger = get_logger("management_engine")

def solver_loop (db, zmq_socket, mongoServer, lookAhead):
    logger.info ("Solver loop started")

    # Find own IP.
    # NOTE: If mongoServer is running on localhost, we assume local deployment
    # which only involves a single machine. As such, we set the RE's address to
    # localhost as well.
    if mongoServer == "localhost":
        myIP = "localhost"
    else:
        myIP = socket.gethostbyname(socket.gethostname())

    myPort = 7000

    PING = "PING"
    PING_RESPONSE_READY = "READY"
    PING_RESPONSE_BUSY = "BUSY"
    SOLVE = "SOLVE"
    SOLVE_RESPONSE_OK = "OK"

    sock = None
    try:
        sock = socket.socket(socket.AF_INET,    # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind((myIP, myPort))
        inComputation = False
        while True:
            logger.info ("Waiting for request...")
            data, addr = sock.recvfrom(1024)    # buffer size is 1024 bytes

            if data == PING:
                logger.info ("Solver received a ping message")
                sock.sendto(PING_RESPONSE_READY, addr)
            elif data == SOLVE:
                logger.info ("Solver received solve request")
                if inComputation:
                    sock.sendto(PING_RESPONSE_BUSY, addr)
                else:
                    inComputation = True
                    sock.sendto(SOLVE_RESPONSE_OK, addr)
                    find_solution(db, zmq_socket, lookAhead)
                    inComputation = False
            else:
                if addr is not None:
                    sock.sendto(data, addr)
                inComputation = False

    except Exception, e:
        logger.info (e.message)
    except:
        if sock != None:
        #   sock.shutdown(socket.SHUT_RDWR)
            sock.close()

def find_solution(db, zmq_socket, lookAhead):
    if (lookAhead):
        # If RE in look ahead mode, then check if the triggering reconfiguration event is a
        # failure or an update. If it is the latter, we cannot look ahead so invoke the solver.
        reColl = db["ReconfigurationEvents"]
        findUpdateEvent = reColl.find_one({"completed":False, "kind":"UPDATE"})
        if findUpdateEvent is not None:
            invoke_solver(db, zmq_socket, False, lookAhead, True)
        else:
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
                logger.info ("Searching pre-computed solution for failure of node:" + node)
                laResult = laColl.find_one({"failedEntity":node})

                # If solution found, store time, get deployment actions and send them out.
                if laResult is not None:
                    logger.info ("Pre-computed solution found.")

                    # Check number of recovery actions to set actionCount.
                    recoveryActions = laResult["recoveryActions"]
                    numOfActions = len(recoveryActions)

                    # If number of recovery actions is 0 then no actions required, mark
                    # reconfiguration event as completed.
                    if numOfActions == 0:
                        reColl.update({"completed":False},
                                      {"$currentDate":{"solutionFoundTime":{"$type":"date"}, "reconfiguredTime":{"$type":"date"}},
                                       "$set": {"completed":True,
                                                "actionCount":0}})
                    else:
                        reColl.update({"completed":False},
                                      {"$currentDate":{"solutionFoundTime":{"$type":"date"}},
                                       "$set": {"actionCount":numOfActions}})

                        logger.info ("Populating Nodes collection with information about processes and component instances")
                        populate_nodes(db, recoveryActions)

                        # Making a copy as db insert below will modify by adding _id.
                        recoveryActionsToInsert = copy.deepcopy(recoveryActions)

                        # Store actions in DeploymentActions collection.
                        for ra in recoveryActionsToInsert:
                            daColl.insert(ra)

                        # Save each action in deploymentActions list and send each action.
                        for ra in recoveryActions:
                            deploymentActions.append(ra)

                            if send_action(db, ra, zmq_socket) is False:
                                return
                else:
                    logger.info ("Pre-computed solution not found!")

            # Failure handle attempt done. Look ahead again.
            look_ahead(db)
    else:
        invoke_solver(db, zmq_socket, False, lookAhead)

# Returns true if send succeeds, false otherwise.
def send_action (db, action, zmq_socket):
    # Default zeromq port to use.
    ZMQ_PORT = 8000

    # Get address of node to send action to.
    addr, port = get_node_address(db, action["node"])
    zmq_addr = None
    if (addr is not None and port is not None):
        zmq_addr = "tcp://%s:%d"%(str(addr), int(port))
    elif (addr is not None and port is None):
        zmq_addr = "tcp://%s:%d"%(str(addr), ZMQ_PORT)
    elif (addr is None and port is None):
        logger.error ("Cannot retrieve address of target node to send action to.")
        return False

    logger.info ("Sending action to DeploymentManager in node: " + str(action["node"]))

    try:
        zmq_socket.connect(zmq_addr)
        zmq_socket.send(json.dumps(action))
        response = zmq_socket.recv()
        zmq_socket.disconnect(zmq_addr)
    except zmq.error.Again as e:
        logger.info ("Caught exception: %s" % e)
        logger.error ("Cannot reach DeploymentManager in node: " + str(action["node"]))
        return False
    return True

# This function gets current configuration and invokes the solver. No looking ahead.
# This function returns list of deployment actions if solution found.
def invoke_solver(db, zmq_socket, initial, lookAhead, lookAheadUpdate = False):
    startTime = time.time()

    backend = SolverBackend()

    logger.info ("Loading ConfigSpace.")
    backend.load_state(db)
    logger.info ("Successfully loaded ConfigSpace and computed all component instances that needs to be deployed.")

    logger.info ("Populating ConfigSpace with new component instances that needs to be deployed.")
    backend.dump_component_instances(db)
    logger.info ("Successfully populated ConfigSpace with component instances.")

    elapsedTime = time.time() - startTime
    logger.info ("** Problem setup time (Phase 1 - Instance Computation Phase): " + str(elapsedTime))

    startTime = time.time()

    solver = NewConfigurationSolverBound(backend)

    # Store current deployment.
    solver.c2n_old = backend.c2n

    # Add component instance dependencies.
    dependencyAdditionTime = time.time()

    backend.add_dependency_constraints(solver)

    dependencyAdditionElapsedTime = time.time() - dependencyAdditionTime
    logger.info ("** Dependency constraint addition time: " + str(dependencyAdditionElapsedTime))

    # Add failure constraints.
    backend.add_failure_constraints(solver)

    # Add replication constraints.
    backend.add_replication_constraints(solver)

    # TODO: Check if current deployment is valid. If valid, no need to invoke solver.
    #solver.check_valid()

    elapsedTime = time.time() - startTime
    logger.info ("** Problem setup time (Phase 2 - Constraint Encoding Phase) : " + str(elapsedTime))

    logger.info ("Computing new deployment.")

    startTime = time.time() 

    # Get new deployment.
    result = solver.get_difference(initial)

    # List of actions to return.
    actions = None

    if(result is not None):
        [componentsToShutDown, componentsToStart, model, dist] = result
        reColl = db["ReconfigurationEvents"]
        if (dist == None):
            logger.info ("No deployment found!")

            elapsedTime = time.time() - startTime
            logger.info ("** Solver time (Phase 3 - Solution Computation Phase): " + str(elapsedTime))

            if not lookAhead or lookAheadUpdate:
                reColl.update({"completed":False},
                              {"$set":{"completed":True}})
            
            return None
        else:
            if dist !=0:
                logger.info ("Deployment computation done")
                if (model is not None):
                    logger.info ("Computing new deployment actions and populating DeploymentActions collection.")
                    actions = compute_deployment_actions(db, backend, solver, componentsToStart, componentsToShutDown)

                    elapsedTime = time.time() - startTime
                    logger.info ("** Solver time (Phase 3 - Solution Computation Phase): " + str(elapsedTime))
                    # Perform steps needed for non-lookahead or lookahead but update scenario.
                    if not lookAhead or lookAheadUpdate:
                        reColl.update({"completed":False},
                                      {"$currentDate":{"solutionFoundTime": {"$type": "date"}},
                                       "$set":{"actionCount":len(actions)}})

                        # Print actions (difference).
                        solver.print_difference(componentsToShutDown, componentsToStart)

                        logger.info ("Populating Nodes collection with information about processes and component instances")
                        populate_nodes(db, actions)

                        # Send actions using zeromq if not lookahead.
                        for action in actions:
                            if send_action(db, action, zmq_socket) is False:
                                return

                        # If lookahead update scenario then perform update lookahead.
                        if lookAheadUpdate:
                            logger.info ("Update lookahead mechanism")
                            look_ahead(db)

                    # If lookahead and initial then send action and perform initial lookahead.
                    if lookAhead and initial:
                        logger.info ("Populating Nodes collection with information about processes and component instances")
                        populate_nodes(db, actions)

                        for action in actions:
                            if send_action(db, action, zmq_socket) is False:
                                return

                        logger.info ("Initial lookahead mechanism")
                        look_ahead(db)
            elif dist == 0:
                logger.info ("Same deployment as before. No need for any changes.")

                elapsedTime = time.time() - startTime
                logger.info ("** Solver time (Phase 3 - Solution Computation Phase): " + str(elapsedTime))

                # No action so update reconfiguration event if non-lookahead or if lookahead and update scenario.
                if not lookAhead or lookAheadUpdate:
                    reColl.update({"completed":False},
                                  {"$currentDate":{"solutionFoundTime": {"$type": "date"}, "reconfiguredTime": {"$type": "date"}},
                                   "$set":{"completed":True,
                                           "actionCount":0}})

                    # If lookahead update scenario then perform lookahead.
                    if lookAheadUpdate:
                        look_ahead(db)
                    
                # Here we return empty list to distinguish returns for scenarios where no action is required and where
                # no solution is found. This is the former. For the latter, we return None (see dist == None check above).
                return list()
    else:
        logger.info ("New deployment could not be computed.")

        elapsedTime = time.time() - startTime
        logger.info ("** Solver time (Phase 3 - Solution Computation Phase): " + str(elapsedTime))

    return actions

def look_ahead(db):
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
        logger.info ("**Looking ahead for failure of node: " + node)
        # Copy database.
        client = db.client
        client.admin.command('copydb',
                             fromdb='ConfigSpace',
                             todb='LookAhead_'+node)

        tmpDb = client["LookAhead_"+node]

        # Mark node as FAULTY and invoke solver.
        mark_node_failure(tmpDb, node)

        # Invoke solver and store solution.
        recoveryActions = invoke_solver(tmpDb, None, False, True)

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
    logger.info ("** TIME TAKEN TO LOOK AHEAD: " + str(elapsedTime))

def mark_node_failure(db, nodeName):
    nColl = db["Nodes"]

    result = nColl.update({"name":nodeName, "status":"ACTIVE"},
                          {"$set": {"status":"FAULTY"}},
                          upsert = False)

    # Store names of affected component instances.
    findResults = nColl.find({"name":nodeName, "status":"FAULTY"})
    failedComponentInstances = list()
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

def populate_nodes(db, actions):
    nColl = db["Nodes"]

    for action in actions:
        # Get component instance name from process name.
        componentInstanceName = re.sub("process_", "", action["process"])

        # Get component instance with above name in ComponentInstances collection.
        ciColl = db["ComponentInstances"]
        componentInstanceToAdd = ciColl.find_one({"name":componentInstanceName})

        if componentInstanceToAdd is not None:
            processDocument = dict()
            processDocument["name"] = action["process"]
            processDocument["pid"] = long(0)
            processDocument["status"] = "TO_BE_DEPLOYED"
            processDocument["startScript"] = action["startScript"]
            processDocument["stopScript"] = action["stopScript"]
            processDocument["components"] = list()

            liveComponentInstDocument = dict()
            liveComponentInstDocument["name"] = componentInstanceName
            liveComponentInstDocument["status"] = "TO_BE_DEPLOYED"
            liveComponentInstDocument["type"] = componentInstanceToAdd["type"]
            liveComponentInstDocument["functionalityInstanceName"] = componentInstanceToAdd["functionalityInstanceName"]
            liveComponentInstDocument["alwaysDeployOnNode"] = componentInstanceToAdd["alwaysDeployOnNode"]
            liveComponentInstDocument["mustDeploy"] = componentInstanceToAdd["mustDeploy"]

            processDocument["components"].append(liveComponentInstDocument)

            nColl.update({"name":action["node"], "status":"ACTIVE"},
                         {"$push":{"processes":processDocument}})
        else:
            logger.info ("Component instance with name: " + componentInstanceName + " not found!")

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
        componentInstanceName = solver.componentNames[stopAction[0]]
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
