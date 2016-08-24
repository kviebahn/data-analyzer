# -*- coding: utf-8 -*-
'''This script offers basic 'listening' functionality for the Event 'hdfDon' which occurs at the end of each sequence run.
The method 'analyze' is overriden by the user, eg. in analyzer.py'''

import socket
from Pyro.EventService.Clients import Subscriber
import Pyro.core
import os.path
import h5py

def getHostIP():
    """return the host ip of the computer"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        myip = s.getsockname()[0]
        s.close()
    except:
        myip = socket.gethostbyname(socket.gethostname())
        print "failed to get ip by connecting to external server. using %s"%myip
    return myip

Pyro.config.PYRO_HOST = getHostIP()
Pyro.config.PYRO_NS_HOSTNAME = '172.31.10.10'
Pyro.core.initClient()

class Listener(Subscriber):
    def __init__(self, function):
        Subscriber.__init__(self)
        self.subscribe('hdfDone')
        #self.subscribe('Status')
        self._function = function
        print('listening for events')

    def event(self, event):
        if event.msg[0][0] == 'Time':
            return
        print(event.subject)
        print(event.msg)
        return
        datapath = os.path.normpath(os.path.join(*event.msg[0]))
        with h5py.File(datapath, 'r') as f:
            self._function(f, datapath)

def analyze(file, datapath):
    print(file)

if __name__ == '__main__':
    ls = Listener(analyze)
    ls.listen()
