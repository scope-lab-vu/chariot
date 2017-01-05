__author__ = "Subhav Pradhan"

import pymongo
import socket
import logging
import os

# Basic serialize class to convert a mongo document into a dictionary.
class Serialize:
    def __init__(self, **entries):
        self.__dict__.update(entries)

# Helper to create and return python logger. This uses environment variable CHARIOT_LOG_LEVEL to determine base log level.
def get_logger(name):
    logger = logging.getLogger(name)
    
    # Get base log level from environment variable.
    try:
        logLevel = os.environ["CHARIOT_LOG_LEVEL"]
    except KeyError:
        # If environment variable not set, use INFO as base.
        logLevel = "INFO" 
    
    if (logLevel == "DEBUG"):
        logger.setLevel(logging.DEBUG)
    elif (logLevel == "WARNING"):
        logger.setLevel(logging.WARNING)
    elif (logLevel == "ERROR"):
        logger.setLevel(logging.ERROR)
    elif (logLevel == "CRITICAL"):
        logger.setLevel(logging.CRITICAL)
    else:
        # If none of the above four is used as base log level,
        # then assume INFO.
        logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)

    return logger

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
        if (seperatorIndex != -1):
            ip = address[:(seperatorIndex)]
            port = address[(seperatorIndex+1):]
        else:
            ip = address
            port = None
        return ip, port
    else:
        return None, None

# Helper for mongo connection.
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

def invoke_management_engine(mongoServer, managementEngine, isUpdate):
    # Add appropriate reconfiguration event.
    client = pymongo.MongoClient(mongoServer)
    db = client["ConfigSpace"]
    reColl = db["ReconfigurationEvents"]

    if isUpdate:
        # NOTE: Using update as we need to use currentDate which
        # is an update operator.
        reColl.update({"completed":False},
                        {"$currentDate":{"detectionTime":{"$type":"date"}},
                         "$set": {"kind":"UPDATE",
                                  "solutionFoundTime":0,
                                  "reconfiguredTime":0,
                                  "actionCount":0}},
                         upsert = True)
    else:
        # NOTE: Using update as we need to use currentDate which
        # is an update operator.
        reColl.update({"completed":False},
                      {"$currentDate":{"detectionTime":{"$type":"date"}},
                       "$set": {"kind":"FAILURE",
                                "solutionFoundTime":0,
                                "reconfiguredTime":0,
                                "actionCount":0}},
                       upsert = True)

    print "Invoking solver!"

    managementEnginePort = 7000

    # Find own IP.
    if managementEngine == "localhost":
        myIP = "localhost"
    else:
        myIP = socket.gethostbyname(socket.gethostname())

    myPort = 8888

    PING = "PING"
    PING_RESPONSE_READY = "READY"
    PING_RESPONSE_BUSY = "BUSY"
    SOLVE = "SOLVE"
    SOLVE_RESPONSE_OK = "OK"

    sock = socket.socket(socket.AF_INET,    # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((myIP, myPort))

    print "Pinging management engine for status"

    # First, ping server and see if its is ready or busy.
    sock.sendto(PING, (managementEngine, managementEnginePort))

    print "Waiting for response..."
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    print "Response message:", data

    # If ready, ask solver to solve.
    if data == PING_RESPONSE_READY:
        print "Requesting for solution"
        sock.sendto(SOLVE, (managementEngine, managementEnginePort))

    print "Waiting for response..."
    data, addr = sock.recvfrom(1024)

    print "Response message:", data
