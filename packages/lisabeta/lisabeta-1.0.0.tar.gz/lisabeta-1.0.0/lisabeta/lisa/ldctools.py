#This file contains tools for interfacing with data from the LDC

import numpy as np
import lisabeta.pyconstants as PC

#This stuff is to support the LDC params getConvert fn, probably don't really want to do it this way.
convAngle = {'rad':1.,\
             'radian':1.,\
             'r':1.,\
             'deg':np.pi/180.,\
             'degree':np.pi/180.
             }

convMass = {'kg':1.,\
            'g':1e-3,\
            'msun':PC.MSUN_SI,\
            'solarmass':PC.MSUN_SI}

convDistance = {'m':1.,\
                'meter':1.,\
                'km':1000.,\
                'pc':PC.PC_SI,\
                'kpc':1000*PC.PC_SI,\
                'mpc':1e6*PC.PC_SI,\
                'gpc':1e9*PC.PC_SI}

### Conversion of time
convTime = {'s':1.,\
            'sec':1.,\
            'second':1.,\
            'seconds':1.,\
            'mn':60.,\
            'minute':60.,\
            'h':3600.,\
            'hour':3600,\
            'day':86400.,\
            'year':PC.YRSID_SI,\
            'yr':PC.YRSID_SI}

### Convert everything in time
convT = convTime
c = 299792458.0         # Uses speed of light in vacuum [m.s^-1] (CODATA 2014)
G = 6.67408e-11         # Newtonian constant of graviation [m^3.kg^-1.s^-2] (CODATA 2014)
kg2s = G/(c*c*c)

for x in convDistance:
    convT.update( { x : convDistance[x]/c } )   
for x in convMass:
    convT.update( { x : convMass[x]*kg2s } )
####End of stuff for getConvert


def AziPolAngleL2PsiIncl(bet, lam, theL, phiL):
    """
    Convert Polar and Azimuthal angles of zS (typically orbital angular momentum L)
    to polarisation and inclination (see doc)
    @param bet is the ecliptic latitude of the source in sky [rad]
    @param lam is the ecliptic longitude of the source in sky [rad]
    @param theL is the polar angle of zS [rad]
    @param phiL is the azimuthal angle of zS [rad]
    @return polarisation and inclination
    """
    #inc = np.arccos( np.cos(theL)*np.sin(bet) + np.cos(bet)*np.sin(theL)*np.cos(lam - phiL) )
    #up_psi = np.cos(theL)*np.cos(bet) - np.sin(bet)*np.sin(theL)*np.cos(lam - phiL)
    #down_psi = np.sin(theL)*np.sin(lam - phiL)
    #psi = np.arctan2(up_psi, down_psi)

    inc = np.arccos( - np.cos(theL)*np.sin(bet) - np.cos(bet)*np.sin(theL)*np.cos(lam - phiL) )
    down_psi = np.sin(theL)*np.sin(lam - phiL)
    up_psi = -np.sin(bet)*np.sin(theL)*np.cos(lam - phiL) + np.cos(theL)*np.cos(bet)
    psi = np.arctan2(up_psi, down_psi)

    return psi, inc
    

def GetSkyAndOrientation(p):
    """
    Get sky postion and orientation of the source from parameters
    If Initial Polar Angle L and Initial Azimuthal Angle L are the parameters,
    it will do the conversion
    @param p is the parameters of GW MBHB as read from hdf5 file
    @return beta, lamdba, inclination and polarisation
    """
    bet = p.getConvert("EclipticLatitude",convAngle,'rad')
    lam = p.getConvert("EclipticLongitude",convAngle,'rad')

    OrientationDefined = False
    if ('InitialPolarAngleL' in p.pars) and ('InitialAzimuthalAngleL' in p.pars):
        OrientationDefined = True
        theL = p.getConvert('InitialPolarAngleL',convAngle,'rad') #!!!! WRONG TODO
        phiL = p.getConvert("InitialAzimuthalAngleL",convAngle,'rad')
        psi, inc = AziPolAngleL2PsiIncl(bet, lam, theL, phiL)
    if ('Polarisation' in p.pars) and ('Inclination' in p.pars):
        psi_n = p.getConvert('Polarisation',convAngle,'rad') #!!!! WRONG TODO
        inc_n = p.getConvert("Inclination",convAngle,'rad')
        if OrientationDefined and ( (not np.isclose(psi_n,psi)) or (not np.isclose(inc_n,inc))) :
            print("Error in ComputeMBHBXYZ_FD: Incompatibility between multiple definition of orientation:")
            print("\t - from Polarisation and Inclination : psi = ",psi_n," inc = ",inc_n)
            print("\t - from InitialPolarAngleL and InitialAzimuthalAngleL : psi = ",psi," inc = ",inc)
            raise ValueError
        psi = psi_n
        inc = inc_n
        OrientationDefined = True
    if not OrientationDefined :
        print("Error in ComputeMBHBXYZ_FD: Orientation not defined: use either InitialPolarAngleL and InitialAzimuthalAngleL or Polarisation and Inclination.")
        raise ValueError
    return bet, lam, inc, psi

def get_params_from_LDC(p):
    '''
    Get lisabeta/lisa parameters from LDC param object.

    #Input
    p        #LDC params

    #Output
    params   #for use with code in lisa.py
    '''
    
    #{{{
    ### Getting parameters:
    m1s = p.getConvert('Mass1',convMass,'solarmass')
    m2s = p.getConvert('Mass2',convMass,'solarmass')
    redshift = p.get('Redshift')
    DL = p.getConvert('Distance',convDistance,'mpc')
    tc = p.getConvert('CoalescenceTime',convT,'sec')

    phi0 = p.getConvert('PhaseAtCoalescence',convAngle,'rad')

    chi1s = p.get('Spin1')
    chi2s = p.get('Spin2')

    Stheta1s = p.getConvert('PolarAngleOfSpin1',convAngle,'rad') #!!!! WRONG TODO
    Stheta2s = p.getConvert('PolarAngleOfSpin2',convAngle,'rad') #!!!! WRONG TODO

    inc = p.getConvert('InitialPolarAngleL',convAngle,'rad') #!!!! WRONG TODO

    a1 = np.cos(Stheta1s)*chi1s
    a2 = np.cos(Stheta2s)*chi2s

    #phiL = p.get("InitialAzimuthalAngleL")
    #beta = p.get("EclipticLatitude")
    #lam = p.get("EclipticLongitude")
    ### psi and h+, hx is taken from https://arxiv.org/pdf/0806.2110.pdf
    #up = np.sin(beta)*np.cos(lam - phiL)*np.sin(inc) - np.cos(inc)*np.cos(beta)
    #down = np.cos(beta)*np.sin(lam - phiL)
    #psi = np.arctan2(up, down)
    beta, lam, inc, psi = GetSkyAndOrientation(p)
    #dist = Cosmology.DL(redshift, w=0)[0]

    #print ("DL:", dist, DL, DL-dist)
    #sys.exit(0)


    m1 =  m1s*(1+redshift)   ### redshifted masses
    m2 =  m2s*(1+redshift)

    Tobs = p.get("ObservationDuration")
    del_t = p.get("Cadence")

    #df = 0.5e-8
    #print ("Assumed duration ", 1.0/df)
    #Mc = pyFDresponse.funcMchirpofm1m2(m1, m2)
    #f0 = pyFDresponse.funcNewtonianfoft(Mc, 2.0*Tobs/YRSID_SI)
    #fRef = 1.e-3
    t0 = 0.0
    # psi = 0.5*np.pi - psi
    params = m1s, m2s, a1, a2, tc, DL, inc, phi0, lam, beta, psi
    return params

def make_params_dict(paramslist):
    params={}
    params['m1']   = paramslist[0]
    params['m2']   = paramslist[1]
    params['chi1'] = paramslist[2]
    params['chi2'] = paramslist[3]
    params['Deltat']=paramslist[4]
    params['dist'] = paramslist[5]
    params['inc']  = paramslist[6]
    params['phi']  = paramslist[7]
    params['lambda']=paramslist[8]
    params['beta'] = paramslist[9]
    params['psi']  = paramslist[10]
    return params

def ComputeTDfromFD(Xf, Yf, Zf, del_t):
    #Essentially copied from GenerateFD_SignalTDIs.py
    #Except that we use opposite sign convention, so take CC
    Xta = np.fft.irfft(Xf.conj())*(1.0/del_t)
    Yta = np.fft.irfft(Yf.conj())*(1.0/del_t)
    Zta = np.fft.irfft(Zf.conj())*(1.0/del_t)
    tma = np.arange(len(Xta))*del_t
    return (tma, Xta, Yta, Zta)

def ComputeFDfromTD(Xt, Yt, Zt, del_t):
    #Invented to invert ComputeTDfromFD
    Xf = np.fft.rfft(Xt*del_t).conj()
    Yf = np.fft.rfft(Yt*del_t).conj()
    Zf = np.fft.rfft(Zt*del_t).conj()
    Nf=len(Xf)
    df=0.5/del_t/(Nf)
    fr=np.arange(Nf)*df
    #Nf=len(Xf)
    #fmx=0.5/del_t
    #df=fmx/(Nf-1)
    #fr=np.arange(Nf)*df
    return (fr, Xf, Yf, Zf)


def convert_XYZ_to_AET(X,Y,Z):
    A=(Z - X)/np.sqrt(2)        
    E=(X - 2*Y + Z)/np.sqrt(6)
    T=(X + Y + Z)/np.sqrt(3)
    return A,E,T

def shiftTime(f,Xf,delay):
    return Xf*np.exp(-2j*np.pi*f*delay)

#Transform data to freq domain (with opposite sign convention)
def makeFDtrim(TDA,TDE,TDT,dt,minf=1e-5,maxf=0.1,offset=0):
    fs,FDA,FDE,FDT=ComputeFDfromTD(TDA,TDE,TDT,dt)
    #First optimization: restricting the bandwidth
    #print(fs[0],'<f<',fs[-1])
    if minf>fs[0]:
        #print(np.argwhere(fs>minf))
        imin=np.argwhere(fs>minf)[0][0]
    else: imin=0
    if maxf<fs[-1]:iend=np.argwhere(fs>maxf)[0][0]
    else:iend=len(fs)
    #print(imin,"< i <",iend)
    FDA=shiftTime(fs,FDA,offset)[imin:iend]
    FDE=shiftTime(fs,FDE,offset)[imin:iend]
    FDT=shiftTime(fs,FDT,offset)[imin:iend]
    fs=fs[imin:iend] #cut off zero-freq
    return fs,FDA,FDE,FDT

#Transform data to freq domain (with opposite sign convention)
def trimFD(fs,FDA,FDE,FDT,minf=1e-5,maxf=0.1,offset=None):
    #fs,FDA,FDE,FDT=ComputeFDfromTD(TDA,TDE,TDT,dt)
    #First optimization: restricting the bandwidth
    #print(fs[0],'<f<',fs[-1])
    if minf>fs[0]:
        #print(np.argwhere(fs>minf))
        imin=np.argwhere(fs>minf)[0][0]
    else: imin=0
    if maxf<fs[-1]:iend=np.argwhere(fs>maxf)[0][0]
    else:iend=len(fs)
    #print(imin,"< i <",iend)
    newFDA=np.array(FDA)
    newFDE=np.array(FDE)
    newFDT=np.array(FDT)    
    if offset is not None:
        newFDA=shiftTime(fs,newFDA,offset)[imin:iend]
        newFDE=shiftTime(fs,newFDE,offset)[imin:iend]
        newFDT=shiftTime(fs,newFDT,offset)[imin:iend]
    else:
        newFDA=newFDA[imin:iend]
        newFDE=newFDE[imin:iend]
        newFDT=newFDT[imin:iend]
    newfs=fs[imin:iend] #cut off zero-freq
    return newfs,newFDA,newFDE,newFDT

def decimate2(X):
    n=int(len(X)/2)
    Xd=np.zeros(n,dtype=X.dtype)
    for i in range(n):
        Xd[i]=X[2*i]+X[2*i+1]
        #if numpy.abs(Xd[i]-2*X[2*i])/numpy.abs(Xd[i])>0.01:print(i,numpy.abs(Xd[i]-2*X[2*i])/numpy.abs(Xd[i]),X[2*i],X[2*i+1],Xd[i]/2)
    return Xd/2.0
