import numpy as np

#%% Engines
def f_m0(P0, A, M, T, k=1.4, R=287):
    P0 *= 1000
    pp1 = P0*A*M*(k**0.5)/((R*T)**0.5)
    pp2 = (1+(k-1)*(M**2)/2)**((-k-1)/(2*k-2))
    return pp1*pp2


def turbofan(B:float, PCI:float, m0:float, piHPC:float,
            piLPC:float, T04:float, Pa:float, Ta:float,
            M0:float, cp:float=1004, k:float=1.4, R:float=287) -> tuple:
    
    mac = m0*B/(B+1)
    mah = mac/B
    
    # INTAKE (1->2)
    T02l = T01 = Ta*(1+(k-1)*(M0**2)/2)
    P02l = P01 = Pa*( (1+(k-1)*(M0**2)/2)**(k/(k-1)) )
    
    pii  = 1
    taui = 1
    
    #Low Pressure Compressor (2'->3')
    P03l = P02 = P02l*piLPC
    T03l = T02 = T02l*(piLPC**((k-1)/k))
    
    tauLPC = piLPC**((k-1)/k)
    
    # High Pressure Compressor (2->3)
    P03 = P02*piHPC
    T03 = T02*(piHPC**((k-1)/k))
    
    tauHPC = piHPC**((k-1)/k)
    
    #Burner (3->4)
    P04 = P03
    f   = (T04/T03 - 1)/(PCI/(cp*T03) - T04/T03)
    
    pib  = 1
    taub = T04/T03
    
    # High Pressure Turbine (4->5)
    T05  = T04 - (T03-T02)/(1+f)
    P05  = P04* ( (T05/T04)**(k/(k-1)) )
    
    piHPT  = P05/P04
    tauHPT = T05/T04
    
    # Low Pressure Turbine (5->6)
    T06  = T05 - ((B+1)*(T03l-T02l))/(1+f)
    P06  = P05 * ( (T06/T05)**(k/(k-1)) )
    
    piLPT  = P06/P05
    tauLPT = T06/T05
    
    # Nozzle secundário (3'->7')
    T07l  = T03l
    P07l  = P03l
    
    # Nozzle primário (6->7)
    T07   = T06
    P07   = P06
    piNS  = piNP  = 1
    tauNS = tauNP = 1
    
    pi    = (pii, piLPC, piHPC, pib, piHPT, piLPT, piNS, piNP)
    tau   = (taui, tauLPC, tauHPC, taub, tauHPT, tauLPT, tauNS, tauNP)
    
    NPRp  = P06/Pa 
    NPRs  = P03l/Pa
    
    # Cheque de choque
    if NPRp > 1.893:
        Mep = 1
    else:
        Mep = ( 2*(NPRp**((k-1)/k)-1)/(k-1) )**0.5 
        
    if NPRs > 1.893:
        Mes = 1
    else:
        Mes = ( 2*(NPRs**((k-1)/k)-1)/(k-1) )**0.5 
    
    T7  = T07/(1+(Mep**2)*(k-1)/2)
    T7l = T07l/(1+(Mes**2)*(k-1)/2)

    P7  = P07 /(1+Mep**2 * (k-1)/2)**(k/(k-1))
    P7l = P07l/(1+Mes**2 * (k-1)/2)**(k/(k-1))

    uep = Mep*( (k*R*T7)**0.5 )
    ues = Mes*( (k*R*T7l)**0.5 )
    
    # Calculo do impulso
    Ae  = (1+f)*mah*R*T7/(P7*1000*uep)
    Ael = mac*R*T7l/(P7l*1000*ues) 
    
    u0  = M0*( (k*R*Ta)**0.5 )
    
    Fn  = mah*((1+f)*uep - u0) + 1000*(P7-Pa)*Ae + (ues-u0)*mac + 1000*(P7l-Pa)*Ael
    
    # Consumo de combustível
    TSFC= 3600*mah*f/Fn
    
    return (pi, tau, Fn, TSFC, f)

def turbojato(PCI:float, m0:float, pic:float, T04:float, 

              Pa:float, Ta:float, M0:float, k:float = 1.4,
              cp:float=1004, R:float=287, prt:bool = False) -> tuple:
              

    # Intake (1->2)
    T02     = T01 = Ta*(1+(k-1)*(M0**2)/2)
    P02     = P01 = Pa*(T02/T01)**(k/(k-1))
    
    pid    = 1
    taud   = 1

    # Compressor (2->3)
    P03     = pic*P02
    T03     = T02*pic**((k-1)/k)
    
    tauc   = pic**((k-1)/k)

    # Burner (3->4)
    taub    = T04/T03
    pib     = 1

    f       = (taub - 1)/(PCI/cp/T03 - taub)
    mf      = f*m0
    P04     = P03
    
    # Turbine (4->5)           
    T05     = T04 - cp*(T03 - T02)/(cp*(1+f))   
    taut    = T05/T04
    
    P05     = P04*taut**(k/(k-1))
    pit     = P05/P04

    # Nozzle (5->6)
    T06     = T05
    P06     = P05

    taun    = 1
    pin     = 1 

    NPR = T06/Ta

    if round(NPR,3) >= 1.892:
        Me = 1
        if round(NPR,3)==1.892:
            print("Chocked!\nMe\t= 1")
        else:
            print("Just chocked!\nMe\t= 1")
    else:
        Me = np.sqrt(2*( NPR**((k-1)/k) -1 )/(k-1) )
        print(f"No chocked!\nMe = {Me}")
    
    Pe      = P06/( (1+(k-1)*(Me**2)/2)**(k/(k-1)) )
    Te      = T06/( (1+(k-1)*(Me**2)/2) )

    # Pressure and Temperature Ratios
    pi      = (pid, pic, pib, pit, pin)
    tau     = (taud, tauc, taub, taut, taun)

    # Impulse
    u0      = M0*np.sqrt(k*R*Ta)
    ue      = Me*np.sqrt(k*R*Te)
    m_tot   = m0 + mf
    Ae      = (R*Te*m_tot)/(ue*1000*Pe)

    Fn      = m0*( (1+f)*ue -u0 ) + 1000*(Pe - Pa)*Ae
    
    # TSFC
    TSFC = 3600*mf/Fn

    return (pi,tau, Fn, TSFC, f)

#%% 
















    