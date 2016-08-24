'''
Created on 2016-08-22 Mon 16:43 AM
by Matteo
'''

from math import pi
import phys_const as pc

# atomic mass (kg)
m = 86.90918052*pc.u

'optical properties'
'D2: 4S1/2 <-> 5P3/2'

#frequency (Hz)
omegaD2 = 2.*pi*384.2304844685e12
nuD2 = omegaD2/2./pi

#wavelength (m)
lD2 = pc.c/nuD2

#lifetime (s)
tauD2 = 26.24e-9

#linewidth (Hz*2*pi)
gammaD2 = 6.065e6

#recoil velocity (m/s)
vrecD2 = 5.8845e-3

#recoil temperature (K)
TrecD2 = 361.96e-9

#Doppler temperature (K)
TdoppD2 = 146e-6

#saturation intensity
IsatD2 = pi*pc.h*pc.c/(3.*lD2**3*tauD2)
