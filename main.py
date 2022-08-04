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
pid, taud, Fnd, TSFCd,fd = en.turbojato(PCI, m0j, picj, T04, Pad, Tad, 0,cp = cpd)
print('\nDados TurboJato na decolagem')
print(f'Fn\t= {Fnd/1000} [kN]')
print(f'TSFC\t= {TSFCd} [kg/N.h]')
print(f'Consumo\t= {TSFCd*Fnd} [kg/.h]')

#%% Cruzeiro -------------------------------------------------------------------------------------------------
pi, tau,Fn,TSFC,f = en.turbojato(PCI, m0j, picj, T04, Pac, Tac, M0, cp = cpc)
print('\nDados TurboJato em cruzeiro')
print(f'Fn\t= {Fn/1000} [kN]')
print(f'TSFC\t= {TSFC} [kg/N.h]')
print(f'Consumo\t= {TSFC*Fn} [kg/.h]')

#%%
#                                       PARTE II
#%% Decolagem - Take off -------------------------------------------------------------------------------------------------
MfuelMissionj   = []
FnMissionj      = []
Mj              = []

m_tot   = 100_000
m_wetj  = memp+nengj*mmjato
m_fuelj = m_tot - memp - nengj*mmfan 
W0      = m_tot*g

v_stall = np.sqrt( W0/(0.5*Clmax*rhod*Aw) )
V_lo    = 1.2*v_stall
u0      = 0.707*V_lo
M_to    = u0/np.sqrt(k*R*Tad)

_,_,Fnd,TSFCd,_ =en.turbojato(PCI, m0j, picj, T04, Pad, Tad, M_to, cp = cpd) 
TSFCd/=3600

Fn_tot  = nengj*Fnd
a_med   = g*(Fn_tot-0.02*W0)/W0
d_to    = V_lo**2/(2*a_med)
t_to    = V_lo/(2*a_med)
Cd_to   = Cd(Clmax)
D_to    = 0.5*rhod*(u0**2)*Cd_to*Aw
SFC_to  = TSFCd*D_to*t_to
m_to    = m_tot - SFC_to

MfuelMissionj.append(m_to-m_wetj)
FnMissionj.append(Fn_tot)
Mj.append(m_tot)
print(10*'-'+'TURBOJET MISSION' + 10*'-')
print("\nDECOLAGEM "+10*'-')
print(f'Distância de decolagem: {d_to} m')
print(f'Tempo de decolagem: {t_to} s')
print(f'Massa após Takeoff: {m_to} kg')
print(f'Qte de combustível: {m_fuelj} kg')

#%% Subida -----------------------------------------------------------------------------------------------------------------
alphat  = np.deg2rad(10)
W_up    = m_to*g -SFC_to*g
L_up    = W_up*np.cos(alphat)
Cl_up   = 2*L_up/(rhod**Aw*usub**2)
Cd_up   = Cd(Cl_up)
D_upx   = 0.5*rhod*(u0**2)*Cd_up*Aw
D_upy   = 0.5*rhod*(usub**2)*Cd_to*Aw
t_up    = (hc*1e3/abs( np.sin(alphat) ) )/usub    

Fn_requp=D_upy/Fn_tot
SFC_up  = TSFCd*Fn_tot*Fn_requp
m_up    = m_to - SFC_up

MfuelMissionj.append(m_up-m_wetj)
FnMissionj.append(Fn_tot)
Mj.append(m_up)
print("\nSUBIDA "+10*'-')
print(f'Tempo de subida: {t_up} s')
print(f'Massa após subida: {m_up} kg')

#%% Alcance -----------------------------------------------------------------------------------------------------------------
W_cru   = W_up - SFC_up*g
Cl_cru  = 2*W_cru/(rhocru*Aw*(usub**2))
Cd_cru  = Cd(Cl_cru)
u_cru   = np.sqrt(2*W_cru/(rhocru*Aw*Cl_cru))
M_cru   = u_cru/(np.sqrt(k*R*Tacru))
t_cru   = A*1e3/u_cru
D_cru   = 0.5*rhocru*(u_cru**2)*Cd_cru*Aw


_,_,Fn,TSFCcru,_ =en.turbojato(PCI, m0j, picj, T04, Pacru, Tacru, M_cru,cp = cpc) 
TSFCcru /=3600

Fn_totcru= nengj*Fn
Fn_reqcru= D_cru/Fn_totcru
SFC_cru = TSFCcru*Fn_totcru*Fn_reqcru*t_cru
m_cru   = m_up - SFC_cru

MfuelMissionj.append(m_cru-m_wetj)
FnMissionj.append(Fn_totcru)
Mj.append(m_cru)
print("\nCRUZEIRO "+10*'-')
print(f"Vel. de cruzeiro   : {u_cru*3.6} [km/h]")
print(f'Mach de cruzeiro   : {M_cru}')
print(f'Tempo de cruzeiro  : {t_cru/3600} h')
print(f'Massa após cruzeito: {m_cru} kg')
#%% Descida -----------------------------------------------------------------------------------------------------------------
W_do    = W_cru - SFC_cru*g
L_do    = W_do*np.cos(alphat)
Cl_do   = 2*W_do/(rhocru*Aw*(udesc**2))
Cd_do   = Cd(Cl_do)
D_doy   = 0.5*rhocru*(udesc**2)*Cd_do*Aw
D_dox   = 0.5*rhocru*(u0**2)*Cd_up*Aw
Fn_reqdo= D_doy/Fn_tot

t_do    = ( hc*1e3/ np.sin(alphat))/udesc
SFC_do  = TSFCd*Fn_tot*Fn_reqdo*t_do

m_do    = m_cru - SFC_do
W_do2   = W_do - SFC_do*g

MfuelMissionj.append(m_do-m_wetj)
FnMissionj.append(Fn_tot)
Mj.append(m_do)
print("\nDESCIDA "+10*'-')
print(f'Tempo de descida  : {t_do} s')
print(f'Massa após descida: {m_do} kg')
#%% 

"""
                                       TURBOFAN
"""
#                                       PARTE I
#%% Decolagem -------------------------------------------------------------------------------------------------
pid, taud, Fnd, TSFCd,fd = en.turbofan(B, PCI, m0f, picf, pifan, T04, Pad, Tad, 0, cp = cpd)
print('\nDados TurboFan na decolagem')
print(f'Fn\t= {Fnd/1000} [kN]')
print(f'TSFC\t= {TSFCd} [kg/N.h]')
print(f'Consumo\t={Fnd*TSFCd} [kg/h]')

#%% Cruzeiro -------------------------------------------------------------------------------------------------
Fntf   = []
TSFCtf = []
piLPCx = []
for i in np.linspace(1.0,1.8):
    _,_,Fn,TSFC,_ = en.turbofan(B, PCI, m0f, picf, i, T04, Pac, Tac, M0, cp = cpc)
    Fntf.append(Fn/1000)
    TSFCtf.append(TSFC)
    piLPCx.append(i)

Fntf    = np.array(Fntf)
TSFCtf  = np.array(TSFCtf)

fig, ax1 = plt.subplots()
ax1.plot(piLPCx,Fntf, 'r')
ax1.set_xlabel(r'$\pi_{LPC}$')
ax1.set_ylabel(r'$F_n[kN]$')
ax1.tick_params(axis='y', labelcolor='r')
ax1.grid(color='r', linestyle='-.')

ax2 = ax1.twinx()

ax2.plot(piLPCx,TSFCtf,'b')
ax2.set_xlabel(r'$\pi_{LPC}$')
ax2.set_ylabel(r'$TSFC[kg/N\cdot h]$')
ax2.tick_params(axis='y', labelcolor='b')
ax2.grid(color='b', linestyle=':')
plt.savefig('images/LPC_TSFC_Fn.png')
plt.title(r'comportamento do $TSFC$ e $F_n$')
plt.close()

pi, tau,Fn,TSFC,f = en.turbofan(B, PCI, m0f, picf, pifan,T04, Pac, Tac, M0,cp = cpc)
print('\nDados TurboFan em cruzeiro')
print(f'Fn\t= {Fn/1000} [kN]')
print(f'TSFC\t= {TSFC} [kg/N.h]')
print(f'Consumo\t={Fn*TSFCd} [kg/h]')



#%%
#                                      PARTE II
#%% Decolagem - Take off -------------------------------------------------------------------------------------------------
MfuelMissionf   = []
FnMissionf      = []
Mf              = []

m_tot   = 100_000
m_wetf  = memp+nengf*mmfan
m_fuelf = m_tot - memp - nengf*mmfan 
W0      = m_tot*g

v_stall = np.sqrt( W0/(0.5*Clmax*rhod*Aw) )
V_lo    = 1.2*v_stall
u0      = 0.707*V_lo
M_to    = u0/np.sqrt(k*R*Tad)

_,_,Fnd,TSFCd,_ =en.turbofan(B, PCI, m0f, picf, pifan, T04, Pad, Tad, M_to, cp = cpd) 
TSFCd/=3600
Fn_tot  = nengf*Fnd
a_med   = g*(Fn_tot-0.02*W0)/W0
d_to    = V_lo**2/(2*a_med)
t_to    = V_lo/(2*a_med)
Cd_to   = Cd(Clmax)
D_to    = 0.5*rhod*(u0**2)*Cd_to*Aw
Fn_reqto= D_to/Fn_tot
SFC_to  = TSFCd*D_to*t_to
m_to    = m_tot - SFC_to

MfuelMissionf.append(m_to-m_wetf)
FnMissionf.append(Fn_tot)
Mf.append(m_tot) 

print(10*'-'+'TURBOFAN MISSION' + 10*'-')
print("\nDECOLAGEM "+10*'-')
print(f'Distância de decolagem: {d_to} m')
print(f'Tempo de decolagem: {t_to} s')
print(f'Massa após Takeoff: {m_to} kg')
print(f'Qte de combustível: {m_fuelf} kg')
#%% Subida -----------------------------------------------------------------------------------------------------------------
alphat  = np.deg2rad(10)
W_up    = m_to*g -SFC_to*g
L_up    = W_up*np.cos(alphat)
Cl_up   = 2*L_up/(rhod**Aw*usub**2)
Cd_up   = Cd(Cl_up)
D_upx   = 0.5*rhod*(u0**2)*Cd_up*Aw
D_upy   = 0.5*rhod*(usub**2)*Cd_to*Aw
t_up    = (hc*1e3/abs( np.sin(alphat) ) )/usub    

Fn_requp=D_upy/Fn_tot
SFC_up  = TSFCd*Fn_tot*Fn_requp
m_up    = m_to - SFC_up

MfuelMissionf.append(m_up-m_wetf)
FnMissionf.append(Fn_tot)
Mf.append(m_up)

print("\nSUBIDA "+10*'-')
print(f'Tempo de subida: {t_up} s')
print(f'Massa após subida: {m_up} kg')

#%% Alcance -----------------------------------------------------------------------------------------------------------------
W_cru   = W_up - SFC_up*g
Cl_cru  = 2*W_cru/(rhocru*Aw*(usub**2))
Cd_cru  = Cd(Cl_cru)
u_cru   = np.sqrt(2*W_cru/(rhocru*Aw*Cl_cru))
M_cru   = u_cru/(np.sqrt(k*R*Tacru))
t_cru   = A*1e3/u_cru
D_cru   = 0.5*rhocru*(u_cru**2)*Cd_cru*Aw


_,_,Fn,TSFCcru,_ =en.turbofan(B, PCI, m0f, picf, pifan,T04, Pacru, Tacru, M_cru,cp = cpc) 
TSFCcru /=3600

Fn_totcru= nengf*Fn
Fn_reqcru= D_cru/Fn_totcru
SFC_cru = TSFCcru*Fn_totcru*Fn_reqcru*t_cru
m_cru   = m_up - SFC_cru

MfuelMissionf.append(m_cru-m_wetf)
FnMissionf.append(Fn_totcru)
Mf.append(m_cru)

print("\nCRUZEIRO "+10*'-')
print(f"Vel. de cruzeiro   : {u_cru} [m/s]")
print(f'Mach de cruzeiro   : {M_cru}')
print(f'Tempo de cruzeiro  : {t_cru/3600} h')
print(f'Massa após cruzeito: {m_cru} kg')
#%% Descida -----------------------------------------------------------------------------------------------------------------
W_do    = W_cru - SFC_cru*g
L_do    = W_do*np.cos(alphat)
Cl_do   = 2*W_do/(rhocru*Aw*(udesc**2))
Cd_do   = Cd(Cl_do)
D_doy   = 0.5*rhocru*(udesc**2)*Cd_do*Aw
D_dox   = 0.5*rhocru*(u0**2)*Cd_up*Aw
Fn_reqdo= D_doy/Fn_tot

t_do    = ( hc*1e3/ np.sin(alphat))/udesc
SFC_do  = TSFCd*Fn_tot*Fn_reqdo*t_do

m_do    = m_cru - SFC_do
W_do2   = W_do - SFC_do*g


MfuelMissionf.append(m_do-m_wetf)
FnMissionf.append(Fn_tot)
Mf.append(m_do)

print("\nDESCIDA "+10*'-')
print(f'Tempo de descida  : {t_do} s')
print(f'Massa após descida: {m_do} kg')

print('\n\n', MfuelMissionf,'\n\n')
print(MfuelMissionj)
