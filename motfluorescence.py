from analyzer import Analyzer, save_plot
import library.phys_const as pc
import library.K39_const as K39
import library.Rb87_const as Rb87
from util.atomnumber import Atomnumber

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt




def saturated_exponential(x, a, tau, x0):
    return a*(1.-np.exp(-(x-x0)/tau))

def analyze(figure, file):

    # time vs red fibre cluster photodiode
    xx = np.array(file['system.soft.visa.scope/red fibre cluster photodiode/x'])
    yy = np.array(file['system.soft.visa.scope/red fibre cluster photodiode/y'])

    const_value = np.argwhere(xx>0.01)
    coolinglightPD = np.mean(yy[const_value.T[0]])
    check_std = np.std(yy[const_value.T[0]])

    if check_std>0.02:
        raise Exception("Red fibre cluster voltage not constant, cooling light not constant")

    # time vs fluorescence
    x = np.array(file['system.soft.visa.scope/mot fluorescence/x'])
    y = np.array(file['system.soft.visa.scope/mot fluorescence/y']) #Volts
    freq3DcoolAOM = file['parameters/detunings/rb_mot_cooling_aom_freq'][()]

    first_index = np.argwhere(x>0)[0][0]
    y = Atomnumber(y, 23, freq3DcoolAOM, coolinglightPD) #translates fluorescence voltage to number of atoms
     

    values, std_array = curve_fit(saturated_exponential, x[first_index:], y[first_index:], p0 = (1e10, 1., 0.0))

    errs = np.sqrt(np.diag(std_array))
    print values, errs
    loadrate = values[0]/values[1]
    print 'Loading rate = {:.2e} atoms/s'.format(loadrate)
    print 'Max number of atoms = {:.2e} atoms'.format(values[0])

    ax = figure.add_subplot(121)
    ax.plot(x,y, 'r-', label = 'Data')
    mystring = 'f(x) = a*(1-exp(-(x-x0)/tau))\na = %1.4f\ntau = %1.3f \nx0 = %1.2f \nLoading rate = a/tau = %.4f' %(values[0], values[1], values[2], loadrate)
    ax.plot(x, saturated_exponential(x, *values), 'b-', label = mystring)
    ax.set_xlabel('Time/s')
    ax.set_ylabel('Atom number')

    return values[0], loadrate

def plot(fig, data):
    ax = fig.add_subplot(122)
    lns1 = ax.plot(data[0],data[2], 'b-', label='loading rate')
    ax2 = ax.twinx()
    lns2 = ax2.plot(data[0],data[1], 'r-', label='max fluorescence')
    ax.set_ylabel('3D MOT loading rate [atoms/s]')
    ax2.set_ylabel('3D MOT atom number')
    ax.set_xlabel('3D cooling freq [MHz]')
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

a = Analyzer(analyze, plot, save_plot('fluorescence.png'))
a.run()
