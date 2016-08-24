# -*- coding: utf-8 -*-
import h5py
import os
import numpy as np
import matplotlib.pyplot as plt
import listener
from scipy.optimize import curve_fit

from datetime import date, timedelta

def saturated_exponential(x, a, tau, x0):
    return a*(1.-np.exp(-(x-x0)/tau))

def analyze(file, datapath):
    
    # get iterator if in looped mode
    I = file.get('parameters/I', np.array(None))[()]
    print I
    
    x = np.array(file['system.soft.visa.scope/mot fluorescence/x'])
    y = np.array(file['system.soft.visa.scope/mot fluorescence/y'])

    first_index = np.argwhere(x>0)[0][0]
    values, std_array = curve_fit(saturated_exponential, x[first_index:], y[first_index:], p0 = (0.04, 1., 0.0))
    
    errs = np.sqrt(np.diag(std_array))
    print values, errs
    loadrate = values[0]/values[1]
    print 'Loading rate = %.4f' %(loadrate)
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    ax.plot(x,y, 'r-', label = 'Data')
#    mystring = 'f(x) = a*(1-exp(-(x-x0)/tau))\na = %1.4f\ntau = %1.3f \nx0 = %1.2f \nLoading rate = a/tau = %.4f' %(values[0], values[1], values[2], loadrate)
#    ax.plot(x, saturated_exponential(x, *values), 'b-', label = mystring)
#    ax.set_xlabel('Time/s')
#    ax.set_ylabel('Fluorescence/V')
#    plt.legend(loc = 0)

#    plt.savefig(os.path.splitext(datapath)[0] + '.png')
    return I, loadrate

def readhdf5(datapath):
    with h5py.File(datapath, 'r') as f:
        return analyze(f, datapath)

def getdatapath(datadir, day = date.today()):
    # shared path
    shared_path = os.path.normpath(os.path.join('Z:\Shared',day.strftime('%Y/%m/%d'),datadir))
    # get all the files in one directory
    files = os.listdir(shared_path)
    # join the datapath to each filepath
    return [os.path.join(shared_path, file) for file in files]

def reading(filelist):
    datalist = []
    for file in filelist:
        datalist.append(readhdf5(file))
    return np.array(datalist)
        
    
#ls = listener.Listener(analyze)
#ls.listen()
