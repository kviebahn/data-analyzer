# -*- coding: utf-8 -*-
'''This script offers subscribing/listening functionality but it already also includes some plotting. The method 'analyze' should be overriden by the user.'''


import socket
from Pyro.EventService.Clients import Subscriber
import Pyro.core
import os.path
import h5py
import numpy as np
import Queue
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

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

# Set up ethernet connection between this script and the timing PC
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
        print('analyzer: listening for events')

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
                plt.pause(0.001)

    def _full_analyze(self, f):
        # get iterator if in looped mode
        I = f.get('parameters/I', np.array(None))[()]
        if I:
            x = I
        else:
            x = self._counter
            self._counter += 1

        return (x,) + self._analyze(self._fig, f)

    def cleardata(self,event):
        self._data = []
        self._counter = 0

    def event(self, event):
        try:
            if event.subject == 'hdfDone':
                datapath = os.path.normpath(os.path.join(*event.msg[0]))
                with h5py.File(datapath, 'r') as f:
                    #clear figure before each data point arrives
                    self._fig.clear()
                    plt.subplots_adjust(bottom=0.15)

                    # get the (new) data
                    data = np.array([self._full_analyze(f)]).T
                    if self._data == []:
                        self._data = data
                    else:
                        self._data = np.concatenate((self._data, data), axis=1)

                    if self._plot:
                        self._plot(self._fig, self._data)

                        # if not in looped mode, clear data of single shots
                        
                        buttonax = plt.axes([0.88, 0.01, 0.1, 0.075])
                        self.mybutton = Button(buttonax, 'Clear')
                        self.mybutton.on_clicked(self.cleardata)

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
        except Exception as e:
            print(e)
        #else:
        #    if event.msg[0][0] == 'processStarted':
        #        self._data = []
        #        self._counter = 0

def save_plot(name):
    return lambda data,folder: plt.savefig(os.path.join(folder, name))

def analyze(figure, file):
    # analyze the data and return one or multiple datapoints
    # the figure that is passed here is for the current run
    # the file that is passed is the hdf5 data file.
    print(file.filename)
    return 1

def plot(fig, data):
    # do something with the cummulative data we have so far. Data is a 2D numpy array
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
