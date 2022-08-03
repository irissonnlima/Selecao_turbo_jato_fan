import engines as en

# Dados atmosféricos
Tac     = -4.83+273.15  # K (Temperatura de cruzeiro)
Tad     = 15+273.15     # K (Temperatura de decolagem)
Pac     = 69658.015     # Pa (Pressão atm de cruzeiro)
Pad     = 101135.00     # Pa (Pressão atm de decolagem)
cpc     = 1003.25       # J/kg (cp cruzeiro)
cpd     = 1004.08       # J/kg (cp decolagem)

# Dados construtivos
M0      = 0.85 
PCI     = 43e6          # J/kg K
T04     = 1300          # K
pic     = 24.5          #
m0      = 65            # kg/s

#%% Cruzeiro
pi, tau, Fn, TSFC = en.turbojato(PCI, m0, pic, T04, Pac, Tac, M0)
