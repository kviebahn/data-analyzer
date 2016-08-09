# -*- coding: utf-8 -*-

import socket
from Pyro.EventService.Clients import Subscriber
import Pyro.core
import os.path
import h5py
import numpy as np
import Queue
from threading import Thread
import matplotlib.pyplot as plt

# enable interactive plots
plt.ion()

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
    def __init__(self, queue):
        Subscriber.__init__(self)
        self.subscribe('hdfDone')
        self.subscribe('iterationStatus')
        self.subscribe('Status')
        self._queue = queue
        print('listening for events')

    def event(self, event):
        # ignore all timing events, they will just flood the queue
        if event.subject == 'Status' and event.msg[0][0] == 'Time':
            return
        self._queue.put(event)

class Analyzer():
    def __init__(self, analyze, plot = None, save = None):
        self._iterationDone = False
        self._analyze = analyze
        self._plot = plot
        self._fig = plt.figure()
        self._save = save
        self._data = []
        self._counter = 0
        self._queue = Queue.Queue()
        self._listener = Listener(self._queue)
        self._thread = Thread(target=Listener.listen, args = (self._listener,))
        self._thread.start()

    def run(self):
        while True:
            try:
                e = self._queue.get_nowait()
                self.event(e)
            except Queue.Empty:
                plt.pause(0.01)

    def _full_analyze(self, f):
        # get iterator if in looped mode
        I = f.get('parameters/I', np.array(None))[()]
        if I:
            x = I
        else:
            x = self._counter
            self._counter += 1

        return (x,) + self._analyze(f)

    def event(self, event):
        if event.subject == 'hdfDone':
            datapath = os.path.normpath(os.path.join(*event.msg[0]))
            with h5py.File(datapath, 'r') as f:
                data = np.array([self._full_analyze(f)]).T
                if self._data == []:
                    self._data = data
                else:
                    self._data = np.concatenate((self._data, data), axis=1)

                if self._plot:
                    self._fig.clear()
                    self._plot(self._fig, self._data)

                if self._iterationDone:
                    if self._save:
                        self._save(self._data, self._folder)
                    self._iterationDone = False
                    self._data = []

        elif event.subject == 'iterationStatus':
            if event.msg[0]['status'] == 'started':
                self._folder = os.path.normpath(event.msg[0]['folder'])
            if event.msg[0]['status'] == 'stopped':
                self._iterationDone = True
        else:
            if event.msg[0][0] == 'processStarted':
                self._data = []
                self._counter = 0

def save_plot(name):
    return lambda data,folder: plt.savefig(os.path.join(folder, name))

def analyze(file):
    # analyze the data and return one or multiple datapoints
    return 1

def plot(fig, data):
    # do something with the data we have so far. Data is a 2D numpy array
    # with data[0] == x, data[1] == y1 , etc.
    pass

def save(data, path):
    # save the data which finishes a sequence. Data is all data accumulated
    # during the sequence, path is the folder in which the sequence files
    # are stored
    pass

if __name__ == '__main__':
    a = Analyzer(analyze, plot, save)
    a.run()
