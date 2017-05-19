#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:00:57 2017

@author: eejvt
"""

from base_imports import *



Temp_min=-35+273.15
Temp_min=0
SW_dict=OrderedDict()


plt.figure(figsize=(20,20))
i=1
itime=12
for key in run_path:
    itime=cloud_it[key[:2]]
    print key
    if 'GLOBAL' in key:
#        if 'C3' in key:
#            continue
        sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
        cube_SW=iris.load(ukl.Obtain_name(run_path[key]+'L1/','LWP'))[0][itime,:,:]
        cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
#        cube = cube.regrid(sample_cube, iris.analysis.Linear())
        cube_SW = cube_SW.regrid(sample_cube, iris.analysis.Linear())
    else:
        cube=stc.clean_cube(iris.load(run_path[key]+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
        cube_SW=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'L1/','LWP'))[0])[itime,:,:]
    mask=cube.data<Temp_min
    plt.subplot(5,5,i)

    masked_cube=cube.data
    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
    masked_cube=cube_SW.data
    masked_cube[mask]=np.nan
#    plt.imshow(cube[12,:,:].data)
    plt.title(key)
    plt.imshow(masked_cube[:,:])
    SW_dict[key]=np.nanmean(masked_cube)
    plt.colorbar()
    print cube
    i=i+1
#SW_dict['C3_GLOBAL']=SW_dict['C2_GLOBAL']#fix to avoid breaking, correct!! also the global runs will give more problems as there is not enough low cloud
#%%




import glob

path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
lon_offset=7



sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
from amsr2_daily_v7 import AMSR2daily
amsr_data='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code/data.remss.com/amsr2/bmaps_v07.2/y2014/m12/'
def read_data(filename=amsr_data+'f34_20141209v7.2.gz'):
    dataset = AMSR2daily(filename, missing=missing)
    if not dataset.variables: sys.exit('problem reading file')
    return dataset
cube =  stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/L1/','LWP'))[0])

ilon = (169,174)
ilat = (273,277)
iasc = 0
avar = 'vapor'
missing = -999.

dataset = read_data()

times=dataset.variables['time'][0,]
LWP=dataset.variables['cloud'][0,]
LWP[LWP==missing]=np.nan
LWP[times<12]=np.nan
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

SW_dict['C1_SAT']=np.nanmean(grid_z1)

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
cube_DM10 = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0])

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


SW_dict['C2_SAT']=np.nanmean(grid_z1)
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
LWP[times<14]=np.nan
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

SW_dict['C3_SAT']=np.nanmean(grid_z1)




#%%
list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_MIN']
list_colors=['y','r','green','brown','k','grey','silver']
list_params=['SAT','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_MIN']
list_colors=['b','y','r','green','brown','k','grey','silver']
list_clouds=['C1','C2','C3']
#SW_dict['C1_SAT']=0
#SW_dict['C2_SAT']=0
#SW_dict['C3_SAT']=0
N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
fig, ax = plt.subplots()
width = 0.1       # the width of the bars
iparam=0
for param in list_params:
    means = tuple([SW_dict[cloud+'_'+param] for cloud in list_clouds])
    std = tuple([SW_dict[cloud+'_'+param]*0.0 for cloud in list_clouds])


    rects1 = ax.bar(ind+iparam*width, means, width, color=list_colors[iparam], yerr=std,label=param)
    iparam=iparam+1
plt.legend()
ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
ax.set_xticklabels(tuple(list_clouds))
ax.set_title('LWP')
ax.set_ylabel('LWP mm')
plt.ylim(0,0.25)
plt.xlim(0,4)


plt.savefig(sav_fol+'LWP_barplot.png')

#%%
#women_means = (25, 32, 34, 20, 25)
#women_std = (3, 5, 2, 3, 3)
#rects2 = ax.bar(ind + width, women_means, width, color='y', yerr=women_std)
#ax.set_title('Scores by group and gender')
#
#ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

