from analyzer import Analyzer, save_plot

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

fig2 = plt.figure()

def saturated_exponential(x, a, tau, x0):
    return a*(1.-np.exp(-(x-x0)/tau))

def analyze(file):
    x = np.array(file['system.soft.visa.scope/mot fluorescence/x'])
    y = np.array(file['system.soft.visa.scope/mot fluorescence/y'])

    first_index = np.argwhere(x>0)[0][0]
    values, std_array = curve_fit(saturated_exponential, x[first_index:], y[first_index:], p0 = (0.04, 1., 0.0))

    errs = np.sqrt(np.diag(std_array))
    print values, errs
    loadrate = values[0]/values[1]
    print 'Loading rate = %.4f' %(loadrate)

    fig2.clear()
    ax = fig2.add_subplot(111)
    ax.plot(x,y, 'r-', label = 'Data')
    mystring = 'f(x) = a*(1-exp(-(x-x0)/tau))\na = %1.4f\ntau = %1.3f \nx0 = %1.2f \nLoading rate = a/tau = %.4f' %(values[0], values[1], values[2], loadrate)
    ax.plot(x, saturated_exponential(x, *values), 'b-', label = mystring)
    ax.set_xlabel('Time/s')
    ax.set_ylabel('Fluorescence/V')

    return values[0], loadrate

def plot(fig, data):
    ax = fig.add_subplot(111)
    lns1 = ax.plot(data[0],data[2], 'b-', label='loading rate')
    ax2 = ax.twinx()
    lns2 = ax2.plot(data[0],data[1], 'r-', label='max fluorescence')
    ax.set_ylabel('3D MOT fluorescence loading rate [V/s]')
    ax2.set_ylabel('3D MOT fluorescence [V]')
    ax.set_xlabel('3D MOT current [A]')
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

a = Analyzer(analyze, plot, save_plot('fluorescence.png'))
a.run()
