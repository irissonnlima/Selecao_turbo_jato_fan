from platform import machine
import matplotlib.pyplot as plt
import engines as en
from inputs import *
import numpy as np

cl          = np.linspace(-2.1,2.1)
cd          = Cd(cl)
plt.plot(cd, cl)
plt.xlabel('Cd')
plt.ylabel('Cl')
plt.grid()
plt.show()

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
plt.show()