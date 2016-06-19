import mraa
import time
import zmq
import socket

# Host name.
HOST_NAME = socket.gethostname()

# Default message.
MESSAGE = "Hello"

# ZMQ topic name.
TOPIC_NAME = "SimpleDemoMessage"

# ZMQ port.
PUB_PORT = 5556

# ZMQ publisher socket.
zmq_context = zmq.Context()
pub_socket = zmq_context.socket(zmq.PUB)
pub_socket.bind("tcp://*:%d"%PUB_PORT)

# LED pin.
led = mraa.Gpio(13)
led.dir(mraa.DIR_OUT)

while 1:
        message = '{0},{1}'.format(HOST_NAME,MESSAGE)
        pub_socket.send(message)
        led.write(1)
        time.sleep(1)
        led.write(0)
        time.sleep(2)
