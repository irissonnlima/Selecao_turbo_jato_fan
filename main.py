import matplotlib.pyplot as plt
import engines as en
from inputs import *
import numpy as np

"""
                                        TURBOJATO
"""
#%%
#                                       PARTE I
#%% Decolagem -------------------------------------------------------------------------------------------------
pid, taud, Fnd, TSFCd,fd = en.turbojato(PCI, m0/(B+1), pic, T04, Pad, Tad, 0,cp = cpd)
print('\nDados TurboJato na decolagem')
print(f'Fn\t= {Fnd/1000} [kN]')
print(f'TSFC\t= {TSFCd} [kg/N.h]')

#%% Cruzeiro -------------------------------------------------------------------------------------------------
pi, tau,Fn,TSFC,f = en.turbojato(PCI, m0/(B+1), pic, T04, Pac, Tac, M0, cp = cpc)
print('\nDados TurboJato em cruzeiro')
print(f'Fn\t= {Fn/1000} [kN]')
print(f'TSFC\t= {TSFC} [kg/N.h]')

#%%
#                                       PARTE II
#%% Decolagem - Take off -------------------------------------------------------------------------------------------------

Vstall  = np.sqrt(Wmax*R*Tad/(0.5*Pad*1000*Clmax*Aw))
Vlo     = 1.2*Vstall 
a0      = np.sqrt(k*R*Tad)
M0d     = 0.707*Vlo/a0
m0_d    = en.f_m0(Pad, Afan, M0, Tad) # kg/s

_,_,Fnd,TSFCd,f = en.turbojato(PCI, m0_d, pic, T04, Pad, Tad, M0d)

acel    = (Fnd - 0.02*Wmax)*g/Wmax
Sg      = Vlo**2/(2*acel)
Dt      = Vlo/(2*acel)

Fn_req  = 0.5*1e3*Pad*0.707*Vlo*Cd(Clmax)*Aw
SFC     = TSFCd*Fn_req*Dt

print('\n'+10*'-'+'Impulso na decolagem'+10*'-')
print(f'Fn\t= {Fnd} [N]')
print(f'Vlo\t={Vlo} [m/s]')
print(f'Mad\t= {M0d}')
print(f'acel\t= {acel} [m/s²] ')
print(f'Sg\t= {Sg} [m]')
print(f'Deltat\t= {Dt} [s]')
#%% 

"""
                                       TURBOFAN
"""
#                                       PARTE I
#%% Decolagem -------------------------------------------------------------------------------------------------
Fntf   = []
TSFCtf = []
piLPCx = []
for i in np.linspace(1.0,1.8):
    _,_,Fn,TSFC = en.turbofan(B, PCI, m0, pic, i, T04, Pac, Tac, M0)
    Fntf.append(Fn/1000)
    TSFCtf.append(TSFC)
    piLPCx.append(i)

Fntf    = np.array(Fntf)
TSFCtf  = np.array(TSFCtf)

plt.plot(piLPCx,Fntf)
plt.xlabel(r'$\pi_{LPC}$')
plt.ylabel(r'$F_n[kN]$')
plt.grid()
plt.title(r'Comportamento do $F_n$ para $\pi_{LPC}$')
plt.savefig('images/LPC_Fn.png')
plt.close()

plt.plot(piLPCx,TSFCtf)
plt.xlabel(r'$\pi_{LPC}$')
plt.ylabel(r'$TSFC[kg/N\cdot h]$')
plt.grid()
plt.title(r'Comportamento do $TSFC$ para $\pi_{LPC}$')
plt.savefig('images/LPC_TSFC.png')
plt.close()

pifan    = 1.65
pid, taud, Fnd, TSFCd,fd = en.turbofan(B, PCI, m0f, picf, pifan, T04, Pad, Tad, 0, cp = cpd)
print('\nDados TurboFan na decolagem')
print(f'Fn\t= {Fnd/1000} [kN]')
print(f'TSFC\t= {TSFCd} [kg/N.h]')

#%% Cruzeiro -------------------------------------------------------------------------------------------------
pi, tau,Fn,TSFC,f = en.turbofan(B, PCI, m0f, picf, T04, Pac, Tac, M0,cp = cpc)
print('\nDados TurboJato em cruzeiro')
print(f'Fn\t= {Fn/1000} [kN]')
print(f'TSFC\t= {TSFC} [kg/N.h]')

#%%
#                                      PARTE II
#%% Decolagem - Take off -------------------------------------------------------------------------------------------------
minital = mmfan*neng
Vstall  = np.sqrt(Wmax*R*Tad/(0.5*Pad*1000*Clmax*Aw))
Vlo     = 1.2*Vstall 
a0      = np.sqrt(k*R*Tad)
M0d     = 0.707*Vlo/a0
m0_d    = en.f_m0(Pad, Afan, M0, Tad) # kg/s

_,_,Fnd,TSFCd,f = en.turbojato(PCI, m0_d, pic, T04, Pad, Tad, M0d)

acel    = (Fnd - 0.02*Wmax)*g/Wmax
Sg      = Vlo**2/(2*acel)
Dt      = Vlo/(2*acel)

Fn_req  = 0.5*1e3*Pad*0.707*Vlo*Cd(Clmax)*Aw
SFC     = TSFCd*Fn_req*Dt

print('\n'+10*'-'+'Impulso na decolagem'+10*'-')
print(f'Fn\t= {Fnd} [N]')
print(f'Vlo\t={Vlo} [m/s]')
print(f'Mad\t= {M0d}')
print(f'acel\t= {acel} [m/s²] ')
print(f'Sg\t= {Sg} [m]')
print(f'Deltat\t= {Dt} [s]')
