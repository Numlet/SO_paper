# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:00:57 2017

@author: eejvt
"""

from base_imports import *
from LW_satellite import LW_satellite_dict


LW_dict=OrderedDict()
LW_dict_filtered=OrderedDict()

Temp_min=-35+273.15
#Temp_min=0


LW_min=0.001

plt.figure(figsize=(20,20))
i=1
for key in run_path:
    if 'GLOBAL' in key:
#        if 'C2' in key:
#            continue
        sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'A_TRAIN_COLLOCATED/L1_CTT_Cloud_top_temperatureA-train_collocated.nc')[0])[:,:]
        cube_LW=iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s02i205_toa_outgoing_longwave_fluxA-train_collocated.nc')[0][:,:]
        cube_LW = cube_LW.regrid(sample_cube, iris.analysis.Linear())
    else:
        cube=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CTT_Cloud_top_temperatureA-train_collocated.nc')[0])[:,:]
        cube_LWP=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'A_TRAIN_COLLOCATED/','LWP'))[0])[:,:]
        cube_SW=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0])[:,:]
        cube_LW=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s02i205_toa_outgoing_longwave_fluxA-train_collocated.nc')[0][:,:])




    np.save(pspc_fol+'LW_distribution_'+key,cube_LW.data)

    LW_dict[key]=np.nanmean(cube_LW.data)
#    masked_cube[mask]=np.nan
    np.save(pspc_fol+'LW_distribution_filtered_'+key,cube_LW.data)
#    LWP_dict_filtered[key]=np.nanmean(masked_cube)


#    mask=cube.data<Temp_min
    plt.subplot(5,5,i)

#    masked_cube=cube.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
#    masked_cube=cube_LWP.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube[12,:,:].data)

    plt.title(key)
    plt.imshow(cube_LW.data[:,:])
    plt.colorbar()
#    print cube
    i=i+1
#LWP_dict['C2_GLOBAL']=LWP_dict['C1_GLOBAL']#fix to avoid breaking, correct!! also the global runs will give more problems as there is not enough low cloud
#%%

#
#import glob
#
#path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
#lon_offset=7
#
#
#
#sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
#from amsr2_daily_v7 import AMSR2daily
#amsr_data='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code/data.remss.com/amsr2/bmaps_v07.2/y2014/m12/'
#def read_data(filename=amsr_data+'f34_20141209v7.2.gz'):
#    dataset = AMSR2daily(filename, missing=missing)
#    if not dataset.variables: sys.exit('problem reading file')
#    return dataset
#cube =  stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/L1/','LWP'))[0])
#
#ilon = (169,174)
#ilat = (273,277)
#iasc = 0
#avar = 'vapor'
#missing = -999.
#
#dataset = read_data()
#
#times=dataset.variables['time'][0,]
#LWP=dataset.variables['cloud'][0,]
#LWP[LWP==missing]=np.nan
#LWP[times<12]=np.nan
#LWP[times>15]=np.nan
#lon=dataset.variables['longitude']
#lat=dataset.variables['latitude']
#Xsat,Ysat=np.meshgrid(lon,lat)
#Xsat[np.isnan(LWP)]=np.nan
#Ysat[np.isnan(LWP)]=np.nan
#
#Xsat_flat=Xsat.flatten()
#Ysat_flat=Ysat.flatten()
#LWP_flat=LWP.flatten()
#Xsat_flat=Xsat_flat[np.logical_not(np.isnan(Xsat_flat))]
#Ysat_flat=Ysat_flat[np.logical_not(np.isnan(Ysat_flat))]
#LWP_flat=LWP_flat[np.logical_not(np.isnan(LWP_flat))]
#
#
#
#
#
#model_lons,model_lats=stc.unrotated_grid(cube)
#
#coord=np.zeros([len(Xsat_flat),2])
#coord[:,0]=Xsat_flat
#coord[:,1]=Ysat_flat
#cm=plt.cm.RdBu_r
##model_lons=np.linspace(-5,20,500)
#X,Y=np.meshgrid(model_lons, model_lats)
#grid_z1 = sc.interpolate.griddata(coord, LWP_flat, (X,Y), method='linear')
#
#LWP_dict['C3_SATELLITE']=np.nanmean(grid_z1)
#LWP_dict_filtered['C3_SATELLITE']=np.nanmean(grid_z1)
#
##%%
#
#path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
#
#sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
#from amsr2_daily_v7 import AMSR2daily
#amsr_data='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/AMSR2/data.remss.com/amsr2/bmaps_v07.2/y2015/m03/'
#glob.glob(amsr_data+'*')
#def read_data(filename=amsr_data+'f34_20150301v7.2.gz'):
#    dataset = AMSR2daily(filename, missing=missing)
#    if not dataset.variables: sys.exit('problem reading file')
#    return dataset
#
#ilon = (169,174)
#ilat = (273,277)
#iasc = 0
#avar = 'vapor'
#missing = -999.
#
#dataset = read_data('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/AMSR2/f34_20150308v7.2.gz')
#dataset = read_data('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/AMSR2/f34_20150301v7.2.gz')
#
#sim_path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/'
#sub_folder='L1/'
#code='LWP'
#cube_DM10 = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0])
#
#times=dataset.variables['time'][0,]
#LWP=dataset.variables['cloud'][0,]
#LWP[LWP==missing]=np.nan
#
#lon=dataset.variables['longitude']
#lon[lon>180]=lon[lon>180]-360
#lat=dataset.variables['latitude']
#
#Xsat,Ysat=np.meshgrid(lon,lat)
#Xsat[np.isnan(LWP)]=np.nan
#Ysat[np.isnan(LWP)]=np.nan
#
#Xsat_flat=Xsat.flatten()
#Ysat_flat=Ysat.flatten()
#LWP_flat=LWP.flatten()
#Xsat_flat=Xsat_flat[np.logical_not(np.isnan(Xsat_flat))]
#Ysat_flat=Ysat_flat[np.logical_not(np.isnan(Ysat_flat))]
#LWP_flat=LWP_flat[np.logical_not(np.isnan(LWP_flat))]
#
#def check_nan(array):
#    return np.isnan(array).any()
#
#model_lons,model_lats=stc.unrotated_grid(cube_DM10)
#max_lon,min_lon=model_lons.max(),model_lons.min()
#max_lat,min_lat=model_lats.max(),model_lats.min()
#
#coord=np.zeros([len(Xsat_flat),2])
#coord[:,0]=Xsat_flat
#coord[:,1]=Ysat_flat
#cm=plt.cm.RdBu_r
#X,Y=np.meshgrid(model_lons, model_lats)
#grid_z1 = sc.interpolate.griddata(coord, LWP_flat, (X,Y), method='linear')
#
#
#LWP_dict['C1_SATELLITE']=np.nanmean(grid_z1)
#LWP_dict_filtered['C1_SATELLITE']=np.nanmean(grid_z1)
##%%
#
#path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
#
#
#sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
#from amsr2_daily_v7 import AMSR2daily
#amsr_data='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code/data.remss.com/amsr2/bmaps_v07.2/y2014/m12/'
#amsr_data='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/AMSR2/'
#glob.glob(amsr_data+'*')

#def read_data(filename=amsr_data+'f34_20150110v7.2.gz'):
#    dataset = AMSR2daily(filename, missing=missing)
#    if not dataset.variables: sys.exit('problem reading file')
#    return dataset
#
#ilon = (169,174)
#ilat = (273,277)
#iasc = 0
#avar = 'vapor'
#missing = -999.
#
#dataset = read_data()
#
#
#sim_path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/'
#sub_folder='L1/'
#code='LWP'
#
#cube_DM10 = iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0]
#
#times=dataset.variables['time'][0,]
#LWP=dataset.variables['cloud'][0,]
#LWP[times<14]=np.nan
#LWP[times>18]=np.nan
#LWP[LWP==missing]=np.nan
#
#lon=dataset.variables['longitude']
#lon[lon>180]=lon[lon>180]-360
#lat=dataset.variables['latitude']
#Xsat,Ysat=np.meshgrid(lon,lat)
#Xsat[np.isnan(LWP)]=np.nan
#Ysat[np.isnan(LWP)]=np.nan
#Xsat_flat=Xsat.flatten()
#Ysat_flat=Ysat.flatten()
#LWP_flat=LWP.flatten()
#Xsat_flat=Xsat_flat[np.logical_not(np.isnan(Xsat_flat))]
#Ysat_flat=Ysat_flat[np.logical_not(np.isnan(Ysat_flat))]
#LWP_flat=LWP_flat[np.logical_not(np.isnan(LWP_flat))]
#def check_nan(array):
#    return np.isnan(array).any()
#model_lons,model_lats=stc.unrotated_grid(cube_DM10)
#max_lon,min_lon=model_lons.max(),model_lons.min()
#max_lat,min_lat=model_lats.max(),model_lats.min()
#coord=np.zeros([len(Xsat_flat),2])
#coord[:,0]=Xsat_flat
#coord[:,1]=Ysat_flat
#cm=plt.cm.RdBu_r
#X,Y=np.meshgrid(model_lons, model_lats)
#grid_z1 = sc.interpolate.griddata(coord, LWP_flat, (X,Y), method='linear')
#plt.figure()
#plt.imshow(grid_z1)
#
#LWP_dict['C2_SATELLITE']=np.nanmean(grid_z1)
#LWP_dict_filtered['C2_SATELLITE']=np.nanmean(grid_z1)
#
#

#%%



#np.save(pspc_fol+'LWP_dict',LWP_dict)
#np.save(pspc_fol+'LWP_dict_filtered',LWP_dict_filtered)
list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['y','r','green','peru','k','grey','silver']
list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

#LW_dict['C3_VT17_MEAN']
for cloud in list_clouds:
    LW_dict[cloud+'_SATELLITE']=np.nanmean(LW_satellite_dict[cloud+'_SATELLITE'])
    LW_dict_filtered[cloud+'_SATELLITE']=np.nanmean(LW_satellite_dict[cloud+'_SATELLITE'])

#LW_dict['C3_SATELLITE']=0
#LW_dict['C1_SATELLITE']=0
#LW_dict['C2_SATELLITE']=0
N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
fig, ax = plt.subplots()
width = 0.1       # the width of the bars
iparam=0
for param in list_params:
    means = tuple([LW_dict[cloud+'_'+param] for cloud in list_clouds])
    std = tuple([LW_dict[cloud+'_'+param]*0.0 for cloud in list_clouds])


    rects1 = ax.bar(ind+iparam*width, means, width, color=list_colors[iparam], yerr=std,label=param)
    iparam=iparam+1
plt.legend()
ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
ax.set_xticklabels(tuple(list_clouds))
ax.set_title('Outgoing Longwave radiation')
ax.set_ylabel('LW $\mathrm{(W/m^2)}$')
#plt.ylim(0,0.25)
plt.xlim(0,5)
plt.ylim(0,280)


plt.savefig(sav_fol+'LW_barplot.png')
plt.savefig(sav_fol+'LW_barplot.eps')

#%%

plt.figure()
data=np.load(pspc_fol+'LW_distribution_filtered_C3_VT17_MEAN.npy')
plt.title(np.nanmean(data))
plt.imshow(data)
plt.colorbar()
