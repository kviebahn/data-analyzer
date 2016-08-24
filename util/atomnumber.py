'''
Created on 2016-08-22 Mon 16:43 AM
by Matteo
'''

#number of atoms calculation

import library.phys_const as pc
import library.K39_const as K39
import library.Rb87_const as Rb87

import numpy as np

# this calcultes the fraction of light from the MOT centre that impinges on the PD surface, from geometrical contributions of vacuum setup
def Fraction(kneeLens): #distance between viewport and collecting lens
    MOTknee = 502e-3 #m, distance between centre of MOT and end of viewport
    MOTendDPS = 291e-3 #m, distance MOT centre and end of Diff pump section
    CF = 2.5e-3 #m, CF16 internal diameter
    collecting = 25.4e-3 #radius of collecting lens
    focussing = 12.7e-3 #radius of focussing lens
    tangent = CF/MOTendDPS
    distance = MOTknee + kneeLens
    actualradius = distance*tangent #radius subtended by solid angle
    solidangle = 0.25*(actualradius/distance)**2
    lensStuff = (focussing/collecting)**2 #apparently because focussing lens is smaller than collecting lens, there is some light lost, need to multiply by this factor

    return solidangle*lensStuff

def Atomnumber(fluorescence, lock, freqAOM, pdvoltage): # needs fluorescence [V], lock (2->3 crossover) frequency of 3D cooling AOM, and red fibre cluster photodiode
    if lock == 23:
        freqref = 133.5e6
    else:
        print('What are you locking your frequency to?')

    det = freqref - freqAOM
    power = -5.8+13.5*(pdvoltage) # W vs V, from calibration of fibre cluster PD (2016/08/17)
    conversion = 2.92e-6 # W/V conversion for home made photodiodes, measured on 2016/05/05
    waist = 14e-3 #m, double waist of 3D MOT beam is 28 mm
    intensity = 2*power/(np.pi*(waist)**2)
    Ephoton = pc.h*pc.c/Rb87.lD2
    satpar = intensity/Rb87.IsatD2
    scatteringrate = 0.5*2*np.pi*Rb87.gammaD2*(satpar)/(1+satpar+4*(det/(2*np.pi*Rb87.gammaD2))**2)
    fraction = Fraction(15e-3) 
    
    print(scatteringrate)
    print(Rb87.gammaD2)

    return conversion*fluorescence/(scatteringrate*Ephoton*fraction)
    

    
