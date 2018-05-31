# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:00:57 2017

@author: eejvt
"""

from base_imports import *
from CTT_satellite import CTT_satellite_dict


CTT_dict=OrderedDict()
CTT_dict_filtered=OrderedDict()

Temp_min=-35+273.15
#Temp_min=0


CTT_min=0.001

plt.figure(figsize=(20,20))

i=1

for key in run_path:
    if 'C3' in key:
        continue
    if 'GLOBAL' in key:
  
        sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'A_TRAIN_COLLOCATED/L1_CTT_LIQUID_Cloud_liquid_top_temperatureA-train_collocated.nc')[0])[:,:]
        cube_CTT=iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CTT_LIQUID_Cloud_liquid_top_temperatureA-train_collocated.nc')[0][:,:]
        cube_CTT = cube_CTT.regrid(sample_cube, iris.analysis.Linear())
    else:
        cube=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CTT_LIQUID_Cloud_liquid_top_temperatureA-train_collocated.nc')[0])[:,:]
        cube_LWP=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'A_TRAIN_COLLOCATED/','LWP'))[0])[:,:]
        cube_SW=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0])[:,:]
        cube_CTT=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CTT_LIQUID_Cloud_liquid_top_temperatureA-train_collocated.nc')[0][:,:])




    try:
        np.save(pspc_fol+'CTT_liquid_distribution_'+key,cube_CTT.data)
    except:
        np.save(pspc_fol+'CTT_liquid_distribution_'+key,cube_CTT.data.data)

    CTT_dict[key]=np.nanmean(cube_CTT.data)
#    masked_cube[mask]=np.nan
    try:
        np.save(pspc_fol+'CTT_liquid_distribution_filtered_'+key,cube_CTT.data)
    except:
        np.save(pspc_fol+'CTT_liquid_distribution_filtered_'+key,cube_CTT.data.data)
        
#    LWP_dict_filtered[key]=np.nanmean(masked_cube)


#    mask=cube.data<Temp_min
    plt.subplot(5,5,i)

#    masked_cube=cube.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
#    masked_cube=cube_CTTP.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube[12,:,:].data)

    plt.title(key)
    plt.imshow(cube_CTT.data[:,:])
    plt.colorbar()
#    print cube
    i=i+1
#LWP_dict['C2_GLOBAL']=LWP_dict['C1_GLOBAL']#fix to avoid breaking, correct!! also the global runs will give more problems as there is not enough low cloud
#%%

list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['y','r','green','brown','k','grey','silver']
list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','brown','k','grey','silver']
list_clouds=['C1','C2','C3']
list_clouds=['C1','C2']

#CTT_dict['C3_VT17_MEAN']
for cloud in list_clouds:
    CTT_dict[cloud+'_SATELLITE']=np.nanmean(CTT_satellite_dict[cloud+'_SATELLITE'])
    CTT_dict_filtered[cloud+'_SATELLITE']=np.nanmean(CTT_satellite_dict[cloud+'_SATELLITE'])

#CTT_dict['C3_SATELLITE']=0
#CTT_dict['C1_SATELLITE']=0
#CTT_dict['C2_SATELLITE']=0
N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
fig, ax = plt.subplots()
width = 0.1       # the width of the bars
iparam=0
for param in list_params:
    means = tuple([CTT_dict[cloud+'_'+param] for cloud in list_clouds])
    std = tuple([CTT_dict[cloud+'_'+param]*0.0 for cloud in list_clouds])


    rects1 = ax.bar(ind+iparam*width, means, width, color=list_colors[iparam], yerr=std,label=param)
    iparam=iparam+1
plt.legend()
ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
ax.set_xticklabels(tuple(list_clouds))
ax.set_title('Mean cloud top')
ax.set_ylabel('CTT')
#plt.ylim(0,0.25)
plt.xlim(0,5)
plt.ylim(0,280)


plt.savefig(sav_fol+'CTT_liquid_barplot.png')

#%%

plt.figure()
data=np.load(pspc_fol+'CTT_distribution_filtered_C3_VT17_MEAN.npy')
plt.title(np.nanmean(data))
plt.imshow(data)
plt.colorbar()
