# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:00:57 2017

@author: eejvt
"""

from base_imports import *
#from CDNC_satellite import CDNC_satellite_dict


CDNC_dict=OrderedDict()
CDNC_dict_std=OrderedDict()
CDNC_dict_filtered=OrderedDict()

Temp_min=-35+273.15
#Temp_min=0


CDNC_min=0.001

plt.figure(figsize=(20,20))
i=1

for key in run_path:
#    if 'DM15' in key:
#        continue
    if 'GLOBAL' in key:
#        if 'C2' in key:
        continue
        sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'A_TRAIN_COLLOCATED/L1_CDNC_max_cloud_water_Cloud_droplet_concentratio_at_maximum_cloud_water_contentA-train_collocated.nc')[0])[:,:]
        cube_CDNC=iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CDNC_max_cloud_water_Cloud_droplet_concentratio_at_maximum_cloud_water_contentA-train_collocated.nc')[0][:,:]
        cube_CDNC_all=iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CDNC_Cloud droplet number concentrationA-train_collocated.nc')[0][:,:]
        cube_CDNC = cube_CDNC.regrid(sample_cube, iris.analysis.Linear())
    else:
#        cube=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CDNC_Cloud_top_temperatureA-train_collocated.nc')[0])[:,:]
        cube_LWP=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'A_TRAIN_COLLOCATED/','LWP'))[0])[:,:]
        cube_SW=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0])[:,:]
        cube_CDNC=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CDNC_max_cloud_water_Cloud_droplet_concentratio_at_maximum_cloud_water_contentA-train_collocated.nc')[0][:,:])
        cube_CDNC_all=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CDNC_max_cloud_water_Cloud_droplet_concentratio_at_maximum_cloud_water_contentA-train_collocated.nc')[0][:,:])




    try:
        np.save(pspc_fol+'CDNC_distribution_'+key,cube_CDNC.data)
    except:
        np.save(pspc_fol+'CDNC_distribution_'+key,cube_CDNC.data.data)

    CDNC_dict[key]=np.nanmean(cube_CDNC.data)
    CDNC_dict_std[key]=np.nanstd(cube_CDNC.data)
#    masked_cube[mask]=np.nan
    try:
        np.save(pspc_fol+'CDNC_distribution_filtered_'+key,cube_CDNC.data)
    except:
        np.save(pspc_fol+'CDNC_distribution_filtered_'+key,cube_CDNC.data.data)
        
#    LWP_dict_filtered[key]=np.nanmean(masked_cube)


#    mask=cube.data<Temp_min
    plt.subplot(5,5,i)

#    masked_cube=cube.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
#    masked_cube=cube_CDNCP.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube[12,:,:].data)

    plt.title(key)
    plt.imshow(cube_CDNC.data[:,:])
    plt.colorbar()
#    print cube
    i=i+1
#LWP_dict['C2_GLOBAL']=LWP_dict['C1_GLOBAL']#fix to avoid breaking, correct!! also the global runs will give more problems as there is not enough low cloud
#%%

#np.save(pspc_fol+'LWP_dict',LWP_dict)
#np.save(pspc_fol+'LWP_dict_filtered',LWP_dict_filtered)
list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['y','r','green','brown','k','grey','silver']
list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','brown','k','grey','silver']
list_clouds=['C1','C2','C3']

#CDNC_dict['C3_VT17_MEAN']
for cloud in list_clouds:
    CDNC_dict[cloud+'_SATELLITE']=np.nanmedian(CDNC_satellite_dict[cloud+'_SATELLITE'])*1e6
    CDNC_dict_filtered[cloud+'_SATELLITE']=np.nanmean(CDNC_satellite_dict[cloud+'_SATELLITE'])*1e6
    CDNC_dict_std[cloud+'_SATELLITE']=np.nanstd(CDNC_satellite_dict[cloud+'_SATELLITE'])*1e6

#CDNC_dict['C3_SATELLITE']=0
#CDNC_dict['C1_SATELLITE']=0
#CDNC_dict['C2_SATELLITE']=0
N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
fig, ax = plt.subplots()
width = 0.1       # the width of the bars
iparam=0
list_params=['SATELLITE','M92','DM10','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','r','green','peru','k','grey','silver']
list_params=['SATELLITE','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
for param in list_params:
    print param
    
    means = tuple([CDNC_dict[cloud+'_'+param]*1e-6 for cloud in list_clouds])
    if param=='SATELLITE':
        std = tuple([CDNC_dict_std[cloud+'_'+param]*1e-6*2 for cloud in list_clouds])
    else:
        std = tuple([0 for cloud in list_clouds])

    rects1 = ax.bar(ind+iparam*width, means, width, color=list_colors[iparam], yerr=std,label=param,error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))
    iparam=iparam+1
plt.legend()
ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
ax.set_xticklabels(tuple(list_clouds))
ax.set_title('CDNC')
ax.set_ylabel('CDNC $\mathrm{(cm^{-3})}$')
#plt.ylim(0,0.25)
#plt.xlim(0,5)
#plt.ylim(0,280)


plt.savefig(sav_fol+'CDNC_barplot.png')
plt.savefig(sav_fol+'CDNC_barplot.eps')

#%%

#for c in cube:
#    print c._attributes['STASH'].item
#    if c._attributes['STASH'].item=='208':
#        print c
