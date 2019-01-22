##--------------------------------------------------------------------------
##
##			Script to read in WRF output files, extract necessary data,
##			then save into new NetCDF file (reduces file size for archiving)
##					-- GYoung
##
##--------------------------------------------------------------------------

from netCDF4 import Dataset
import numpy as np
import time 
from datetime import datetime, timedelta 
from netCDF4 import num2date, date2num 
import os

##--------------------------------------------------------------------------
##--------------------------------------------------------------------------
##---------------				IN
##--------------------------------------------------------------------------
##--------------------------------------------------------------------------

###################################
###################################
## LEM OUTPUT
###################################
###################################

run1 = 120
info1 = 'C86_Ocean'

# run7='120';		YES
# info7='C86';

# run8='135';		YES
# info8='D10';

# run9='143';		YES
# info9='ACC';

## /gws/nopw/j04/ncas_weather/gyoung/ACCACIA/ModellingScripts/mod_obs_comp_noNice.m


###################################
# Define time dump separation
###################################

hours = np.array([7,11,15,19,23,27,31,35,39,43,47,51])

# os.chdir("../LEM/r1")

L_vap = 2.5e6    # J/kg
L_sub = 2.836e6  # J/kg
cp = 1004.6      # J/kg.K

###################################
# Load in data
###################################

nc1 = {}		# define nc1 as a dictionary
strg1 = "%2.f" % run1 

filedir = '/gws/nopw/j04/ncas_weather/gyoung/ACCACIA/LEM/r'
rundir = "".join([filedir,strg1,'/'])

for i in range(0, len(hours)):
	strg2 = "%02d" % hours[i] # string of hour index
	a1 = ''.join([rundir,'RUN0',strg1,'_00',strg2,'.nc']) # string of filename
	strgi = "%1.f" % (i+1) # string of hour number
	nc1[strgi] = Dataset(a1,'r')

# ###################################
# # Pick file
# ###################################
# filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/31_DeMott_WATSAT_eta70_MYNN/wrfout_d02_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/31_DeMott_WATSAT_eta70_MYNN/wrfout_d01_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/30_DeMott_WATSAT_HM_noThresh_eta70_MYNN/wrfout_d02_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/30_DeMott_WATSAT_HM_noThresh_eta70_MYNN/wrfout_d01_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/36_DeMott_WATSAT_2xHM_noThresh_eta70_MYNN/wrfout_d02_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/36_DeMott_WATSAT_2xHM_noThresh_eta70_MYNN/wrfout_d01_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/57_DeMott_WATSAT_5xHM_noThresh_eta70_MYNN/wrfout_d02_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/57_DeMott_WATSAT_5xHM_noThresh_eta70_MYNN/wrfout_d01_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/56_DeMott_WATSAT_10xHM_noThresh_eta70_MYNN/wrfout_d02_2015-11-27_00:00:00'
# # filename1 = '/data/scihub-users/giyoung/PWRF_V3.6.1/RUNS/MAC_WRF/56_DeMott_WATSAT_10xHM_noThresh_eta70_MYNN/wrfout_d01_2015-11-27_00:00:00'

# runlabel_start = filename1.find('/MAC_WRF/') + 9
# runlabel_end = filename1.find('/wrfout',runlabel_start)
# runlabel = filename1[runlabel_start:runlabel_end]

# if runlabel == '31_DeMott_WATSAT_eta70_MYNN':
# 	runlab = 'CNTRL'
# if runlabel == '30_DeMott_WATSAT_HM_noThresh_eta70_MYNN':
# 	runlab = 'NoThresh'
# if runlabel == '36_DeMott_WATSAT_2xHM_noThresh_eta70_MYNN':
# 	runlab = '2xHM'
# if runlabel == '57_DeMott_WATSAT_5xHM_noThresh_eta70_MYNN':
# 	runlab = '5xHM'
# if runlabel == '56_DeMott_WATSAT_10xHM_noThresh_eta70_MYNN':
# 	runlab = '10xHM'

###################################
## Read in NetCDF variables to usable variables
###################################

## Define dictionaries
ice_num1 = {}; liqmass1 = {}; temp_K1 = {}; incloud1 = {}

for i in range(0, len(hours)):
	strgi = "%1.f" % (i+1) # string of hour number
	ice_num1[strgi] = (nc1[strgi]['QBAR07'][:]+nc1[strgi]['QBAR08'][:]+nc1[strgi]['QBAR09'][:])			# Nisg m-3
	liqmass1[strgi] = (nc1[strgi]['QBAR02'][:]+nc1[strgi]['QBAR03'][:]) 								# Qliq(tot) kg/kg
	temp_K1[strgi] = nc1[strgi]['ALL_TEMP'][:]															# Temp K
	pres1[strgi] = nc1[strgi]['PREFN'][:]																# Pressure Pa
	evs1[strgi] = (0.611*np.exp(17.27*(temp_K1[strgi]-273.15)/((temp_K1[strgi]-273.15)+237.3)))*1000
	qvs1[strgi] = (0.622*evs1[strgi])/(pres1[strgi]-evs1[strgi])
	rh1[strgi] = ((watvap1[strgi]/1000)/qvs1[strgi])*100
	incloud1[strgi] = (rh1[strgi]>=100).nonzero()
timesec1 = (nc1['12']['TIMES'][:])/3600
Z1 = nc1['12']['ZN'][:]																					# Z m
X1 = nc1['12']['XN'][:]																					# X m
Y1 = nc1['12']['YN'][:]																					# Y m
times=np.arange(1,13)

##--------------------------------------------------------------------------
##--------------------------------------------------------------------------
##---------------				OUT
##--------------------------------------------------------------------------
##--------------------------------------------------------------------------

###################################
## Open File
###################################
outfile = "".join([info1,'.nc'])
dataset =  Dataset(outfile, 'w', format ='NETCDF4_CLASSIC') 

print dataset.file_format 

###################################
## Global Attributes
###################################
desc = runlab + ' simulation from Young et al., 2017 (ACP). x/y grid size = 120m with 105 vertical levels (20m resolution up to 1500m, then 50m resolution between 1500m and 3000m). Domain size = 16km x 16km.'
dataset.description = desc
dataset.history = 'Created ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dataset.source = 'UK Met Office Large Eddy Model (LEM), version 2.4, coupled with the Morrison et al., 2005 (JAS) microphysics scheme (ported from the Weather Research and Forecasting model).' 
dataset.references = 'First published in Young et al., 2017 (ACP): Microphysical sensitivity of coupled springtime Arctic stratocumulus to modelled primary ice over the ice pack, marginal ice, and ocean. (doi:10.5194/acp-17-4209-2017)'
dataset.project = 'Aerosol-Cloud Coupling and Climate Interactions in the Arctic (ACCACIA), funded by the UK Natural Environment Research Council (Grant no. NE/I028696/1).'
dataset.comment = 'Other LEM variables from this simulation are archived locally at the University of Manchester. Contact Gillian Young (G.Young1@leeds.ac.uk) for details.'
dataset.institution = 'University of Manchester.'

###################################
## Switch off automatic filling 
###################################
dataset.set_fill_off()

# ###################################
# ## Data dimensions
# ###################################
# time = dataset.createDimension('time', np.size(data1['xlat'],0))
# level = dataset.createDimension('level', np.size(data1['theta'],1)) 
# lat = dataset.createDimension('lat', data1['y_dim'])
# lon = dataset.createDimension('lon', data1['x_dim']) 

# ###################################
# ## Dimensions variables
# ###################################
# times = dataset.createVariable('time', np.float32, ('time',),fill_value='-9999') 
# levels = dataset.createVariable('level', np.int32, ('level',),fill_value='-9999') 
# latitudes = dataset.createVariable('latitude', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# longitudes = dataset.createVariable('longitude', np.float32, ('time','lat','lon',),fill_value='-9999') 

# ###################################
# ## Create 3-d variables
# ###################################
# swdnb = dataset.createVariable('swdnb', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# swdnbc = dataset.createVariable('swdnbc', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# lwdnb = dataset.createVariable('lwdnb', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# lwdnbc = dataset.createVariable('lwdnbc', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# swupb = dataset.createVariable('swupb', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# swupbc = dataset.createVariable('swupbc', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# lwupb = dataset.createVariable('lwupb', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# lwupbc = dataset.createVariable('lwupbc', np.float32, ('time','lat', 'lon',),fill_value='-9999')
# seaice = dataset.createVariable('seaice', np.float32, ('time','lat', 'lon',),fill_value='-9999')

# ###################################
# ## Create 4-d variables
# ###################################
# temperature = dataset.createVariable('temperature', np.float32, ('time','level','lat','lon'),fill_value='-9999') 
# theta = dataset.createVariable('theta', np.float32, ('time','level','lat','lon'),fill_value='-9999') 
# height = dataset.createVariable('height', np.float32, ('time','level','lat','lon'),fill_value='-9999') 
# pressure = dataset.createVariable('pressure', np.float32, ('time','level','lat','lon'),fill_value='-9999') 
# rho = dataset.createVariable('rho', np.float32, ('time','level','lat','lon'),fill_value='-9999') 

# qcloud = dataset.createVariable('qcloud', np.float32, ('time','level','lat','lon'),fill_value='-9999') 
# nisg =  dataset.createVariable('nisg', np.float32, ('time','level','lat','lon'),fill_value='-9999') 
# nisg100 =  dataset.createVariable('nisg100', np.float32, ('time','level','lat','lon'),fill_value='-9999') 

# ###################################
# ## 3-d variables: standard names
# # ###################################
# swdnb.standard_name = 'surface_downwelling_shortwave_flux_in_air'
# swdnbc.standard_name = 'surface_downwelling_shortwave_flux_in_air_assuming_clear_sky'
# lwdnb.standard_name = 'surface_downwelling_longwave_flux_in_air'
# lwdnbc.standard_name = 'surface_downwelling_longwave_flux_in_air_assuming_clear_sky'
# swupb.standard_name = 'surface_upwelling_shortwave_flux_in_air'
# swupbc.standard_name = 'surface_upwelling_shortwave_flux_in_air_assuming_clear_sky'
# lwupb.standard_name = 'surface_upwelling_longwave_flux_in_air'
# lwupbc.standard_name = 'surface_upwelling_longwave_flux_in_air_assuming_clear_sky'
# seaice.standard_name = 'sea_ice_area_fraction'

# # ###################################
# # ## Create 4-d variables
# # ###################################
# temperature.standard_name = 'air_temperature'
# theta.standard_name = 'air_potential_temperature'
# height.standard_name = 'height'
# pressure.standard_name = 'air_pressure'
# rho.standard_name = 'air_density'

# W.standard_name = 'vertical_wind_speed'
# qvapor.standard_name = 'humidity_mixing_ratio'
# qcloud.standard_name = 'cloud_liquid_water_mixing_ratio'
# qrain.standard_name = 'rain_water_mixing_ratio'
# qisg.standard_name = 'cloud_ice_mixing_ratio'
# nisg.standard_name = 'number_concentration_of_ice_crystals_in_air'
# nisg80.long_name = 'number_concentration_of_ice_crystals_larger_than_80micron_in_air'
# nisg50.long_name = 'number_concentration_of_ice_crystals_smaller_than_50micron_in_air'

# ###################################
# ## Variable Attributes  
# ###################################
# times.units = 'hours since 2015-11-27 00:00:00'  
# times.calendar = 'gregorian' 
# levels.units = 'm' 
# latitudes.units = 'degree_north'  
# longitudes.units = 'degree_east'  

# swdnb.units = 'W m-2'
# swdnbc.units = 'W m-2'
# lwdnb.units = 'W m-2'
# lwdnbc.units = 'W m-2'
# swupb.units = 'W m-2'
# swupbc.units = 'W m-2'
# lwupb.units = 'W m-2'
# lwupbc.units = 'W m-2'
# seaice.units = ''

# temperature.units = 'K' 
# theta.units = 'K' 
# height.units = 'm'
# pressure.units = 'Pa'
# rho.units = 'kg m-3'

# W.units = 'm s-1'
# qvapor.units = 'kg kg-1'
# qcloud.units = 'kg kg-1'
# qrain.units = 'kg kg-1'
# qisg.units = 'kg kg-1'
# nisg.units = 'kg-1'
# nisg80.units = 'kg-1'
# nisg50.units = 'kg-1'


# ###################################
# ## Ice comments
# ###################################
# qisg.comment = 'Sum of ice + snow + graupel particle categories'
# nisg.comment = 'Sum of ice + snow + graupel particle categories'
# nisg80.comment = 'Sum of ice + snow + graupel particle categories. Particle sizes calculated online following the assumption that each hydrometeor class is represented by a Gamma distribution.'
# nisg50.comment = 'Sum of ice + snow + graupel particle categories. Particle sizes calculated online following the assumption that each hydrometeor class is represented by a Gamma distribution.'

# ###################################
# ## Fill in times
# ###################################
# # dates = [] 
# # for n in range(temp.shape[0]): 
# # 	dates.append(datetime(2015, 11, 27) + n * timedelta(hours=0)) 
# # 	times[:] = date2num(dates, units = times.units, calendar = times.calendar) 
# # print 'time values (in units %s): ' % times.units + '\n', times[:] 

# wrftime = nc1.variables['Times']
# tim = np.zeros(np.size(data1['Tk'],0))
# for i in range(np.size(data1['Tk'],0)):
# 	str_times = wrftime[i][11:]
# 	tim[i] = (np.int(str_times[0])*600 + np.int(str_times[1])*60 + np.int(str_times[3])*10)/float(60)

# ###################################
# ## Fill arrays
# ###################################
# times[:] = tim[:]
# levels[:] = np.arange(0,np.size(data1['Z'],1))
# latitudes[:,:,:] = data1['xlat'][:,:,:]
# longitudes[:,:,:] = data1['xlon'][:,:,:]

# swdnb[:,:,:] = data1['swdnb'][:,:,:]
# swdnbc[:,:,:] = data1['swdnbc'][:,:,:]
# lwdnb[:,:,:] = data1['lwdnb'][:,:,:]
# lwdnbc[:,:,:] = data1['lwdnbc'][:,:,:]
# swupb[:,:,:] = data1['swupb'][:,:,:]
# swupbc[:,:,:] = data1['swupbc'][:,:,:]
# lwupb[:,:,:] = data1['lwupb'][:,:,:]
# lwupbc[:,:,:] = data1['lwupbc'][:,:,:]
# seaice[:,:,:] = data1['seaice'][:,:,:]

# temperature[:,:,:,:] = data1['Tk'][:,:,:,:]
# theta[:,:,:,:] = data1['theta'][:,:,:,:]
# height[:,:,:,:] = data1['Z'][:,:,:,:]
# pressure[:,:,:,:] = data1['p'][:,:,:,:]
# rho[:,:,:,:] = data1['rho'][:,:,:,:]

# W[:,:,:,:] = data1['w'][:,:,:,:]
# qvapor[:,:,:,:] = data1['qvap'][:,:,:,:]
# qcloud[:,:,:,:] = data1['qcloud'][:,:,:,:]
# qrain[:,:,:,:] = data1['qrain'][:,:,:,:]
# qisg[:,:,:,:] = data1['qisg'][:,:,:,:]
# nisg[:,:,:,:] = data1['qnisg'][:,:,:,:]
# nisg80[:,:,:,:] = data1['nisg80'][:,:,:,:]
# nisg50[:,:,:,:] = data1['nisg50'][:,:,:,:]

###################################
## Write out file
###################################
dataset.close()