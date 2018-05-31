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
levels_SW=np.linspace(0,700,15).tolist()
import matplotlib.ticker as plticker

loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
#ax.xaxis.set_major_locator(loc)

ylim1=-73
ylim2=-38

xlim1=-95
xlim2=17


ylim1=-70
ylim2=-48

xlim1=-62
xlim2=15



ax=plt.subplot(1,4,1)
mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_NPP-XTRK_Edition1A_Subset_2015030100-2015031904.nc','r')
mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r')

times_ceres=mb.variables['time'].data*24*60*60


LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data

#primer pase a las 14.50
#segundo pase a las 16.30
ti=14#h
te=15#h

tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]
cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN_SECOND_DOMAIN/All_time_steps/','m01s01i208'))[0]
cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN_THIRD_DOM/All_time_steps/','m01s01i208'))[0]
model_lons,model_lats=stc.unrotated_grid(cube_wc)

cut_value=375
lon1=-10
lon2=-45
cut_value=jl.find_nearest_vector_index(model_lons,lon1)
cut_value2=jl.find_nearest_vector_index(model_lons,lon2)

lonline1=model_lons[cut_value]
lonline2=model_lons[cut_value2]
#cube_wc=cube_wc[:,:,150:]
#model_lons=model_lons[150:]

#times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
sat_lon=lon[times_range]
sat_lat=lat[times_range]
print datetime.datetime.fromtimestamp(times_ceres[times_range][0])
print datetime.datetime.fromtimestamp(times_ceres[times_range][-1])

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
#grid_z1[:,:cut_value]=np.nan
plt.axvline(model_lons[cut_value],lw=3,c='k',ls='--')
#plt.title(name)
plt.xlabel('Longitude')
CS=plt.contourf(X,Y,grid_z1,levels_SW,cmap=cmap)
#plt.colorbar()
#plt.subplot(1,4,1)

mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_NPP-XTRK_Edition1A_Subset_2015030100-2015031904.nc','r')
mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r')

times_ceres=mb.variables['time'].data*24*60*60


LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data

#primer pase a las 14.50
#segundo pase a las 16.30
ti=16#h
te=17#h


tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
#cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]
model_lons,model_lats=stc.unrotated_grid(cube_wc)

#cube_wc=cube_wc[:,:,150:]
#model_lons=model_lons[150:]

#times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
print datetime.datetime.fromtimestamp(times_ceres[times_range][0])
print datetime.datetime.fromtimestamp(times_ceres[times_range][-1])
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

plt.title('a) Satellite')
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
#plt.axvline(model_lons[cut_value],lw=3,c='k')
#plt.title(name)
plt.xlabel('Longitude')

CS=plt.contourf(X,Y,grid_z2,levels_SW,cmap=cmap)

loc = plticker.MultipleLocator(base=20) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(loc)


ti=18#h
te=19#h


tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
#cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]
model_lons,model_lats=stc.unrotated_grid(cube_wc)

#cube_wc=cube_wc[:,:,150:]
#model_lons=model_lons[150:]

#times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
print datetime.datetime.fromtimestamp(times_ceres[times_range][0])
print datetime.datetime.fromtimestamp(times_ceres[times_range][-1])
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
grid_z3 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
grid_z3[grid_z1>1000]=np.nan

grid_z3[:,cut_value2:]=np.nan


print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
#plt.axvline(model_lons[cut_value],lw=3,c='k')
#plt.title(name)
plt.xlabel('Longitude')
CS=plt.contourf(X,Y,grid_z3,levels_SW,cmap=cmap)

cube_small=stc.clean_cube(iris.load('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/GLO_MEAN/All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0],50)
model_lons_small,model_lats_small=stc.unrotated_grid(cube_small)

from matplotlib.patches import Rectangle

someX, someY = 0.5, 0.5
#plt.figure()
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))
plt.ylim(ylim1,ylim2)
plt.xlim(xlim1,xlim2)

currentAxis.add_patch(Rectangle((model_lats_small.max(), someY - .1), 0.2, 0.2, fill=None, alpha=1))
#plt.show()
plt.axvline(lonline2,lw=3,c='k',ls='--')
plt.text(-8,-65,'14.55h UTC',rotation=90,fontsize=12)
plt.text(-15,-65,'16.35h UTC',rotation=90,fontsize=12)
plt.text(-50,-65,'18.14h UTC',rotation=90,fontsize=12)
plt.text(3,-53,'Frontal Cloud',rotation=90,fontsize=14,alpha=0.8)
plt.text(-40,-65,'Low-cloud \nCold sector',fontsize=12,alpha=0.8)
plt.ylabel('Latitude')
#%%

#==============================================================================
# MEYERS
#==============================================================================

folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/MEYERS_SECOND_DOMAIN/All_time_steps/'
folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/MEYERS_SAME_DOMAIN/All_time_steps/'
folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/MEYERS_THIRD_DOM/All_time_steps/'
#folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/PRESENTDAY_DUST/All_time_steps/'


cube=iris.load(folder+'All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0]

latitude=cube.coord('grid_latitude')

longitude=cube.coord('grid_longitude')


lons,lats=unrotated_grid(cube)


#latitude.points=lats

#cube.remove_dimensions
from iris.coords import DimCoord
model_lons,model_lats=unrotated_grid(cube)
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
bx=plt.subplot(1,4,3)
#plt.title(name)

plt.xlabel('Longitude')
itime2=15
itime1=17
itime3=18


cut_value=jl.find_nearest_vector_index(model_lons,lon1)
cut_value2=jl.find_nearest_vector_index(model_lons,lon2)



data1=(cube[16,:,:].data+cube[17,:,:].data)/2
#data1=cube[itime1,:,:].data
data1[:,cut_value:]=np.nan
CS=plt.contourf(X,Y,data1,levels_SW,cmap=cmap)

data2=cube[15,:,:].data
data2[:,:cut_value]=np.nan
CS=plt.contourf(X,Y,data2,levels_SW,cmap=cmap)
plt.axvline(lonline1,lw=3,c='k',ls='--')
plt.title('c) [INP]: M92')

data3=cube[itime3,:,:].data
data3[:,cut_value2:]=np.nan
CS=plt.contourf(X,Y,data3,levels_SW,cmap=cmap)
plt.axvline(lonline2,lw=3,c='k',ls='--')
currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))


#CS=plt.contourf(X,Y,cube[itime2,:,:].data)
#        plt.clabel(CS, inline=1, fmt='%1.0f')
#plt.colorbar()
plt.ylim(ylim1,ylim2)
plt.xlim(xlim1,xlim2)
loc = plticker.MultipleLocator(base=20) # this locator puts ticks at regular intervals
bx.xaxis.set_major_locator(loc)

#%%

#==============================================================================
# VT17
#==============================================================================
folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/'
folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN_SECOND_DOMAIN/All_time_steps/'
folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN_THIRD_DOM/All_time_steps/'
#folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/PRESENTDAY_DUST/All_time_steps/'


cube=iris.load(folder+'All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0]

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
cx=plt.subplot(1,4,4)
#plt.title(name)
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.xlabel('Longitude')
itime2=15
itime1=17
itime3=18



model_lons,model_lats=unrotated_grid(cube)



cut_value=jl.find_nearest_vector_index(model_lons,lon1)
cut_value2=jl.find_nearest_vector_index(model_lons,lon2)



data1=(cube[16,:,:].data+cube[17,:,:].data)/2
#data1=cube[itime1,:,:].data
data1[:,cut_value:]=np.nan
CS=plt.contourf(X,Y,data1,levels_SW,cmap=cmap)

data2=cube[itime2,:,:].data
data2[:,:cut_value]=np.nan
im=plt.contourf(X,Y,data2,levels_SW,cmap=cmap)
plt.axvline(lonline1,lw=3,c='k',ls='--')

data3=cube[itime3,:,:].data
data3[:,cut_value2:]=np.nan
im=plt.contourf(X,Y,data3,levels_SW,cmap=cmap)
plt.axvline(lonline2,lw=3,c='k',ls='--')
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))

currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))
plt.title('d) [INP]: VT17 (Mean)')


plt.ylim(ylim1,ylim2)
plt.xlim(xlim1,xlim2)


#CS=plt.contourf(X,Y,cube[itime2,:,:].data)
#        plt.clabel(CS, inline=1, fmt='%1.0f')
divider = make_axes_locatable(cx)
cax = divider.append_axes("right", size="5%", pad=0.05)

cb=plt.colorbar(im, cax=cax)
#            cb=plt.colorbar()
cb.set_label('SW flux $\mathrm{(W/m^2)}$')

loc = plticker.MultipleLocator(base=20) # this locator puts ticks at regular intervals
cx.xaxis.set_major_locator(loc)

#%%

#==============================================================================
# GLOBAL
#==============================================================================
folder='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/GLOBAL24H/All_time_steps/'
#folder='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/PRESENTDAY_DUST/All_time_steps/'
#plt.figure(figsize=(20,5))
dx=plt.subplot(1,4,2)


cube_global=iris.load(folder+'All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0]
cube=iris.load(folder+'All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0]

cut_lon=model_lons[cut_value]
cut_lon2=model_lons[cut_value2]


global_lats=cube.coord('latitude').points

global_lons=cube.coord('longitude').points
global_lons2=np.array(global_lons)
global_lons2[global_lons>180]=global_lons[global_lons>180]-360
global_lons=global_lons2
cut_value_glob=jl.find_nearest_vector_index(global_lons,cut_lon)

global_lons=cube.coord('longitude').points
global_lons2=np.array(global_lons)
global_lons2[global_lons>180]=global_lons[global_lons>180]-360
global_lons=global_lons2
cut_value_glob2=jl.find_nearest_vector_index(global_lons,cut_lon2)

#lons,lats=unrotated_grid(cube)

cube_regrided=cube.regrid(cube_wc, iris.analysis.Linear())
#plt.imshow(cube_regrided[15,:,:].data)
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
itime1=16
itime3=18


#
data1=(cube[16,:,:].data+cube[17,:,:].data)/2
data1[:,cut_value_glob:]=np.nan
data1[:,:200]=np.nan
CS=plt.contourf(X,Y,data1,levels_SW,cmap=cmap)
#
#

itime2=9
data2=cube[itime2,:,:].data
data2[:,300:cut_value_glob]=np.nan
CS=plt.contourf(X,Y,data2,levels_SW,cmap=cmap)
#
#
#
data3=cube[itime3,:,:].data
data3[:,cut_value_glob2:]=np.nan
data3[:,:cut_value_glob2-120]=np.nan

CS=plt.contourf(X,Y,data3,levels_SW,cmap=cmap)


plt.axvline(lonline1,lw=3,c='k',ls='--')
plt.axvline(lonline2,lw=3,c='k',ls='--')

currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))

plt.title('b) Global model')


#
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))

#CS=plt.contourf(X,Y,cube[itime2,:,:].data)
#        plt.clabel(CS, inline=1, fmt='%1.0f')
plt.ylim(ylim1,ylim2)
plt.xlim(xlim1,xlim2)

#cube.remove_coord('grid_latitude')
#cube.remove_coord('grid_longitude')
#pole_lat=cube.coord('grid_longitude').coord_system.grid_north_pole_latitude
#pole_lon=cube.coord('grid_longitude').coord_system.grid_north_pole_longitude

loc = plticker.MultipleLocator(base=20) # this locator puts ticks at regular intervals
dx.xaxis.set_major_locator(loc)

#%%

cube_regrided=cube.regrid(cube_wc, iris.analysis.Linear())
model_lons,model_lats=unrotated_grid(cube_regrided)
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
cx=plt.subplot(1,4,2)
#plt.title(name)
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.xlabel('Longitude')
itime2=15
itime1=17
itime3=18

cube=cube_regrided

#model_lons,model_lats=unrotated_grid(cube)



cut_value=jl.find_nearest_vector_index(model_lons,lon1)
cut_value2=jl.find_nearest_vector_index(model_lons,lon2)



data1=(cube[16,:,:].data+cube[17,:,:].data)/2
#data1=cube[itime1,:,:].data
data1[:,cut_value:]=np.nan
CS=plt.contourf(X,Y,data1,levels_SW,cmap=cmap)

#

data2=cube[itime2,:,:].data
data2[:,:cut_value]=np.nan
im=plt.contourf(X,Y,data2,levels_SW,cmap=cmap)
plt.axvline(lonline1,lw=3,c='k',ls='--')



data3=cube[itime3,:,:].data
data3[:,cut_value2:]=np.nan
im=plt.contourf(X,Y,data3,levels_SW,cmap=cmap)



#plt.axvline(lonline2,lw=3,c='k',ls='--')
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))

currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))
plt.title('b) Global model')
#plt.title('d) [INP]: VT17 (Mean)')


plt.ylim(ylim1,ylim2)
plt.xlim(xlim1,xlim2)


#CS=plt.contourf(X,Y,cube[itime2,:,:].data)
#        plt.clabel(CS, inline=1, fmt='%1.0f')
#divider = make_axes_locatable(cx)
#cax = divider.append_axes("right", size="5%", pad=0.05)

#cb=plt.colorbar(im, cax=cax)
#            cb=plt.colorbar()
#cb.set_label('SW flux $\mathrm{(W/m^2)}$')






#%%
plt.savefig(sav_fol+'Whole_cyclone_SW.png')
plt.savefig(sav_fol+'Whole_cyclone_SW.eps')

#%%

def func(x, y):
    return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2


global_lats=cube_global.coord('latitude').points

global_lons=cube_global.coord('longitude').points
global_lons2=np.array(global_lons)
global_lons2[global_lons>180]=global_lons[global_lons>180]-360
global_lons=global_lons2



grid_x, grid_y = np.meshgrid(global_lons,global_lats)


points = np.copy(coord)
values = np.copy(sat_LW)
valids=values<1000
points=points[valids,:]
values=values[valids]

#This can be done with griddata – below we try out all of the interpolation methods:


from scipy.interpolate import griddata
grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

#plt.figure()
#
#import matplotlib.pyplot as plt
#plt.subplot(221)
##>>> plt.imshow(, origin='lower')
#plt.plot(points[:,0], points[:,1], 'k.', ms=1)
#plt.title('Original')
#plt.subplot(222)
#plt.contourf(grid_x,grid_y,grid_z0, origin='lower')
#plt.plot(points[:,0], points[:,1], 'k.', ms=1)
#plt.colorbar()
#plt.title('Nearest')
#plt.subplot(223)
##>>> plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
#plt.contourf(grid_x,grid_y,grid_z1, origin='lower')
#plt.title('Linear')
#plt.subplot(224)
#plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
#plt.title('Cubic')
#plt.gcf().set_size_inches(6, 6)
#plt.show()
cube_sat=cube_global[0,:,:]
cube_sat.data=grid_z1
#print cube_sat
#sat_on_small_grid=
#sat_on_small_grid=cube_sat.regrid(cube_wc, iris.analysis.Linear())
#
#ax=plt.subplot(1,4,1)
#
#
#CS=plt.contourf(X,Y,sat_on_small_grid.data,levels_SW,cmap=cmap)
#
#
#plt.figure()
#cube_wc_reggrided=cube_wc.regrid(cube_global,iris.analysis.Linear())
#plt.contourf(grid_x,grid_y,cube_wc_reggrided[15,].data)
#


#%%
#
#model_lons,model_lats=unrotated_grid(cube_wc)
#print model_lats.max(),model_lats.min()
#X,Y=np.meshgrid(model_lons, model_lats)
##plt.pcolormesh(X,Y,cube_wc[15,:,:].data)

#for i in range(4):
#    
#plot(1,4,i+1)
#    plt.xlim(-60,20)
#    plt.ylim(-70,-50)
#
#lons, lats =iris.analysis.cartography.unrotate_pole(cube.coord('grid_longitude').points,cube.coord('grid_latitude').points,0,90-58)
#print lons.max(),lons.min()
#print lats.max(),lats.min()
#
#%%
'''
mb=netcdf.netcdf_file('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/SATELLITE/CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015030101-2015030223.nc','r')
plt.figure()

path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/'
mb=netcdf.netcdf_file(path+'CERES/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015011000-2015011123.nc','r')

times_ceres=mb.variables['time'].data*24*60*60
path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
from scipy.io import netcdf
cubes  =iris.load(path+'ceres/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc')
mb=netcdf.netcdf_file(path+'ceres/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc','r')
mb=netcdf.netcdf_file(path+'ceres_all_SO/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc','r')
times_ceres=mb.variables['time'].data*24*60*60


LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
lon=mb.variables['lon'].data
lat=mb.variables['lat'].data


latmin=-70
latmax=-30

lonmax=model_lons.max()
#lonmin=
lonmin=model_lons.min()


#primer pase a las 14.50
#segundo pase a las 16.30
ti=9#h
te=20#h

ti=11#h
te=15#h

tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()

tdi=(datetime.datetime(2015,01,10,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2015,01,10,te)-datetime.datetime(1970,1,1)).total_seconds()

t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.

tdi=(datetime.datetime(2014,12,9,ti)-datetime.datetime(1970,1,1)).total_seconds()
tde=(datetime.datetime(2014,12,9,te)-datetime.datetime(1970,1,1)).total_seconds()


cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]

sim_path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/'

cube_wc= iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0]
cube_wc = iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/All_time_steps/','m01s01i208'))[0]
#cube_wc=  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE/VT17_MEAN/All_time_steps/','m01s01i208'))[0]
model_lons,model_lats=stc.unrotated_grid(cube_wc)
#currentAxis = plt.gca()
#currentAxis.add_patch(Rectangle((model_lons_small.min(), model_lats_small.min()), model_lons_small.max()-model_lons_small.min(), model_lats_small.max()-model_lats_small.min(), fill=None, alpha=1))



times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
boolean=((lon>lonmin) & (lon<lonmax) & (lat<latmax) & (lat>latmin) & times_range)
print np.sum(boolean)
sat_lon=lon[boolean]
sat_lat=lat[boolean]

print datetime.datetime.fromtimestamp(times_ceres[boolean][0])
print datetime.datetime.fromtimestamp(times_ceres[boolean][-1])

t0=(datetime.datetime(2015,03,1,0)-datetime.datetime(1970,1,1)).total_seconds()
t0=(datetime.datetime(2015,01,10,0)-datetime.datetime(1970,1,1)).total_seconds()
t0=(datetime.datetime(2014,12,9,0)-datetime.datetime(1970,1,1)).total_seconds()
sat_LW=(times_ceres[boolean]-t0)/60./60.
sat_LW=LW[boolean]
#sat_LW=(times_ceres-datetime.datetime.fromtimestamp(0))/60//60.
coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)

grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
#grid_z1[grid_z1>1000]=np.nan
print model_lats.max(),model_lats.min()
X,Y=np.meshgrid(model_lons, model_lats)
#grid_z1[:,:cut_value]=np.nan
plt.axvline(model_lons[cut_value],lw=3,c='k',ls='--')
#plt.title(name)
plt.xlabel('Longitude')
CS=plt.contourf(X,Y,grid_z1,cmap=cmap)
plt.colorbar()

#%%
plt.plot((times_ceres[boolean]-t0)/60./60.,sat_lat,'bo')
plt.plot((times_ceres[boolean]-t0)/60./60.,sat_lon,'ro')
plt.axhline(model_lons.max(),c='r')
plt.axhline(model_lons.min(),c='r')
plt.axhline(model_lats.min(),c='b')
plt.axhline(model_lats.max(),c='b')

'''
#%%
'''

Frontal C1 Aqua pases:
2015-03-01 14:53:13.319687
2015-03-01 14:56:33.487300
Approximate to 15:00

Central C1 Aqua pases:
2015-03-01 16:34:11.548625
2015-03-01 16:35:26.847674
Calculate mean between 16:00 and 17:00


Back:
2015-03-01 18:13:07.798342
2015-03-01 18:14:33.807330
Can proably approximate to 18h


Central C2 Aqua pases: 16,72 to 16,78 en tiempos de 10
16.45
Calculate 0.25*16:00 and 0.75*17:00


Central C3 1325 UTC
calculate mean between 13 and 14
'''
