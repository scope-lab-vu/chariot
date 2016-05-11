import getopt
import sys
import pymongo
import socket
import time

def execute_action():
    client = pymongo.MongoClient("localhost")
    db = client["ConfigSpace"]
    lsColl = db["LiveSystem"]

    if (NODE_NAME != "" and (START_ACTION or STOP_ACTION)):
        if PROCESS_NAME == "":
            if START_ACTION:
                print "STARTING node:", NODE_NAME
                result = lsColl.update({"name":NODE_NAME, "status":"FAULTY"},
                                       {"$set": {"status":"ACTIVE"}},
                                       upsert = False)
            elif STOP_ACTION:
                print "STOPPING node:", NODE_NAME

                # Store current time as detection time.
                failureColl = db["Failures"]
                failureColl.update({"failedEntity":NODE_NAME},
                                   {"$currentDate": {"detectionTime": {"$type": "date"}},
                                    "$set": {"solutionFoundTime":0, "reconfiguredTime":0}},
                                   upsert = True)

                # Mark node faulty.
                result = lsColl.update({"name":NODE_NAME, "status":"ACTIVE"},
                                       {"$set": {"status":"FAULTY"}},
                                       upsert = False)

                # Store names of affected component instances.
                findResults = lsColl.find({"name":NODE_NAME, "status":"FAULTY"})
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
                result = lsColl.update({"name":NODE_NAME, "status":"FAULTY"},
                                       {"$pull":{"processes":{"name":{"$ne":"null"}}}})

        else:
            if START_ACTION:
                print "Processes can only be STARTED by DM"
            elif STOP_ACTION:
                print "STOPPING process:", PROCESS_NAME, "on node:", NODE_NAME
                result = lsColl.update({"name":NODE_NAME, "status":"ACTIVE", "processes":{"$elemMatch":{"name":PROCESS_NAME, "status":"ACTIVE"}}},
                                       {"$set":{"processes.$.status":"FAULTY"}},
                                       upsert = False)

                # Store names of affected component instances.
                findResults = lsColl.find({"name":NODE_NAME, "status":"ACTIVE", "processes":{"$elemMatch":{"name":PROCESS_NAME, "status":"FAULTY"}}})
                failedComponentInstances = list()
                from SolverBackend import Serialize
                for findResult in findResults:
                    node = Serialize(**findResult)
                    for p in node.processes:
                        process = Serialize(**p)
                        if process.name == PROCESS_NAME:
                            for c in process.components:
                                component = Serialize(**c)
                                failedComponentInstances.append(component.name)

                # Update ComponentInstances collection using above collected information.
                ciColl = db["ComponentInstances"]
                for compInst in failedComponentInstances:
                    result = ciColl.update({"name":compInst},
                                           {"$set":{"status":"FAULTY"}})

                # Mark component instances as failed in LiveSystem collection as well.
                result = lsColl.update({"name":NODE_NAME, "status":"ACTIVE", "processes":{"$elemMatch":{"name":PROCESS_NAME, "status":"FAULTY"}}},
                                       {"$set":{"processes.$.components.0.status":"FAULTY"}},   # NOTE: This assumes one component per process.
                                       upsert = False)

SOLVER_IP = "127.0.0.1"
SOLVER_PORT = 7778
MY_PORT = 8888

PING = "PING"
PING_RESPONSE_READY = "READY"
PING_RESPONSE_BUSY = "BUSY"
SOLVE = "SOLVE"
SOLVE_RESPONSE_OK = "OK"

def invoke_solver():
    sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((SOLVER_IP, MY_PORT))

    print "Pinging solver for status"

    # First, ping solver and see if its is ready or busy.
    sock.sendto(PING, (SOLVER_IP, SOLVER_PORT))

    print "Waiting for solver response..."
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    print "Solver response message:", data

    # If ready, ask solver to solve.
    if data == PING_RESPONSE_READY:
        print "Requesting solver for solution"
        sock.sendto(SOLVE, (SOLVER_IP, SOLVER_PORT))

    print "Waiting for solver response..."
    data, addr = sock.recvfrom(1024)

    print "Solver response message:", data

def print_usage():
    print "USAGE:"
    print "SimulateNodeActivity --nodeName <node name> [--processName <process name>] --action <'start' | 'stop'>"

if __name__ == '__main__':
    global NODE_NAME
    global PROCESS_NAME
    global START_ACTION
    global STOP_ACTION

    NODE_NAME = ""
    PROCESS_NAME = ""
    START_ACTION = False
    STOP_ACTION = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hnpa",
                                   ["help", "nodeName=", "processName=","action="])
    except getopt.GetoptError:
        print 'Cannot retrieve passed parameters.'
        print_usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-n", "--nodeName"):
            print "Node name:", arg
            NODE_NAME = arg
        elif opt in ("-p", "--processName"):
            print "Process name:", arg
            PROCESS_NAME = arg
        elif opt in ("-s", "--action"):
            print "Action:", arg
            if arg == "start":
                START_ACTION = True
            elif arg == "stop":
                STOP_ACTION = True
            else:
                print_usage()
                sys.exit()

    if (NODE_NAME == ""):
        print_usage()
        sys.exit()

    # Add failure affects to the database.
    execute_action()
    # Invoke solver if action was stop.
    if STOP_ACTION:
        invoke_solver()