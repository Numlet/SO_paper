#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:06:17 2017

@author: eejvt
"""

from base_imports import *
CDNC_satellite_dict=OrderedDict()



#==============================================================================
# CLOUD 3 SO_KALLI
#==============================================================================
Nd=iris.load('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/modis/dan/Nd2_MYD06_L2.A2014343.1325.006.2014344210847.hdf.nc')[0]
path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
hdf  =SD.SD(path+'modis/'+'MYD03.A2014343.1325.006.2014344162340.hdf')
#for k in hdf.datasets().keys():
#    if '' in k:
#        print k

SDS_NAME  = 'Latitude'
sds = hdf.select(SDS_NAME)
lat = sds.get()
SDS_NAME  = 'Longitude'
sds = hdf.select(SDS_NAME)
lon = sds.get()



sat_lon=lon.flatten()
sat_lat=lat.flatten()
sat_data=Nd.data.flatten()

cube_cdnc= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/DM10_REPEAT/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0],200)
cube_cdnc=cube_cdnc*1e-6

coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
model_lons,model_lats=unrotated_grid(cube_cdnc)
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)

grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
#plt.figure()
#plt.title(np.nanmean(grid_z1))
#plt.imshow(grid_z1)
#plt.colorbar()

print 'CLOUD 3', np.nanmean(grid_z1), 'std:', np.nanstd(grid_z1), '95%:', 2*np.nanstd(grid_z1) 
print 'model:', np.mean(cube_cdnc.data), 'std:',np.std(cube_cdnc.data),2*np.std(cube_cdnc.data)
CDNC_satellite_dict['C3_SATELLITE']=grid_z1

#%%
np.nanmean(grid_z1)
plt.figure()
plt.contourf(X,Y, grid_z1)
plt.colorbar()
#%%


#==============================================================================
# CLOUD 1 ANTIGUA 2
#==============================================================================


Nd=iris.load('/nfs/a201/eejvt/CASIM/ND_SATELLITE/Nd2_MYD06_L2.A2015060.1630.006.2015062234245.hdf.nc')[0]



hdf  =SD.SD('/nfs/a201/eejvt/CASIM/ND_SATELLITE/MYD03.A2015060.1630.006.2015061161318.hdf')
#for k in hdf.datasets().keys():
#    if 'atit' in k:
#        print k
#plt.figure()
#plt.imshow(Nd.data)
#plt.colorbar()
SDS_NAME  = 'Latitude'
sds = hdf.select(SDS_NAME)
lat = sds.get()
SDS_NAME  = 'Longitude'
sds = hdf.select(SDS_NAME)
lon = sds.get()



sat_lon=lon.flatten()
sat_lat=lat.flatten()
sat_data=Nd.data.flatten()

cube_cdnc= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/GLO_MEAN/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])
cube_cdnc=cube_cdnc*1e-6

coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
model_lons,model_lats=unrotated_grid(cube_cdnc)
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)

#grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
#plt.figure()
#plt.title(np.nanmean(grid_z1))
#plt.imshow(grid_z1)
#plt.colorbar()
print 'CLOUD 1', np.nanmean(grid_z1), 'std:', np.nanstd(grid_z1), '95%:', 2*np.nanstd(grid_z1) 
print 'model:', np.mean(cube_cdnc.data), 'std:',np.std(cube_cdnc.data),2*np.std(cube_cdnc.data)
CDNC_satellite_dict['C1_SATELLITE']=grid_z1
#%%

#==============================================================================
# CLOUD 2 ANTIGUA 3
#==============================================================================


Nd=iris.load('/nfs/a201/eejvt/CASIM/ND_SATELLITE/Nd2_MYD06_L2.A2015010.1645.006.2015012151745.hdf.nc')[0]



hdf  =SD.SD('/nfs/a201/eejvt/CASIM/ND_SATELLITE/MYD03.A2015010.1645.006.2015012123319.hdf')
#for k in hdf.datasets().keys():
#    if 'atit' in k:
#        print k
#plt.figure()
#plt.imshow(Nd.data)
#plt.colorbar()
SDS_NAME  = 'Latitude'
sds = hdf.select(SDS_NAME)
lat = sds.get()
SDS_NAME  = 'Longitude'
sds = hdf.select(SDS_NAME)
lon = sds.get()



sat_lon=lon.flatten()
sat_lat=lat.flatten()
sat_data=Nd.data.flatten()

cube_cdnc= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/MEYERS/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])
cube_cdnc= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/GLO_MEAN/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])
cube_cdnc=cube_cdnc*1e-6
cube_cdnc.data[cube_cdnc.data==0]=np.nan
coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
model_lons,model_lats=unrotated_grid(cube_cdnc)
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)

grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
#plt.figure()
#plt.title(np.nanmean(grid_z1))
#plt.imshow(grid_z1)
#plt.colorbar()
print 'CLOUD 2', np.nanmean(grid_z1), 'std:', np.nanstd(grid_z1), '95%:', 2*np.nanstd(grid_z1) 
print 'model:', np.nanmean(cube_cdnc.data), 'std:',np.nanstd(cube_cdnc.data),2*np.nanstd(cube_cdnc.data)
CDNC_satellite_dict['C2_SATELLITE']=grid_z1
#%%
cube_cdnc= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/GLO_MEAN/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])
cube_cdnc=cube_cdnc*1e-6
cube_cdnc.data[cube_cdnc.data==0]=np.nan

cdnc_data=cube_cdnc.data.flatten()
cdnc_data=cdnc_data[~np.isnan(cdnc_data)]
plt.hist(cdnc_data,color='grey',normed=1)
cube_cdnc= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/MEYERS/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])
cube_cdnc=cube_cdnc*1e-6
cube_cdnc.data[cube_cdnc.data==0]=np.nan

cdnc_data=cube_cdnc.data.flatten()
cdnc_data=cdnc_data[~np.isnan(cdnc_data)]
plt.hist(cdnc_data,color='r',normed=1)

cube_cdnc= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/DM10/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])
cube_cdnc=cube_cdnc*1e-6
cube_cdnc.data[cube_cdnc.data==0]=np.nan

cdnc_data=cube_cdnc.data.flatten()
cdnc_data=cdnc_data[~np.isnan(cdnc_data)]
plt.hist(cdnc_data,color='green',normed=1)


cdnc_data=grid_z1[~np.isnan(grid_z1)]
plt.hist(cdnc_data,color='b',normed=1)







