import pyupm_i2clcd as lcd
import zmq
from random import randint

# LCD.
lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)

# ZMQ Port.
ZMQ_PORT = 5556

# ZMQ subscriber socket.
zmq_context = zmq.Context()
sub_socket = zmq_context.socket(zmq.SUB)

sub_socket.connect("tcp://192.168.1.9:%d"%ZMQ_PORT)
sub_socket.connect("tcp://192.168.1.10:%d"%ZMQ_PORT)
sub_socket.connect("tcp://192.168.1.8:%d"%ZMQ_PORT)
sub_socket.connect("tcp://192.168.1.4:%d"%ZMQ_PORT)
sub_socket.connect("tcp://192.168.1.7:%d"%ZMQ_PORT)
sub_socket.connect("tcp://192.168.1.3:%d"%ZMQ_PORT)

sub_socket.setsockopt(zmq.SUBSCRIBE,"")

lcdDisplay.setColor(randint(0,255),randint(0,255),randint(0,255))
lcdDisplay.setCursor(0,0)
lcdDisplay.write("Message count: 0")

message_count = 0

while 1:
        msg = sub_socket.recv()
        tokens = msg.split(',')
        if tokens[1] == "Hello":
                message_count += 1

                lcdDisplay.setCursor(0,0)
                lcdDisplay.write("Message count: %d"%message_count)

                if message_count == 10:
                        message_count = 0
                        lcdDisplay.setColor(randint(0,255),randint(0,255),randint(0,255))
                        lcdDisplay.setCursor(0,0)
                        lcdDisplay.write("Message count: 0")
