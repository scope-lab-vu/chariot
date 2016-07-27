import getopt, sys
import socket

def invoke_management_engine(serverAddress):
    serverPort = 7000

    # Find own IP.
    myIP = "localhost"                      # Temporarily set to localhost.
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
    sock.sendto(PING, (serverAddress, serverPort))

    print "Waiting for response..."
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    print "Response message:", data

    # If ready, ask solver to solve.
    if data == PING_RESPONSE_READY:
        print "Requesting for solution"
        sock.sendto(SOLVE, (serverAddress, serverPort))

    print "Waiting for response..."
    data, addr = sock.recvfrom(1024)

    print "Response message:", data

def print_usage():
    print "USAGE:"
    print "InvokeManagementEngine --managementEngine <management engine address>"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm",
                                    ["help", "managementEngine="])
    except getopt.GetoptError:
        print "Cannot retrieve passed parameters."
        print_usage()
        sys.exit()

    managementEngine = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-m", "--managementEngine"):
            print "Management engine address:", arg
            managementEngine = arg
        else:
            print "Invalid command line argument."
            print_usage()
            sys.exit()

    if managementEngine is None:
        managementEngine = "localhost"
        print "Using monitoring server: ", managementEngine

    invoke_management_engine(managementEngine)
if __name__ == '__main__':
    main()