__author__="Subhav Pradhan"

from pymongo import MongoClient
import getopt, sys
import socket

def invoke_management_engine(mongoServer, managementEngine, isUpdate):
    # Add appropriate reconfiguration event.
    client = MongoClient(mongoServer)
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
    #myIP = socket.gethostbyname(socket.gethostname())
    myIP = "localhost"
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

def print_usage():
    print "USAGE:"
    print "InvokeManagementEngine --mongoServer <mongo server address> --managementEngine <management engine address>"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdm",
                                    ["help", "mongoServer=", "managementEngine="])
    except getopt.GetoptError:
        print "Cannot retrieve passed parameters."
        print_usage()
        sys.exit()

    mongoServer = None
    managementEngine = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-d", "--mongoServer"):
            print "Mongo server address:", arg
            mongoServer = arg
        elif opt in ("-m", "--managementEngine"):
            print "Management engine address:", arg
            managementEngine = arg
        else:
            print "Invalid command line argument."
            print_usage()
            sys.exit()

    if mongoServer is None:
        mongoServer = "localhost"
        print "Using mongo server: ", mongoServer
    
    if managementEngine is None:
        managementEngine = "localhost"
        print "Using monitoring server: ", managementEngine

    invoke_management_engine(mongoServer, managementEngine, True)
if __name__ == '__main__':
    main()
