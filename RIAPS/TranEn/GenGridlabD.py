# import riaps
from riaps.run.comp import Component
import logging
import os
import re
import zmq
import time
import urllib.request

class GenGridlabD(Component):
    def __init__(self):
        super(GenGridlabD, self).__init__()
        
    def on_periodic(self):
        now = self.clock.recv_pyobj()                # Receive time (as float)
        self.logger.info('on_periodic():%s',now)
        period = self.clock.getPeriod()              # Query the period
        if period == 5.0:
            period = period - 1.0
            self.periodic.setPeriod(period)             # Set the period
            self.logger.info('setting period to %f',period)
        msg = now
        self.ticker.send_pyobj(msg)