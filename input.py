import numpy as np
import os

## Constants ##

kboltz = 1.38064852e-16    # Boltzmann's constant
amu = 1.660539040e-24      # atomic mass unit
gamma = 0.57721
rjup = 7.1492e9            # equatorial radius of Jupiter
rsun = 6.9566e10           # solar radius
rearth = 6.378e8            # earth radius
pressure_probed = 1e-2      # probed pressure in bars
# pressure_cia = 1e-2         # pressure for cia in bars
# m = 2.4*amu                 # assummed hydrogen-dominated atmosphere
m_water = 18.0*amu          # mean molecular mass of any molecules you want to consider
m_cyanide = 27.0*amu
m_ammonia = 17.0*amu
m_methane = 16.0*amu
m_carbon_monoxide = 28.0*amu


## Planet Data ##

planet_name = 'WASP-17b'

g = 316
g_uncertainty = 20
rstar = 1.583
rstar_uncertainty = 0.041
r0 = 1.709   # Rp = [1.88,1.99]
r0_uncertainty = 0.28   # R0 = [1.43,1.99]

wavelength_bins = np.array([1.114, 1.142, 1.170, 1.198, 1.226, 1.254, 1.282, 1.311, 1.339, 1.367, 1.395, 1.423, 1.451, 1.479, 1.507, 1.535, 1.563, 1.592, 1.62, 1.648]) # must be 1 longer than transit_depth and transit_depth_error
transit_depth = np.array([1.5087, 1.4867, 1.5044, 1.4957, 1.4998, 1.5166, 1.4822, 1.5362, 1.5545, 1.5686, 1.5050, 1.5578, 1.5446, 1.5300, 1.5086, 1.5410, 1.5534, 1.4875, 1.4530])
transit_depth_error = np.array([0.0257, 0.0250, 0.0259, 0.0216, 0.0222, 0.0226, 0.0237, 0.0197, 0.0223, 0.0239, 0.0261, 0.0250, 0.0267, 0.0247, 0.0229, 0.0316, 0.0282, 0.0278, 0.0303])
pmin = 1e-6



## Retrieval info ##

model_name = 'greycloud'

molecules = ['1H2-16O__POKAZATEL_e2b']  # list of molecules (determines which opacity tables are loaded)
parameters = ["T", "log_xh2o", "R0", "log_kappa_cloud", "log_P_cloudtop", "Rstar", "G"]   # parameters you wish to retrieve (MUST MATCH MOLECULES)
res = 2         # resolution used for opacities
live = 1000     # live points used in nested sampling
wavenumber=True     # True if opacity given in terms of wavenumber, False if wavelength

priors = {"T": [2700, 200], "log_xh2o": [13,-13], "log_xch4": [13,-13], "log_xco": [13,-13], "log_kappa_cloud": [14,-12], "log_P0": [4,-1], "log_kappa_0": [9,-10], "Q0": [99,1], "a": [3,3], "R0": [2*r0_uncertainty, r0-r0_uncertainty], "log_r_c": [6,-7], "log_p_cia": [3,-3], "log_P_cloudtop": [1,-3], "Rstar": [2*rstar_uncertainty,rstar-rstar_uncertainty], "G": [2*g_uncertainty,g-g_uncertainty], "line": [5,0]} # priors for all possible parameters



## info for all possible parameters ##
molecular_name_dict = {'1H2-16O__POKAZATEL_e2b': 'water', '12C-1H4__YT10to10_e2b': 'methane', '12C-16O__Li2015_e2b': 'carbon_monoxide'}  # dictionary list of all possible molecules and corresponding names
molecular_abundance_dict = {'1H2-16O__POKAZATEL_e2b': 'log_xh2o', '12C-1H4__YT10to10_e2b': 'log_xch4', '12C-16O__Li2015_e2b': 'log_xco'}  # dictionary list of all possible molecules and corresponding abundance names

parameter_dict = {"T": 1000, "log_xh2o": "Off", "log_xch4": "Off", "log_xco": "Off", "log_kappa_cloud": "Off", "R0": r0, "Rstar": rstar, "log_P0": 1, "log_kappa_0": "Off", "Q0": "Off", "a": "Off", "log_r_c": "Off", "log_p_cia": -2, "log_P_cloudtop": "Off", "G": g, "line": "Off"}    # default parameter values used if not retrieved

molecular_mass_dict = {'1H2-16O__POKAZATEL_e2b': m_water, '12C-1H4__YT10to10_e2b': m_methane, '12C-16O__Li2015_e2b': m_carbon_monoxide}   # dictionary of molecules and their mean molecular masses
temperature_array = np.r_[50:700:50, 700:1500:100, 1500:3100:200]
#temperature_array = np.array([1500, 1700, 1900, 2100])
#temp_dict = {'01': temperature_array[9:], '12C-1H4__YT10to10_e2b': temperature_array[9:], '12C-16O__HITEMP2010_e2b': temperature_array}   # temperature values for corresponding opacity tables
temperature_array_cia = np.r_[200:3025:25]          # temperature array for CIA table
opacity_path = os.environ['HOME'] + "/Desktop/PhD/OPACITIES/"  # path to opacity binary files
cia_path = os.environ['HOME'] + "/Desktop/PhD/HITRAN/"      # path to CIA files
