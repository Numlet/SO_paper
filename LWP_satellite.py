#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 10:35:16 2017

@author: eejvt
"""
from base_imports import *



path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
lon_offset=7

LWP_satellite_dict=OrderedDict()


sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
from amsr2_daily_v7 import AMSR2daily
amsr_data='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code/data.remss.com/amsr2/bmaps_v07.2/y2014/m12/'
def read_data(filename=amsr_data+'f34_20141209v7.2.gz'):
    dataset = AMSR2daily(filename, missing=missing)
    if not dataset.variables: sys.exit('problem reading file')
    return dataset
cube =  iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/L1/','LWP'))[0]

ilon = (169,174)
ilat = (273,277)
iasc = 0
avar = 'vapor'
missing = -999.

dataset = read_data()

times=dataset.variables['time'][0,]
LWP=dataset.variables['cloud'][0,]
LWP[LWP==missing]=np.nan
LWP[times<13]=np.nan
LWP[times>15]=np.nan
lon=dataset.variables['longitude']
lat=dataset.variables['latitude']
Xsat,Ysat=np.meshgrid(lon,lat)
Xsat[np.isnan(LWP)]=np.nan
Ysat[np.isnan(LWP)]=np.nan

Xsat_flat=Xsat.flatten()
Ysat_flat=Ysat.flatten()
LWP_flat=LWP.flatten()
Xsat_flat=Xsat_flat[np.logical_not(np.isnan(Xsat_flat))]
Ysat_flat=Ysat_flat[np.logical_not(np.isnan(Ysat_flat))]
LWP_flat=LWP_flat[np.logical_not(np.isnan(LWP_flat))]





model_lons,model_lats=stc.unrotated_grid(cube)

coord=np.zeros([len(Xsat_flat),2])
coord[:,0]=Xsat_flat
coord[:,1]=Ysat_flat
cm=plt.cm.RdBu_r
#model_lons=np.linspace(-5,20,500)
X,Y=np.meshgrid(model_lons, model_lats)
grid_z1 = sc.interpolate.griddata(coord, LWP_flat, (X,Y), method='linear')

LWP_satellite_dict['C3_SATELLITE']=grid_z1
grid_z1[grid_z1<0]=np.nan
plt.figure()
plt.title(np.nanmean(stc.clean_cube(grid_z1)))
plt.imshow(stc.clean_cube(grid_z1))
plt.colorbar()
#%%

path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'

sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
from amsr2_daily_v7 import AMSR2daily
amsr_data='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/AMSR2/data.remss.com/amsr2/bmaps_v07.2/y2015/m03/'
glob.glob(amsr_data+'*')
def read_data(filename=amsr_data+'f34_20150301v7.2.gz'):
    dataset = AMSR2daily(filename, missing=missing)
    if not dataset.variables: sys.exit('problem reading file')
    return dataset

ilon = (169,174)
ilat = (273,277)
iasc = 0
avar = 'vapor'
missing = -999.



dataset = read_data('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/AMSR2/f34_20150308v7.2.gz')
dataset = read_data('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/AMSR2/f34_20150301v7.2.gz')

sim_path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/'
sub_folder='L1/'
code='LWP'
cube_DM10 = iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0]

times=dataset.variables['time'][0,]
LWP=dataset.variables['cloud'][0,]
LWP[LWP==missing]=np.nan

lon=dataset.variables['longitude']
lon[lon>180]=lon[lon>180]-360
lat=dataset.variables['latitude']

Xsat,Ysat=np.meshgrid(lon,lat)
Xsat[np.isnan(LWP)]=np.nan
Ysat[np.isnan(LWP)]=np.nan

Xsat_flat=Xsat.flatten()
Ysat_flat=Ysat.flatten()
LWP_flat=LWP.flatten()
Xsat_flat=Xsat_flat[np.logical_not(np.isnan(Xsat_flat))]
Ysat_flat=Ysat_flat[np.logical_not(np.isnan(Ysat_flat))]
LWP_flat=LWP_flat[np.logical_not(np.isnan(LWP_flat))]

def check_nan(array):
    return np.isnan(array).any()

model_lons,model_lats=stc.unrotated_grid(cube_DM10)
max_lon,min_lon=model_lons.max(),model_lons.min()
max_lat,min_lat=model_lats.max(),model_lats.min()

coord=np.zeros([len(Xsat_flat),2])
coord[:,0]=Xsat_flat
coord[:,1]=Ysat_flat
cm=plt.cm.RdBu_r
X,Y=np.meshgrid(model_lons, model_lats)
grid_z1 = sc.interpolate.griddata(coord, LWP_flat, (X,Y), method='linear')


LWP_satellite_dict['C1_SATELLITE']=grid_z1
#%%


from pyhdf import SD
path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/'
SDS_NAME  = 'Cloud_Top_Height_Nadir_Night'
SDS_NAME  = 'cloud_top_height_1km'
#hdf = SD.SD(FILE_NAME)
SDS_NAME  = 'Cloud_Top_Height'
SDS_NAME  = 'Cloud_Top_Temperature'
SDS_NAME  = 'Cloud_Water_Path_37'
SDS_NAME  = 'Cloud_Water_Path'
hdf  =SD.SD(path+'MODIS/'+'MYD06_L2.A2015010.1645.006.2015012151745.hdf')
#print hdf.datasets().keys()
for k in hdf.datasets().keys():
    if 'Water' in k:
        print k
        sds = hdf.select(k)
        data = sds.get()
        print data.shape

sds = hdf.select(SDS_NAME)
data = sds.get( )
mask_value=-9999
data[data==mask_value]=np.float64('Nan')
data=jl.congrid(data,hdf.select('Latitude')[:,:].shape)
#data=(data+15000)*0.009999999776482582
#mask_value=-32767
print data.shape
lat = hdf.select('Latitude')
latitude = lat[:,:]
lon = hdf.select('Longitude')
longitude = lon[:,:]




cloud_top= iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/DM10/All_time_steps','m01s09i223'))[0]

sat_lon=longitude.flatten()
sat_lat=latitude.flatten()
sat_data=data.flatten()

hdf  =SD.SD(path+'MODIS/'+'MYD06_L2.A2015010.1640.006.2015012160803.hdf')
sds = hdf.select(SDS_NAME)
data = sds.get( )
import pprint
mask_value=-9999
data[data==mask_value]=np.float64('Nan')
data=jl.congrid(data,hdf.select('Latitude')[:,:].shape)
#data=(data+15000)*0.009999999776482582
#mask_value=-32767
print data.shape
lat = hdf.select('Latitude')
latitude = lat[:,:]
lon = hdf.select('Longitude')
longitude = lon[:,:]


sat_lon=np.concatenate((sat_lon,longitude.flatten()))
sat_lat=np.concatenate((sat_lat,latitude.flatten()))
sat_data=np.concatenate((sat_data,data.flatten()))

coord=np.zeros([len(sat_lon),2])
coord[:,0]=sat_lon
coord[:,1]=sat_lat
cm=plt.cm.RdBu_r
model_lons,model_lats=unrotated_grid(cloud_top)
X,Y=np.meshgrid(model_lons, model_lats)
grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
grid_z1[np.isnan(grid_z1)]=0


#plt.figure()
#plt.figure(figsize=(15,13))
#levels=np.linspace(0.,1).tolist()
#plt.subplot(221)
#plt.contourf(X,Y,grid_z1*1e-3,levels, origin='lower',cmap=cm)
#plt.title('Satellite (MODIS)')
#cb=plt.colorbar()
#cb.set_label('LWP')
#
LWP_satellite_dict['C2_SATELLITE']=grid_z1*1e-3


#%%

#
path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'


sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
from amsr2_daily_v7 import AMSR2daily
#amsr_data='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code/data.remss.com/amsr2/bmaps_v07.2/y2014/m12/'
amsr_data='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/AMSR2/'
glob.glob(amsr_data+'*')
def read_data(filename=amsr_data+'f34_20150110v8.gz'):
    dataset = AMSR2daily(filename, missing=missing)
    if not dataset.variables: sys.exit('problem reading file')
    return dataset

ilon = (169,174)
ilat = (273,277)
iasc = 0
avar = 'vapor'
missing = -999.

dataset = read_data()


sim_path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/'
sub_folder='L1/'
code='LWP'

cube_DM10 = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0],100)





times=dataset.variables['time'][1,]

times[times==-999.]=np.nan
times[times<14]=np.nan
times[times>19]=np.nan
plt.figure()
plt.imshow(times)
plt.colorbar()
plt.show()
LWP=dataset.variables['cloud'][0,]
#LWP[times<14]=np.nan
#LWP[times>19]=np.nan
LWP[LWP==missing]=np.nan

lon=dataset.variables['longitude']
lon[lon>180]=lon[lon>180]-360
lat=dataset.variables['latitude']
Xsat,Ysat=np.meshgrid(lon,lat)
Xsat[np.isnan(LWP)]=np.nan
Ysat[np.isnan(LWP)]=np.nan
Xsat_flat=Xsat.flatten()
Ysat_flat=Ysat.flatten()
LWP_flat=LWP.flatten()
Xsat_flat=Xsat_flat[np.logical_not(np.isnan(Xsat_flat))]
Ysat_flat=Ysat_flat[np.logical_not(np.isnan(Ysat_flat))]
LWP_flat=LWP_flat[np.logical_not(np.isnan(LWP_flat))]
def check_nan(array):
    return np.isnan(array).any()
model_lons,model_lats=stc.unrotated_grid(cube_DM10)
max_lon,min_lon=model_lons.max(),model_lons.min()
max_lat,min_lat=model_lats.max(),model_lats.min()
coord=np.zeros([len(Xsat_flat),2])
coord[:,0]=Xsat_flat
coord[:,1]=Ysat_flat
cm=plt.cm.RdBu_r
X,Y=np.meshgrid(model_lons, model_lats)
grid_z1 = sc.interpolate.griddata(coord, LWP_flat, (X,Y), method='linear')



grid_z1[grid_z1==0]=np.nan
grid_z1[grid_z1<0]=np.nan
plt.figure()
#plt.contourf(X,Y,grid_z1,cmap=plt.cm.RdBu)
plt.imshow(grid_z1,cmap=plt.cm.RdBu)
plt.colorbar()

#%%
lwp=dataset.variables['cloud'][0,]
values=[]
for ilat in range(len(lat)):
    for ilon in range(len(lon)):
        if ((lon[ilon]>-31) and (lon[ilon]<-21) and (lat[ilat]>-62) and (lat[ilat]<-56)):
            print ilat, ilon
            values.append(lwp[ilat,ilon])
print np.nanmean(values)

X,Y=np.meshgrid(lon, lat)
#plt.contourf(X,Y,lwp,np.linspace(0,0.6,15).tolist(), interpolation='none')
plt.imshow(lwp, interpolation='none')
plt.colorbar()
plt.ylim(-62,-56)
plt.xlim(-31,-21)
#LWP_satellite_dict['C2_SATELLITE']=grid_z1

#np.nanmean(grid_z1)


#plt.close()
