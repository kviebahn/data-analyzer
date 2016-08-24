"""general physical constants"""

from math import pi

h   = 6.6260693e-34                #Plancks constant   (Js)

hbar= 6.6260693e-34 / 2.0 / pi      #Plancks constant / 2pi   (Js)
 
c   = 2.99792458e8                 #speed of light (m/s)

eps0= 8.854187817e-12              #dieelectric constant of vacuum  (A s/V)

R   = 8.314472                     # ideal gas constant (J/mol/K)

kB  = 1.3806505e-23                #Boltzmann constant   (J/K)

Ce  = 1.60217653e-19               #electron charge   (C)

aB  = 5.291772108e-11              #Bohr Radius (m)

g0  = 9.81                         # local gravity  (m/s^2)

me  = 9.10938188e-31               # electron mass (kg)

muB = Ce * hbar/2/me*1e-4         #Bohr magneton (J/G)

gS  = 2.0023193043622              #electron g - Factor   

gN  = 3.82608545              #neutron g - Factor

gP  = 5.585694713              #proton g - Factor

gmu  = 2.0023318414              #muon g - Factor

mu0 = 4. * pi * 1e-7               # vaccum permeability (Vs/Am)      

NA  = 6.0221415e23                   # Avogadro number 1/mol

u = 1.660538921e-27               # atomic mass unit (kg)

alpha = 1./137.035999074        # fine structure constant
