'''
Created on 2014-11-06 Thu 10:56 AM
by Konrad
'''

from math import pi
import phys_const as pc

# atomic mass (kg)
m = 38.96370668*pc.u

'optical properties'
'D2: 4S1/2 <-> 5P3/2'

#frequency (Hz)
omegaD2 = 2.*pi*391.01617003e12
nuD2 = omegaD2/2./pi

#wavelength (m)
lD2 = pc.c/nuD2

#lifetime (s)
tauD2 = 26.37e-9

#linewidth (Hz*2*pi)
gammaD2 = 6.035e6

#recoil velocity (m/s)
vrecD2 = 1.335736144e-2

#recoil temperature (K)
TrecD2 = 0.41805837e-6

#Doppler temperature (K)
TdoppD2 = 145e-6

#saturation intensity
IsatD2 = pi*pc.h*pc.c/(3.*lD2**3*tauD2)
