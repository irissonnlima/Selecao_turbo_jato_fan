from platform import machine
import matplotlib.pyplot as plt
import engines as en
from inputs import *
from main import MfuelMissionf, MfuelMissionj, FnMissionf, FnMissionj, Mf, Mj
import numpy as np

cl          = np.linspace(-2.1,2.1)
cd          = Cd(cl)
plt.plot(cd, cl)
plt.xlabel('Cd')
plt.ylabel('Cl')
plt.grid()
plt.close()

vec_fn      = []
vec_tsfc    = []
mach        = []
for i in np.linspace(0,1):
    _,_, fn_tf, tsfc_tf, _ = en.turbofan(B, PCI, m0f, picf, pifan, T04, 73.8, 273.15-55, i)
    vec_fn.append(fn_tf/1000)
    vec_tsfc.append(tsfc_tf)
    mach.append(i)

vec_fn   = np.array(vec_fn)
vec_tsfc = np.array(vec_tsfc)
plt.plot(mach, vec_fn)
#plt.plot(mach, vec_fn)
plt.close()

#%% Massa x estágios de voo

estagio = ['takeoff', 'subida', 'cruzeiro', 'descida']

plt.plot(estagio, np.array(Mj)/1e3, 'b', label = 'Turbojato')
plt.plot(estagio, np.array(Mf)/1e3, 'r', label = 'Turbofan')
plt.title("Massa x Estágios de operação")
plt.xlabel("Operação")
plt.ylabel("Massa [Ton]")
plt.grid()
plt.legend()
plt.savefig('images/massxest.png')
plt.close()
#%% Impulso x estágio de voo
plt.plot(estagio, np.array(FnMissionj)/1e3, 'b', label = 'Turbojato')
plt.plot(estagio, np.array(FnMissionf)/1e3, 'r', label = 'Turbofan')
plt.title("Impuslo x Estágios de operação")
plt.xlabel("Operação")
plt.ylabel("Impulso [kN]")
plt.grid()
plt.legend()
plt.savefig('images/Imp_x_est.png')
plt.close()
