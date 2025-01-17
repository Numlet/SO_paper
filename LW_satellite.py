#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 10:39:59 2017

@author: eejvt
"""

from base_imports import *

LW_satellite_dict=OrderedDict()
LW_satellite_dict_wc=OrderedDict()

path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/'
from scipy.io import netcdf

#==============================================================================
# C1 AQUA
#==============================================================================


mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r') 
mb=netcdf.netcdf_file(path+'CERES/'+'CERES_SSF_NPP-XTRK_Edition1A_Subset_2015030100-2015030223.nc','r') 

mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_NPP-XTRK_Edition1A_Subset_2015030100-2015031904.nc','r') 
mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r') 
times_ceres=mb.variables['time'].data*24*60*60




LW=np.copy(mb.variables['CERES_LW_TOA_flux___upwards'].data)
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data

ti=16#h
te=17#h

tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
t0=(datetime.datetime(2015,03,1,0)-datetime.datetime(1970,1,1)).total_seconds()
#sat_LW=(times_ceres[times_range]-t0)/60./60.
sim_path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/'

cube_DM10 =  iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0]

#LW_dict[c2]

reload(stc)
model_lons,model_lats=stc.unrotated_grid(cube_DM10)
#times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
sat_lon=lon[times_range]
sat_lat=lat[times_range]
sat_LW=LW[times_range]
#sat_LW=(times_ceres[times_range]-t0)/60./60.
coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)
#Xo,Yo=np.meshgrid(lon_old,lat_old)
plt.figure()
#data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
#grid_z0 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='nearest')
grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
#plt.contourf(X,Y, grid_z1,levels_LW)
plt.contourf(X,Y, grid_z1)
plt.colorbar()
sat_cube=cube_DM10[16,:,:]
sat_cube.data=grid_z1
LW_satellite_dict['C1_SATELLITE']=grid_z1



#%%
#X,Y=np.meshgrid(sat_lon,sat_lat)
#folder='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/GLOBAL/All_time_steps/'
#
##plt.contourf(sat_lon,sat_lat,sat_LW)
#cube=iris.load(folder+'All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0]
#
#cut_lon=model_lons[cut_value]
#cut_lon2=model_lons[cut_value2]
#ti=9#h
#te=19#h
#
#tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
#tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()
#
#t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
#t0=(datetime.datetime(2015,03,1,0)-datetime.datetime(1970,1,1)).total_seconds()
#
#sim_path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/'
#
#cube_DM10 =  iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0]
#
##LW_dict[c2]
#
#reload(stc)
#model_lons,model_lats=stc.unrotated_grid(cube_DM10)
##times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
#times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
#
#global_lats=cube.coord('latitude').points
#
#global_lons=cube.coord('longitude').points
#global_lons2=np.array(global_lons)
#global_lons2[global_lons>180]=global_lons[global_lons>180]-360
#global_lons=global_lons2
#
#
#sat_lon=lon[times_range]
#sat_lat=lat[times_range]
##sat_LW=LW[times_range]
#sat_LW=(times_ceres[times_range]-t0)/60./60.
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
##model_lons=np.linspace(-5,20,500)
#X,Y=np.meshgrid(global_lons, global_lats)
##Xo,Yo=np.meshgrid(lon_old,lat_old)
#plt.figure()
##data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
##grid_z0 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='nearest')
#grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
##plt.contourf(X,Y, grid_z1,levels_LW)
#grid_z1[grid_z1>1000]=np.nan
#plt.contourf(X,Y, grid_z1)
#plt.colorbar()

#%%
#mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_NPP-XTRK_Edition1A_Subset_2015030100-2015030223.nc','r') 

#==============================================================================
# C1 WHOLE CYCLONE 
#==============================================================================
mb=netcdf.netcdf_file(path+'CERES/'+'CERES_SSF_NPP-XTRK_Edition1A_Subset_2015030100-2015030223.nc','r') 
mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r') 

times_ceres=mb.variables['time'].data*24*60*60


LW=np.copy(mb.variables['CERES_LW_TOA_flux___upwards'].data)
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data

ti=14#h
te=17#h

tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]
model_lons,model_lats=stc.unrotated_grid(cube_wc)

cube_wc=cube_wc[:,:,150:]
model_lons=model_lons[150:]

#times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
sat_lon=lon[times_range]
sat_lat=lat[times_range]
sat_LW=LW[times_range]
coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)
#Xo,Yo=np.meshgrid(lon_old,lat_old)
#data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
#grid_z0 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='nearest')
grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
grid_z1[grid_z1>1000]=np.nan
plt.figure()
#plt.imshow(grid_z1)
#plt.show()
#model_lons,model_lats=stc.unrotated_grid(cube_high_res)
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)

#plt.title(name)
#plt.xlabel('Longitude')
#CS=plt.contourf(X,Y,grid_z1) 
#sat_cube=cube_DM10[16,:,:]
#sat_cube.data=grid_z1
LW_satellite_dict_wc['C1_SATELLITE']=grid_z1



#%%
#==============================================================================
# C2
#==============================================================================
path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/'
from scipy.io import netcdf
mb=netcdf.netcdf_file(path+'CERES/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015011000-2015011123.nc','r') 

times_ceres=mb.variables['time'].data*24*60*60
LW=np.copy(mb.variables['CERES_LW_TOA_flux___upwards'].data)
#LW[LW>1400]=0
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data

ti=15#h
te=18#h

tdi=(datetime.datetime(2015,01,10,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,01,10,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,01,10,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
    
sim_path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/'

cube_DM10 = iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0]
#LW_dict['C3_SATELLITE']=np.nanmean(grid_z1)
reload(stc)
model_lons,model_lats=stc.unrotated_grid(cube_DM10)
#times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
sat_lon=lon[times_range]
sat_lat=lat[times_range]
sat_LW=LW[times_range]
coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)
#Xo,Yo=np.meshgrid(lon_old,lat_old)
#data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
#grid_z0 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='nearest')
grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
LW_satellite_dict['C2_SATELLITE']=grid_z1
#%%

#==============================================================================
# C3
#==============================================================================

path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
from scipy.io import netcdf
cubes  =iris.load(path+'ceres/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc')
mb=netcdf.netcdf_file(path+'ceres/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc','r') 
mb=netcdf.netcdf_file(path+'ceres_all_SO/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc','r') 

#LW=cubes[1]
#model_lons=np.arange(-0.02*250,250*0.02,0.02)[0:]
#model_lats=np.arange(-0.02*250-52,250*0.02-52,0.02)

#model_lons=np.linspace(-7,17)
#model_lats=np.linspace(-47.5,-58)
times_ceres=mb.variables['time'].data*24*60*60



#model_lons=model_lons+lon_offset

LW=np.copy(mb.variables['CERES_LW_TOA_flux___upwards'].data)
#LW[LW>1400]=0
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data

ti=13#h
te=15#h

tdi=(datetime.datetime(2014,12,9,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2014,12,9,te)-datetime.datetime(1970,1,1)).total_seconds()

t13=(datetime.datetime(2014,12,9,14)-datetime.datetime(1970,1,1)).total_seconds()/3600.
cube = iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/All_time_steps/','m01s01i208'))[0]

reload(stc)
model_lons,model_lats=stc.unrotated_grid(cube)
#times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
sat_lon=lon[times_range]
sat_lat=lat[times_range]
sat_LW=LW[times_range]
coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)
#Xo,Yo=np.meshgrid(lon_old,lat_old)
#data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
#grid_z0 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='nearest')
grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')

LW_satellite_dict['C3_SATELLITE']=grid_z1
