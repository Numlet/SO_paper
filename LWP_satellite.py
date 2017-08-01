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
plt.figure()
plt.imshow(grid_z1)
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

path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'


sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
from amsr2_daily_v7 import AMSR2daily
amsr_data='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code/data.remss.com/amsr2/bmaps_v07.2/y2014/m12/'
amsr_data='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/AMSR2/'
glob.glob(amsr_data+'*')
def read_data(filename=amsr_data+'f34_20150110v7.2.gz'):
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

cube_DM10 = iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0]

times=dataset.variables['time'][0,]
LWP=dataset.variables['cloud'][0,]
LWP[times<15]=np.nan
LWP[times>18]=np.nan
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
plt.figure()
plt.imshow(grid_z1)

LWP_satellite_dict['C2_SATELLITE']=grid_z1

