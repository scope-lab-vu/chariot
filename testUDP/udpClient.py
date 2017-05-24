import socket
import sys

#Create a UDP socket
sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address=('192.168.0.108', 7000)
message='This is the message. It will be repeated'

try:
    #send data
    print >> sys.stderr, 'sending "%s"' %message
    sent = sock.sendto(message,server_address)

    #receive message
    print >> sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print >> sys.stderr, 'received "%s"' %data

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()
