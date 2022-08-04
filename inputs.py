import engines as en
from numpy import pi
import numpy as np
# Dados atmosféricos -------------------------------------------------------------------------------------------------
Tac     = -4.83+273.15                  # K     (Temperatura de cruzeiro)
Tad     = 15   +273.15                  # K     (Temperatura de decolagem)
Pac     = 69.658015                     # kPa   (Pressão atm de cruzeiro)
Pad     = 101.13500                     # kPa   (Pressão atm de decolagem)
cpc     = 1003.25                       # J/kg  (cp cruzeiro)
cpd     = 1004.08                       # J/kg  (cp decolagem)
R       = 287.05                        # J/kgK (constante dos gases para o ar)
k       = 1.4 
g       = 9.81                          # m/s²  (aceleração da gravidade)
rhod    = Pad*1e3/(R*Tad)
rhoc    = Pac*1e3/(R*Tac)


# Dados construtivos gerais ------------------------------------------------------------------------------------------
M0      = 0.85 
PCI     = 43e6                          # J/kg K
T04     = 1300                          # K

# Dados construtivos TurboJato ----------------------------------------------------------------------------------------
m0j     = 77    # kg/s
picj    = 13.33
mmjato  = 121   # kg

# Dados construtivos TurboFan -----------------------------------------------------------------------------------------
B       = 5.00
picf    = 30.00                         #
pifan   = 1.65
Afan    = pi*(2.39**2)/4                # m
m0f     = en.f_m0(Pac, Afan, M0, Tac)   # kg/s
mmfan   = 4273                          # kg

# Dados da missão    -------------------------------------------------------------------------------------------------
Pacru   = 18.7                          # kPa
Tacru   = -55 +273.15                   # kPa
rhocru  = Pac*1e3/(R*Tac)               # kg/m³
memp    = 70550                         # kg
mmax    = 10e4                          # kg
A       = 5700                          # km
hc      = 12                            # km  
Sgmax   = 2000                          # m
ucru    = M0*np.sqrt(k*R*Tacru)         # m/s
usub    = 600/3.6                       # m/s
udesc   = 500/3.6                       # m/s

Clmax   = 2.1
Cd      = lambda Cl: 0.0181 + 0.0362*Cl**2
Aw      = 116.3                         # m2
neng    =  2

rhofuel = 0.81                          # kg/l

pi_text = [( 'pii= ',  'piLPC= ',  'piHPC= ',  'pib= ',  'piHPT= ',  'piLPT= ',  'piNS= ',  'piNP= ')]
tau_text= [('taui= ', 'tauLPC= ', 'tauHPC= ', 'taub= ', 'tauHPT= ', 'tauLPT= ', 'tauNS= ', 'tauNP= ')]