from math import exp, pow
from math import log, sqrt
from math import sin, cos, tan, atan, pi

T_abs = 273.15

class dlemEvap:
    def __init__(self, lat, depth, elev, solrad, ta, vpd, pres, ut, tw0, fch, mth, tds):
        
        """Daily Lake Evaporation Model

        Arguments
        ---------
        lat : float
            Latitude [degrees].
        depth : float
            Average depth of reservoir (m)
        elev : float
            Elevation [m].
        solrad : float
            incoming surface shortwave solar radiation (W m-2 per day)
        ta : float
            Daily average temperature (C)
        vpd : float
            vapor pressure deficit (kPa)
        pres : float
            Atmospheric Pressure (Pa)
        ut : float
            wind speed at 2m (m s-1)
        tw0 : float
            Water surface temp from previous timestep
        fch : float
            fetch length (m)
        mth : float
            Month of interest
        tds: float
            Total disolved solids (ppm)
        Raises
        ------
        ValueError
            None so far

        Notes
        -----
        Latitude units are degress, not radians.

        References
        ----------
        [1] Gang Zhao, and Huilin Gao. "Estimating reservoir evaporation losses for the United States:
            Fusing remote sensing and modeling approaches." Remote Sensing ofEnvironment 226 (2019):109-124.
        [2] “Monitoring Daily Reservoir Evaporation Losses for the State of Texas”, Bingjie Zhao,
            et al… (tentative authors from TAMU, DRI, TWDB, COE, and LCRA), in preparation.
        """


        ##################### Variables #####################
        # alambda - latent heat of vaporisation (MJ kg-1)
        # gamma - pschrometric constant (kPa deg.C-1)
        # airds - density of air (kg m-3)
        # deltaa - slope of the temperature-satuartion water vapour curve at air temperature (kPa deg C-1)
        # deltawb - slope of the temperature-satuartion water vapour curve at wet bulb temperature (kPa deg C-1)
        # deltaw - slope of the temperature-satuartion water vapour curve at water temperature (kPa deg C-1)
        # windf - wind function 
        # rn - net radiation (MJ m-2 per day)
        # heat_stg - change in heat storage (MJ m-2 per day)
        # tau - time constant of the water body (days)
        # te - equilibrium temperature (deg. C)
        # tw - temperature of the water at the end of the time period (deg.C)
        # le - latent heat flux (w m-2 per day)
        # evap_hs - evaporation calculated using the heat storage (mm/day)
        # evap_nohs - evaporation calculated using no heat storage (mm/day)
        
        # Define Constants
        waterds = 1000.0  # density of water (kg m-3)
        cw = 0.0042       # specific heat of water (MJ kg-1 deg.V-1)
        sigma = 4.9e-9    # stefan-boltzmann constant (MJ m-2 deg.C-4 d-1)
        T_abs = 273.15    # difference between degrees kelvin and degrees celsius
        alb = 0.1         # albedo of the water body
        tstep = 1         #  the time step for the model to use (days)

        # Set up ierr error Flags
        # 0 = ok
        # 2 = depth =< 0
        # 3 = air temperature < wet bulb temperature
        # 4 = downwelling solar radiation  = < 0
        # 5 = wind speed < 0.01 m/s
        # 6 = vpd  = < 0
        # 7 = vpd > vsat

        # Set initial at 0
        ierr = 0

        # Clamp Depth between 0 and 20
        ierr = 2 if depth <= 0 else ierr
        depth = 20.0 if depth>20.0 else depth
        depth = 0.001 if depth<=0 else depth

        # Clamp Solar above 0
        ierr = 3 if solrad <= 0. else ierr
        solrad = 0 if solrad<=0 else solrad

        # Clamp wind speed
        ierr = 4 if ut <= 0.01 else ierr
        ut = 0.01 if ut <= 0.01 else ut

        # Clamp vapor pressure deficite
        ierr = 5 if vpd <= 0 else ierr
        vpd = 0.0001 if vpd <= 0 else vpd


    ##############################################################################################
    ########################### Calculate water equilibrium temperature ##########################
    ##############################################################################################

    ## some variables
        alambda = alambdat(ta)
        gamma = psyconst(pres, alambda)

    ## slope of the saturation water vapour curve at the air temperature (kPa deg C-1) 
        deltaa = delcalc(ta)

    ## actual vapor pressure and saturated vapor pressure (kPa) 
        es = v_sat(ta)
        ea = es - vpd  
        ea = 0.01 if ea < 0 else ea
        [ierr, vpd] = [6, es*0.99] if es < vpd else [ierr, vpd]
        
    ## slope of the saturation water vapour curve at the wet bulb temperature (kPa deg C-1) */
        twb = tvpd2wbt(ta, vpd)
        [ierr, twb] = [7, ta] if twb > ta else [ierr, twb]
        deltawb = delcalc(twb)
        
    ## Emissvity of air and water (unitless)
        sradj = solrad*0.0864       ## convert from W m-2 to MJ m-2 d-1

        fcd = cloud_factor(sradj, mth, lat, elev)
        em_a = 1.08*(1.-exp(-pow(ea*10.,(ta+T_abs)/2016.)))*(1+0.22*pow(fcd,2.75))
        em_w = 0.97

        longrad = -9999
        lradj = em_a*sigma*pow((ta+T_abs),4.) if longrad == -9999 else longrad*0.0864

    ## wind function using the method
        windf = (2.33+1.65*ut)*pow(fch, -0.1)*alambda
        
    ## calculate regression coefficients 
    ## Stream temperature/air temperature relationship: a physical interpretation (O. Mohseni , H.G. Stefan) */
        dcu = windf*(deltaa+gamma)                                  ## (MJ/m2/d)
        B0 = (0.46*em_a+dcu)/(0.46*em_w+dcu)                        ## unitless 
        B1 = ((1.-alb)*sradj-28.38*(em_w-em_a))/(0.46*em_w+dcu)     ## deg. C 
        B2 = windf/(em_w*0.46+dcu)

        te = B0*ta+B1-B2*(es-ea)

    ###############################################################################################
    ############################## Calculate water column temperature #############################
    ###############################################################################################

    ## time constant (d) 
        tau = (waterds*cw*depth)/(4.0*sigma*pow((twb+T_abs),3.)+windf*(deltawb+gamma))
    ## water column temperature (deg. C) 
        tw = te+(tw0-te)*exp(-tstep/tau)
        tw = 0. if tw<0. else tw

    ## change in heat storage (MJ m-2 d-1)
        heat_stg = waterds*cw*depth*(tw-tw0)/tstep

    ################################################################################################
    ############################### Calculate the Salinity Adjustment ##############################
    ################################################################################################    
    # calculate water density from TDS
        ρ=1+tds*0.695*10**(-6)
    # calulate evap beta factor
        β = -30.285 + 77.650*ρ - 62.712*(ρ**2) + 16.3*(ρ**3)
        
    ################################################################################################
    ################################### Calculate the evaporation ##################################
    ################################################################################################

    ## calculate the Penman evaporation
        rn = sradj*(1.-alb)+lradj-em_w*(sigma*pow((ta+T_abs),4.))
        
        le = (deltaa*(rn-heat_stg)+gamma*windf*vpd)/(deltaa+gamma)
        evap_hs = le/alambda
        # evap_hs = 0 if evap_hs < 0 else evap_hs # update 8/8/2023
        
        le = (deltaa*(rn)+gamma*windf*vpd)/(deltaa+gamma)
        evap_nohs = le/alambda
        # evap_nohs = 0 if evap_nohs < 0 else evap_nohs # update 8/8/2023
        
        # Salinity adjustemnt
        if 10_000 < tds < 1_000_000:
            evap_hs_adj = evap_hs*β
        else:
            evap_hs_adj = evap_hs
        
        # Assign outputs to self?
        self.tw = tw
        self.evap_hs = evap_hs
        self.evap_hs_adj = evap_hs_adj
        self.evap_nohs = evap_nohs
        self.ierr = ierr
        self.te = te
        self.rn = rn


###############################################################################
#                     Functions
###############################################################################


def delcalc(ta):
    """Fucntion to calculate slope of the vapour pressure
    curve using air temperature
   Args:
       ta: Air temperature (deg. C)
   Returns:
       slope of the vapour pressure curve (kPa deg. C-1)
   """
    
    ea = 0.6108*exp(17.27*ta/(ta+237.3))
    delcalc = 4098*ea/pow((ta+237.3),2.)
    return delcalc

def alambdat(ta):
    """Function to correct the Latent Heat of Vaporisation
   Args:
       ta: Air temperature (deg. C)
   Returns:
       Latent Heat of Vaporisation (MJ kg-1)
   """
    
    return 2.501-ta*2.361e-3


def psyconst(p, alambda):   ## S2.9 
    """Function to calculate the psychrometric constant (kPa deg. C-1) 
   Args:
       p: Atmospheric Pressure (Pa)
       alambda: Latent Heat of Vaporisation (MJ kg-1)
   Returns:
       psychrometric constant (kPa deg. C-1) 
   """
    
    p = p/1000 # convert Pa to kPa
    
    return 0.00163*p/alambda


def v_sat(ta):
    """Function to calculate saturated vapor pressure
   Args:
       ta: Air temperature (deg. C)
   Returns:
       Saturated Vapor Pressure (kPa)
   """

    return 0.6108*exp(17.27*ta/(ta+237.3))


def tvpd2wbt(ta, vpd): ##S2.2 S2.3    
    """Function to calculate wet bulb temperature
   Args:
       ta: Air temperature (deg. C)
       vpd: Vapor Pressure Deficiete (kPa)
   Returns:
       Wet Bulb Temperature (deg C.)
   """
    
    vpsat = v_sat(ta)
    t_d = (116.9+237.3*log(vpsat-vpd))/(16.78-log(vpsat-vpd))
    t_wb = (0.00066*100.*ta + 4098.*(vpsat-vpd)/pow(t_d+237.3,2)*t_d)/(0.00066*100.+4098.*(vpsat-vpd)/pow(t_d+237.3,2.))
    
    return t_wb


def wspd2m(wspd, hgt):
    """Function to correct wind speed to 2m collection height
    Base on http:##edis.ifas.ufl.edu/ae459 
   Args:
       wspd: wind speed at height hgt (m/s)
       hgt: Wind speed height (m)
   Returns:
       Wind at height of 2m (m/s)
   """

    wpd2m = wspd*4.87/log(67.8*hgt-5.42)
    return wpd2m


def airdens(ta,pres,elev):
    """Function to calculate air density
    Base on http:##edis.ifas.ufl.edu/ae459 
   Args:
       ta: Air Temperature (deg. C)
       pres: Atmospheric Pressure (Pa)
       elev: Elevation (m)
   Returns:
       Air Density (kg/m3)
   """
    
    # Methods
    # https:##en.wikipedia.org/wiki/Density_of_air#Altitude 
    # r     ideal (universal) gas constant, 8.31447 J/(mol K) 
    # m     molar mass of dry air, 0.0289644 kg/mol 

    # pres atmospheric pressure
    r = 8.31447
    m = 0.0289644
    
    ta = ta+273.15     ## celsius to kelvin 
    p = pres
    airds = p*m/r/ta
    airds = 1.225 if airds>1.225 else airds
    return airds


def atm_p(ta, elev):
    """Function to calculate atmospheric pressure
   Args:
       ta: Air Temperature (deg. C)
       elev: Elevation (m)
   Returns:
       Atmospheric Pressure (kPa)
   """

    atmp = 101.3*pow((T_abs + ta -0.0065*elev)/(T_abs + ta),5.26)  ## S2.10 kPa 
    return atmp


def air_emissivity(ta, ea, fcd):
    """Function to calculate air emissivity
    From Satterlund 1979
   Args:
       ta: Air Temperature (deg. C)
       ea: Actual Vapor Pressure (kPa)
       fcd: Cloud Factor (see below)
   Returns:
       Air Emissivity
   """
    
    em_a = 1.08*(1.-exp(-pow(ea*10.,(ta+T_abs)/2016.)))*(1+0.22*pow(fcd,2.75))
    return em_a


def cloud_factor(K, M, lat, elev):
    """Function to calculate cloud factor
    From Satterlund 1979
   Args:
       K: incoming shortwave radiation (MJ/m2/d)
       M: Month
       lat: Latitude (deg)
       elev: Elevation (m)
   Returns:
       Cloud Factor
   """

    J = (int)(30.4*M-15)
    delta = 0.409*sin(2.*pi*J/365. - 1.39)
    lat_r = lat/180.*pi
    omega = pi/2. - atan(-tan(lat_r)*tan(delta)/sqrt(1-tan(lat_r)*tan(lat_r)*tan(delta)*tan(delta)))
    dr = 1.+0.033*cos(2.*pi/365.*J)
    
    Ket = 24./pi*4.92*dr*(omega*sin(lat_r)*sin(delta) + cos(lat_r)*cos(delta)*sin(omega))
    Kso = (0.75+2e-5*elev)*Ket
    Kr = K/Kso
    
    Kr=1. if Kr > 1. else Kr
    Kr=0. if Kr < 0. else Kr
    
    fcd = 1. - Kr
    return fcd



