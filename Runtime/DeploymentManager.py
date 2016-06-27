__author__ = "Subhav Pradhan"

from pymongo import MongoClient
from time import sleep
import pymongo
import json
import sys
import getopt
import socket
import os
from pymongo import CursorType
from pymongo.errors import AutoReconnect
import subprocess
import time
import signal

class Serialize:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def execute_start_action(actionNode, actionProcess, actionStartScript):
    retval = -1

    env_str = os.getenv('APP_HOME','/home/vagrant/chariot_apps/')
    actionStartScript = str(actionStartScript)
    
    cmd = actionStartScript.split(" ")
    cmd[1] = env_str + "/" + cmd[1]
    
    #print "Creating process:", actionProcess, "with START command:", actionStartScript
    proc = subprocess.Popen(cmd)
    print "Command executed, PID:", proc.pid
    retval = proc.pid

    return retval

def execute_stop_action(actionNode, actionProcess, actionStopScript):
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
    import re
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
    # TODO: Check if component instance status needs to be updated in the ComponentInstances collection too.
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
        componentDocument["mode"] = ciDoc["mode"]
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

def update_stop_action(db, actionNode, actionProcess, startScript, stopScript):
    import re
    component = re.sub("process_", "", actionProcess)

    lsColl = db["LiveSystem"]

    result = lsColl.update({"name":actionNode},
                           {"$pull":{"processes":{"name":actionProcess}}})

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
                pid = execute_start_action(actionNode, actionProcess, actionStartScript)
            else:
                from random import randint
                pid = randint(1000, 2000)

            # Update deployment time in Failures collection. To do so, first figure out which node failed.
            # NOTE: This only works for a single failure at a time as we only expect to find one failed node
            #       when querying the database.
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
            #print "STOPPING process:", actionProcess, "on node:", actionNode
            if not SIMULATE_DM_ACTIONS:
                execute_stop_action(actionNode, actionProcess, actionStopScript)

            # Update database to reflect affect of above stop action.
            update_stop_action(db, actionNode, actionProcess, actionStartScript, actionStopScript)

def print_usage():
    print "USAGE:"
    print "DeploymentManager --nodeName <node name> [--simulateDM]"

if __name__ == '__main__':
    global SIMULATE_DM_ACTIONS
    global NODE_NAME
    global SLEEP

    SIMULATE_DM_ACTIONS = False
    NODE_NAME = ""
    SLEEP = 10

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hns",
                                   ["help", "nodeName=", "simulateDM"])
    except getopt.GetoptError:
        print 'Cannot retrieve passed parameters.'
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-n", "--nodeName"):
            print "Node name:", arg
            NODE_NAME = arg
        elif opt in ("-s", "--simulateDM"):
            print "Simulating DM Actions"
            SIMULATE_DM_ACTIONS = True

    if NODE_NAME == "":
        NODE_NAME = socket.gethostname()
        print "Using node name:", NODE_NAME

    if SIMULATE_DM_ACTIONS:
        os.environ["SIMULATED_HOSTNAME"] = NODE_NAME

    client = MongoClient("localhost", 27017)
    oplog = client.local.oplog.rs
    first = oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
    ts = first['ts']

    while True:
        # query = {'ts': {'$gt': some_timestamp}}  # Replace with your own query.
        cursor = oplog.find({'ts': {'$gt': ts}}, cursor_type=CursorType.TAILABLE_AWAIT)
        print 'created cursor'
        cursor.add_option(8)
        # cursor.add_option(_QUERY_OPTIONS['oplog_replay'])

        try:
            while cursor.alive:
                try:
                    for doc in cursor:
                        if doc['op'] == 'i':
                            filename = 'nodeMonitoringDocuments/'+doc['ns']
                            if not os.path.exists(os.path.dirname(filename)):
                                os.makedirs(os.path.dirname(filename))
                            with open(filename, "a") as f:
                                fullname = doc['ns'].split('.')
                                if len(fullname) < 2:
                                    print 'invalid db/collection name'
                                    continue
                                if fullname[0] !="ConfigSpace" or fullname[1]!="DeploymentActions":
                                    continue

                                # Deployment action insert detected. Simulate if required.
                                #master_client = MongoClient("master", 27017)
                                master_client = MongoClient("localhost", 27017)
                                db = master_client[fullname[0]]
                                collection = db[fullname[1]]

                                deploymentActionDoc = collection.find_one({'_id': doc['o']['_id']})
                                handle_action (db, deploymentActionDoc)

                                #tosave = mcollection.find_one({'_id': doc['o']['_id']})
                                #print tosave
                                #jsonstring = json.dumps(str(tosave))

                                # print doc

                except (AutoReconnect, StopIteration):
                    print 'exception triggered'
                    sleep(SLEEP)

        finally:
            cursor.close()
