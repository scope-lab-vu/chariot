__author__ = "Subhav Pradhan"

import sys, os, signal, subprocess, getopt
import socket, zmq, json
import re
from ResilienceEngine import mongo_connect
from random import randint
from SolverBackend import Serialize
from ResilienceEngine import get_node_address

def execute_start_action(actionProcess, actionStartScript):
    retval = None

    env_str = os.getenv('APP_HOME','/home/vagrant/chariot_apps/')
    actionStartScript = str(actionStartScript)

    cmd = actionStartScript.split(" ")
    cmd[1] = env_str + "/" + cmd[1]

    print "Creating process:", actionProcess, "with START command:", cmd
    proc = subprocess.Popen(cmd)
    print "Command executed, PID:", proc.pid
    retval = proc.pid

    return retval

def execute_stop_action(db, actionNode, actionProcess, actionStopScript):
    if (actionNode == NODE_NAME):
        # Find PID in the database.
        lsColl = db["LiveSystem"]

        nodeDoc = lsColl.find_one({"name":actionNode})
        nodeSerialized = Serialize(**nodeDoc)
        pid = None

        for process in nodeSerialized.processes:
            if process["name"] == actionProcess and process["status"] == "ACTIVE":
                pid = process["pid"]

        # If PID found, kill the process.
        if pid is not None:
            print "Killing process:", actionProcess, "with STOP command: kill -9", pid
            os.kill(pid, signal.SIGKILL)
        else:
            print "PID not found in the database. STOP cannot be performed."

def update_start_action(db, actionNode, actionProcess, startScript, stopScript, pid):
    component = re.sub("process_", "", actionProcess)

    lsColl = db["LiveSystem"]

    # Handle scenario where process to start is already in the right place in LiveSystem collection. This
    # will be true for all cases (initial deployment as well as reconfiguration, via ResilienceEngineMain.py
    # populate_live_system function). So, before updating, make sure status is TO_BE_DEPLOYED. If so, update
    # status to ACTIVE.
    result = lsColl.update({"name":actionNode, "processes":{"$elemMatch":{"name":actionProcess, "status":"TO_BE_DEPLOYED"}}},
                           {"$set": {"processes.$.status": "ACTIVE", "processes.$.pid":pid}},
                           upsert = False)

    # If above update matched, then update the component instance status too.
    if result is not None:
        if result["ok"] > 0:
            lsColl.update({"name":actionNode, "processes":{"$elemMatch":{"name":actionProcess, "components":{"$elemMatch":{"name":component}}}}},
                          {"$set": {"processes.$.components.0.status": "ACTIVE"}},  #WARNING: This assumens, one component/process.
                          upsert = False)

            # Update information in ComponentInstances collection as well.
            ciColl = db["ComponentInstances"]

            result = ciColl.update({"name":component},
                                   {"$set":{"status":"ACTIVE"}},
                                   upsert = False)
    else:
        # If not, it means we need to handle the scenario where process to start is not in the right place in
        # LiveSystem collection. So, a new process document must be created and inserted.
        # NOTE: This (TO_BE_DEPLOYED processes not in right place) should never happen but we keep the code below
        # to handle scenario if it ever does happens.
        processDocument = dict()
        processDocument["name"] = actionProcess
        processDocument["pid"] = pid
        processDocument["status"] = "ACTIVE"
        processDocument["startScript"] = startScript
        processDocument["stopScript"] = stopScript
        processDocument["components"] = list()

        # Find component instance in ComponentInstances collection and fill information below.
        ciColl = db["ComponentInstances"]
        ciDoc = ciColl.find_one({"name":component})

        componentDocument = dict()
        componentDocument["name"] = component
        componentDocument["status"] = "ACTIVE"
        componentDocument["type"] = ciDoc["type"]
        componentDocument["functionalityInstance"] = ciDoc["functionalityInstance"]
        componentDocument["node"] = ciDoc["node"]

        processDocument["components"].append(componentDocument)

        result = lsColl.update({"name":actionNode},
                               {"$push":{"processes":processDocument}},
                               upsert = False)

        # Update information in ComponentInstances collection as well.
        ciColl = db["ComponentInstances"]

        result = ciColl.update({"name":component},
                               {"$set":{"status":"ACTIVE"}},
                               upsert = False)

    # Mark action as taken.
    daColl = db["DeploymentActions"]
    daColl.update({"action":"START", "status":"0_TAKEN", "process":actionProcess, "node": actionNode},
                  {"$set":{"status":"1_TAKEN"}},
                  upsert = False)

def update_stop_action(db, actionNode, actionProcess, startScript, stopScript):
    component = re.sub("process_", "", actionProcess)

    lsColl = db["LiveSystem"]

    result = lsColl.update({"name":actionNode},
                           {"$pull":{"processes":{"name":actionProcess}}})

    # Mark action as taken.
    daColl = db["DeploymentActions"]
    daColl.update({"action":"STOP", "status":"0_TAKEN", "process":actionProcess, "node": actionNode},
                  {"$set":{"status":"1_TAKEN"}},
                  upsert = False)

def handle_action(db, actionDoc):
    actionNode = actionDoc["node"]
    if actionNode == NODE_NAME:
        action = actionDoc["action"]
        actionStatus = actionDoc["status"]
        actionNode = actionDoc["node"]
        actionProcess = actionDoc["process"]
        actionTimeStamp = actionDoc["time"]
        actionStartScript = actionDoc["startScript"]
        actionStopScript = actionDoc["stopScript"]

        if action == "START" and actionStatus == "0_TAKEN":
            print "STARTING process:", actionProcess, "on node:", actionNode
            if not SIMULATE_DM_ACTIONS:
                pid = execute_start_action(actionProcess, actionStartScript)
            else:
                pid = randint(1000, 2000)

            # Update deployment time in Failures collection. To do so, first figure out which node failed.
            # NOTE: This only works for a single failure at a time.
            lsColl = db["LiveSystem"]
            result = lsColl.find({"status":"FAULTY"})

            for r in result:
                failureColl = db["Failures"]
                failureColl.update({"failedEntity": r["name"], "reconfiguredTime":0},
                                   {"$currentDate": {"reconfiguredTime": {"$type": "date"}}},
                                   upsert = False)

            # Update database to reflect affect of above start action.
            update_start_action(db, actionNode, actionProcess, actionStartScript, actionStopScript, pid)
        elif action == "STOP" and actionStatus == "0_TAKEN":
            print "STOPPING process:", actionProcess, "on node:", actionNode
            if not SIMULATE_DM_ACTIONS:
                execute_stop_action(db, actionNode, actionProcess, actionStopScript)

            # Update database to reflect affect of above stop action.
            update_stop_action(db, actionNode, actionProcess, actionStartScript, actionStopScript)

def print_usage():
    print "USAGE:"
    print "DeploymentManager --nodeName <node name> --mongoServer <mongo server address> [--simulateDM]"

def main():
    global SIMULATE_DM_ACTIONS
    global NODE_NAME
    global ZMQ_PORT

    SIMULATE_DM_ACTIONS = False
    NODE_NAME = ""
    ZMQ_PORT = 8000

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hnms",
                                   ["help", "nodeName=", "mongoServer=", "simulateDM"])
    except getopt.GetoptError:
        print "Cannot retrieve passed parameters."
        print_usage()
        sys.exit()

    mongoServer = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-n", "--nodeName"):
            print "Node name:", arg
            NODE_NAME = arg
        elif opt in ("-m", "--mongoServer"):
            print "Mongo server address:", arg
            mongoServer = arg
        elif opt in ("-s", "--simulateDM"):
            print "Simulating DM Actions"
            SIMULATE_DM_ACTIONS = True
        else:
            print "Invalid command line argument."
            print_usage()
            sys.exit()

    # If no node name given then use hostname.
    if NODE_NAME == "":
        NODE_NAME = socket.gethostname()
        print "Using node name:", NODE_NAME

    # If no mongoServer given then use default.
    if (mongoServer is None):
        #mongoServer = "mongo"
        mongoServer = "localhost"
        print "Using mongo server: ", mongoServer

    if SIMULATE_DM_ACTIONS:
        os.environ["SIMULATED_HOSTNAME"] = NODE_NAME

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

    # Creating ZeroMQ context and server socket.
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REP)

    # Get IP and port of host.
    addr, port = get_node_address(db, NODE_NAME)

    # Connect to given (stored in database) or default port.
    if (addr is not None and port is not None):
        print "Using address: ", str(addr), " and port: ", int(port)
        zmq_socket.bind("tcp://%s:%d"%(str(addr), int(port)))
    elif (addr is not None and port is None):
        # If port is none, use default ZMQ_PORT.
        print "Using address: ", str(addr), " and port: ", int(port)
        zmq_socket.bind("tcp://%s:%d"%(str(addr),ZMQ_PORT))

    while True:
        # Receive action, which is a JSON document.
        print "Waiting for deployment action"
        action = zmq_socket.recv()
        zmq_socket.send("Received")
        action_json = json.loads(action)
        print "Received new deployment action: ", action_json["action"], " for process: ", action_json["process"]
        handle_action (db, json.loads(action))

if __name__ == '__main__':
    main()