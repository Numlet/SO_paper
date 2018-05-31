#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 09:58:20 2017

@author: eejvt
"""

from base_imports import *


plt.figure(figsize=(20,5))
cmap=plt.cm.RdBu_r
#levels_SW=np.linspace(0,800,15).tolist()
levels_SW=np.linspace(0,750,15).tolist()
levels_SW=np.linspace(253,273,21).tolist()

plt.subplot(1,4,1)
mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r') 

times_ceres=mb.variables['time'].data*24*60*60


LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data
cut_value=375
#primer pase a las 14.50 
#segundo pase a las 16.30
ti=14#h
te=15#h

tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]
model_lons,model_lats=stc.unrotated_grid(cube_wc)

#cube_wc=cube_wc[:,:,150:]
#model_lons=model_lons[150:]

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
#grid_z0 = sc.interpolate.griddata(coord, sat_SW, (X,Y), method='nearest')
grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
grid_z1[grid_z1>1000]=np.nan
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
grid_z1[:,:cut_value]=np.nan
plt.axvline(model_lons[cut_value],lw=5,c='k',ls='--')
#plt.title(name)
plt.xlabel('Longitude')
CS=plt.contourf(X,Y,grid_z1,levels_SW,cmap=cmap) 
#plt.colorbar()
#plt.subplot(1,4,1)

mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r') 

times_ceres=mb.variables['time'].data*24*60*60


LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data

#primer pase a las 14.50 
#segundo pase a las 16.30
ti=15#h
te=17#h

tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]
model_lons,model_lats=stc.unrotated_grid(cube_wc)

#cube_wc=cube_wc[:,:,150:]
#model_lons=model_lons[150:]

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
#grid_z0 = sc.interpolate.griddata(coord, sat_SW, (X,Y), method='nearest')
grid_z2 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
grid_z2[grid_z1>1000]=np.nan

grid_z2[:,cut_value:]=np.nan


#model_lons=model_lons[170:]
#plt.figure()
#plt.imshow(grid_z1)
#plt.show()
#model_lons,model_lats=stc.unrotated_grid(cube_high_res)
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
#plt.axvline(model_lons[cut_value],lw=5,c='k')
#plt.title(name)
plt.xlabel('Longitude')
CS=plt.contourf(X,Y,grid_z2,levels_SW,cmap=cmap) 
#plt.colorbar()
#sat_cube=cube_DM10[16,:,:]
#sat_cube.data=grid_z1
#SW_satellite_dict_wc['C1_SATELLITE']=grid_z1

cube_small=stc.clean_cube(iris.load('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/GLO_MEAN/All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0],50)
model_lons_small,model_lats_small=stc.unrotated_grid(cube_small)

from matplotlib.patches import Rectangle

someX, someY = 0.5, 0.5
#plt.figure()
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))
plt.ylim(-70,-50)
plt.xlim(-50,5.5)
#currentAxis.add_patch(Rectangle((model_lats_small.max(), someY - .1), 0.2, 0.2, fill=None, alpha=1))
plt.show()

plt.ylabel('Latitude')
#%%

folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/MEYERS/L1/'
#folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/PRESENTDAY_DUST/All_time_steps/'


cube=iris.load(folder+'L1_CTT_Cloud_top_temperature.nc')[0]

latitude=cube.coord('grid_latitude')

longitude=cube.coord('grid_longitude')


lons,lats=unrotated_grid(cube)


#latitude.points=lats

#cube.remove_dimensions
from iris.coords import DimCoord
#latitude = DimCoord(lats,
#                    standard_name='latitude',
#                    units='degrees')
#longitude = DimCoord(lons,
#                      standard_name='longitude',
#                      units='degrees')
#>>> cube = Cube(np.zeros((4, 8), np.float32),
#...             dim_coords_and_dims=[(latitude, 0),
#...                                  (longitude, 1)])
model_lons,model_lats=unrotated_grid(cube)
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
plt.subplot(1,4,3)
#plt.title(name)

plt.xlabel('Longitude')
itime2=15
itime1=17
data1=cube[itime1,:,:].data
data1[:,cut_value:]=np.nan
CS=plt.contourf(X,Y,data1,levels_SW,cmap=cmap) 

data2=cube[itime2,:,:].data
data2[:,:cut_value]=np.nan
CS=plt.contourf(X,Y,data2,levels_SW,cmap=cmap) 
plt.axvline(model_lons[cut_value],lw=5,c='k',ls='--')
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))


#CS=plt.contourf(X,Y,cube[itime2,:,:].data) 
#        plt.clabel(CS, inline=1, fmt='%1.0f')
#plt.colorbar()
plt.ylim(-70,-50)
#plt.ylim(-70,-45)
#plt.xlim(-50,5.5)
#%%
folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/L1/'
#folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/PRESENTDAY_DUST/All_time_steps/'


cube=iris.load(folder+'L1_CTT_Cloud_top_temperature.nc')[0]

latitude=cube.coord('grid_latitude')

longitude=cube.coord('grid_longitude')


lons,lats=unrotated_grid(cube)


#latitude.points=lats

#cube.remove_dimensions
from iris.coords import DimCoord
#latitude = DimCoord(lats,
#                    standard_name='latitude',
#                    units='degrees')
#longitude = DimCoord(lons,
#                      standard_name='longitude',
#                      units='degrees')
#>>> cube = Cube(np.zeros((4, 8), np.float32),
#...             dim_coords_and_dims=[(latitude, 0),
#...                                  (longitude, 1)])
model_lons,model_lats=unrotated_grid(cube)
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
ax=plt.subplot(1,4,4)
#plt.title(name)
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.xlabel('Longitude')
itime2=15
itime1=17
data1=cube[itime1,:,:].data
data1[:,cut_value:]=np.nan
CS=plt.contourf(X,Y,data1,levels_SW,cmap=cmap) 

data2=cube[itime2,:,:].data
data2[:,:cut_value]=np.nan
im=plt.contourf(X,Y,data2,levels_SW,cmap=cmap) 
plt.axvline(model_lons[cut_value],lw=5,c='k',ls='--')
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))

plt.ylim(-70,-50)
#plt.ylim(-70,-45)
#plt.xlim(-50,5.5)

#CS=plt.contourf(X,Y,cube[itime2,:,:].data) 
#        plt.clabel(CS, inline=1, fmt='%1.0f')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)

cb=plt.colorbar(im, cax=cax)
#            cb=plt.colorbar()
cb.set_label('$W/m^2$')
#%%
folder='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/GLOBAL/L1/'
#folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/PRESENTDAY_DUST/All_time_steps/'
#plt.figure(figsize=(20,5))
plt.subplot(1,4,2)


cube=iris.load(folder+'L1_CTT_Cloud_top_temperature.nc')[0]

cut_lon=model_lons[cut_value]


global_lats=cube.coord('latitude').points

global_lons=cube.coord('longitude').points
global_lons2=np.array(global_lons)
global_lons2[global_lons>180]=global_lons[global_lons>180]-360
global_lons=global_lons2
cut_value_glob=jl.find_nearest_vector_index(global_lons,cut_lon)

#lons,lats=unrotated_grid(cube)


#latitude.points=lats

#cube.remove_dimensions
from iris.coords import DimCoord
#latitude = DimCoord(lats,
#                    standard_name='latitude',
#                    units='degrees')
#longitude = DimCoord(lons,
#                      standard_name='longitude',
#                      units='degrees')
#>>> cube = Cube(np.zeros((4, 8), np.float32),
#...             dim_coords_and_dims=[(latitude, 0),
#...                                  (longitude, 1)])
#model_lons,model_lats=unrotated_grid(cube)
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(global_lons, global_lats)
#plt.subplot(1,4,2)
#plt.title(name)

plt.xlabel('Longitude')
itime2=15
itime1=17




data1=cube[itime1,:,:].data
data1[:,cut_value_glob:]=np.nan
data1[:,:200]=np.nan
CS=plt.contourf(X,Y,data1,levels_SW,cmap=cmap) 



data2=cube[itime2,:,:].data
data2[:,300:cut_value_glob]=np.nan
CS=plt.contourf(X,Y,data2,levels_SW,cmap=cmap) 

plt.axvline(model_lons[cut_value],lw=5,c='k',ls='--')

#
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))

#CS=plt.contourf(X,Y,cube[itime2,:,:].data) 
#        plt.clabel(CS, inline=1, fmt='%1.0f')
#plt.colorbar()
plt.ylim(-70,-50)
#plt.ylim(-70,-45)
plt.xlim(-50,5.5)
#cube.remove_coord('grid_latitude')
#cube.remove_coord('grid_longitude')
#pole_lat=cube.coord('grid_longitude').coord_system.grid_north_pole_latitude
#pole_lon=cube.coord('grid_longitude').coord_system.grid_north_pole_longitude
#%%

#
#lons, lats =iris.analysis.cartography.unrotate_pole(cube.coord('grid_longitude').points,cube.coord('grid_latitude').points,0,90-58)
#print lons.max(),lons.min()
#print lats.max(),lats.min()
#
