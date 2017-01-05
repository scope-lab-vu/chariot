__author__ = "Subhav Pradhan"

import os, signal, subprocess
import re
from random import randint
from chariot_helpers import Serialize
from logger import get_logger

logger = get_logger("deployment_manager")

def execute_start_action(actionProcess, actionStartScript):
    retval = None

    env_str = os.getenv('APP_HOME','/home/vagrant/chariot_apps/')
    actionStartScript = str(actionStartScript)

    cmd = actionStartScript.split(" ")
    cmd[1] = env_str + "/" + cmd[1]

    logger.info ("Creating process: " + actionProcess + " with START command: " + cmd)
    proc = subprocess.Popen(cmd)
    logger.info ("Command executed, PID: " + proc.pid)
    retval = proc.pid

    return retval

def execute_stop_action(db, actionNode, actionProcess, actionStopScript):
    if (actionNode == NODE_NAME):
        # Find PID in the database.
        nColl = db["Nodes"]

        nodeDoc = nColl.find_one({"name":actionNode})
        nodeSerialized = Serialize(**nodeDoc)
        pid = None

        for process in nodeSerialized.processes:
            if process["name"] == actionProcess and process["status"] == "ACTIVE":
                pid = process["pid"]

        # If PID found, kill the process.
        if pid is not None:
            logger.info ("Killing process: " + actionProcess + " with STOP command: kill -9 " + pid)
            os.kill(pid, signal.SIGKILL)
        else:
            logger.info ("PID not found in the database. STOP cannot be performed.")

def update_start_action(db, actionNode, actionProcess, startScript, stopScript, pid):
    component = re.sub("process_", "", actionProcess)

    # Find process with correct (TO_BE_DEPLOYED) status.
    nColl = db["Nodes"]
    findResult = nColl.find({"name":actionNode, "processes":{"$elemMatch":{"name":actionProcess, "status":"TO_BE_DEPLOYED"}}})

    # If found, update process status to ACTIVE and update component instance information too.
    if findResult.count() != 0:
        nColl.update({"name":actionNode, "processes":{"$elemMatch":{"name":actionProcess, "status":"TO_BE_DEPLOYED"}}},
                     {"$set": {"processes.$.status": "ACTIVE", "processes.$.pid":pid}})

        nColl.update({"name":actionNode, "processes":{"$elemMatch":{"name":actionProcess, "components":{"$elemMatch":{"name":component}}}}},
                     {"$set": {"processes.$.components.0.status": "ACTIVE"}})  #WARNING: This assumens, one component/process.

        # Update information in ComponentInstances collection as well.
        ciColl = db["ComponentInstances"]

        ciColl.update({"name":component},
                      {"$set":{"status":"ACTIVE"}})

        # Mark action as taken.
        daColl = db["DeploymentActions"]
        daColl.update({"action":"START", "completed":False, "process":actionProcess, "node": actionNode},
                      {"$set":{"completed":True}})
    else:
        logger.info ("Process: " + actionProcess + " with status TO_BE_DEPLOYED, not found in node: " + actionNode)

def update_stop_action(db, actionNode, actionProcess, startScript, stopScript):
    component = re.sub("process_", "", actionProcess)

    nColl = db["Nodes"]

    result = nColl.update({"name":actionNode},
                           {"$pull":{"processes":{"name":actionProcess}}})

    # Mark action as taken.
    daColl = db["DeploymentActions"]
    daColl.update({"action":"STOP", "complete":False, "process":actionProcess, "node": actionNode},
                  {"$set":{"completed":True}})

def handle_action(db, actionDoc, simulateDMActions, nodeName):
    # Using parameters to set appropriate global variables.
    global NODE_NAME
    global SIMULATE_DM_ACTIONS

    NODE_NAME = nodeName
    SIMULATE_DM_ACTIONS = simulateDMActions

    actionNode = actionDoc["node"]
    if actionNode == NODE_NAME:
        action = actionDoc["action"]
        actionCompleted = actionDoc["completed"]
        actionNode = actionDoc["node"]
        actionProcess = actionDoc["process"]
        actionStartScript = actionDoc["startScript"]
        actionStopScript = actionDoc["stopScript"]

        if action == "START" and not actionCompleted:
            logger.info ("STARTING process: " + actionProcess + " on node: " + actionNode)
            if not SIMULATE_DM_ACTIONS:
                pid = execute_start_action(actionProcess, actionStartScript)
            else:
                pid = randint(1000, 2000)

            # Update deployment time in ReconfigurationEvents collection.
            reColl = db["ReconfigurationEvents"]
            reColl.update({"completed":False},
                          {"$currentDate": {"reconfiguredTime": {"$type": "date"}},
                          "$inc":{"actionCount":-1}})

            # If after above update, the actionCount field of a ReconfigurationEvent is 0, mark that
            # reconfigurationEvent as completed.
            reColl.update({"completed":False, "actionCount":0},
                          {"$set":{"completed":True}})

            # Update database to reflect affect of above start action.
            update_start_action(db, actionNode, actionProcess, actionStartScript, actionStopScript, pid)
        elif action == "STOP" and not actionCompleted:
            logger.info ("STOPPING process: " + actionProcess + " on node: " + actionNode)
            if not SIMULATE_DM_ACTIONS:
                execute_stop_action(db, actionNode, actionProcess, actionStopScript)

            # Update database to reflect affect of above stop action.
            update_stop_action(db, actionNode, actionProcess, actionStartScript, actionStopScript)
