#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:33:55 2017

@author: eejvt
"""
from base_imports import *

run_path={}
run_path['C3_M92_HIGH']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/MEYERS/'#
run_path['C3_M92_LOW']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/MEYERS_RIGHT_PROFILE/'#

cube_sw_high=iris.load('/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/MEYERS/A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0]
cube_sw_high=stc.clean_cube(cube_sw_high)


cube_sw_low=iris.load('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/MEYERS_RIGHT_PROFILE/A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0]
cube_sw_low=stc.clean_cube(cube_sw_low)

cube_cdnc_high=iris.load('/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/MEYERS/A_TRAIN_COLLOCATED/L1_CDNC_max_cloud_water_Cloud_droplet_concentratio_at_maximum_cloud_water_contentA-train_collocated.nc')[0]
cube_cdnc_high=stc.clean_cube(cube_cdnc_high)





cube_cdnc_low=iris.load('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/MEYERS_RIGHT_PROFILE/A_TRAIN_COLLOCATED/L1_CDNC_max_cloud_water_Cloud_droplet_concentratio_at_maximum_cloud_water_contentA-train_collocated.nc')[0]
cube_cdnc_low=stc.clean_cube(cube_cdnc_low)

LWP_min=0.01
#LWP_min=0.00000
for key in run_path:
    if 'C3' in key:
        itime=13
        if key=='C3_DM10':
            itime=12
    if 'C1' in key:
        itime=16
    if 'C2' in key:
        itime=17
    print key
    if 'GLOBAL' in key:
#        if 'C2' in key:
#            continue
        sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'A_TRAIN_COLLOCATED/L1_CTT_Cloud_top_temperatureA-train_collocated.nc')[0])[:,:]
        cube_SW=iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0][:,:]
        cube_LWP=iris.load(ukl.Obtain_name(run_path[key]+'A_TRAIN_COLLOCATED/','LWP'))[0][:,:]
        cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'A_TRAIN_COLLOCATED/L1_CTT_Cloud_top_temperatureA-train_collocated.nc')[0])[:,:]
#        cube = cube.regrid(sample_cube, iris.analysis.Linear())
        cube_LWP = cube_LWP.regrid(sample_cube, iris.analysis.Linear())
        cube_SW = cube_SW.regrid(sample_cube, iris.analysis.Linear())
    else:
        cube=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CTT_Cloud_top_temperatureA-train_collocated.nc')[0])[:,:]
        cube_LWP=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'A_TRAIN_COLLOCATED/','LWP'))[0])[:,:]
        cube_SW=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0])[:,:]
    mask=[(cube.data<Temp_min) | (cube_LWP.data<LWP_min)]
    print np.any(cube_LWP.data<LWP_min) 
#    print cube_SW.coord('time').points
    masked_cube=np.copy(cube_SW.data)
    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
#    masked_cube=cube_SW.data
#    masked_cube[mask]=np.nan

    SW_dict_mask[key]=mask
    SW_dict_data[key]=cube_SW.data
    SW_dict_filtered_data[key]=masked_cube.data
    np.save(pspc_fol+'SW_distribution_'+key,masked_cube)
    SW_dict[key]=cube_SW.data.mean()
    masked_cube[mask]=np.nan
    np.save(pspc_fol+'SW_distribution_filtered_'+key,masked_cube)
    levels=np.linspace(0,850,15).tolist()
    SW_dict_filtered[key]=np.mean(masked_cube[~np.isnan(masked_cube)])












from SW_satellite import SW_satellite_dict

plt.figure(figsize=(15,8))
ax=plt.subplot(121)

plt.bar(1, np.nanmean(CDNC_satellite_dict['C3_SATELLITE']), 1, color='b', label='SATELLITE', yerr=2*np.nanstd(CDNC_satellite_dict['C3_SATELLITE']),error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))
plt.bar(3, np.nanmean(cube_cdnc_high.data*1e-6), 1, color='r', label='M92 High aerosol')
plt.bar(2, np.nanmean(cube_cdnc_low.data*1e-6), 1, color='lightcoral', label='M92 Base aerosol')
ax.set_xticks([])
plt.ylabel('CDNC $\mathrm{(cm^{-3})}$')
plt.ylim(0,150)
plt.legend()
plt.xlim(0,5)
bx=plt.subplot(122)

plt.bar(1, np.nanmean(SW_satellite_dict['C3_SATELLITE']), 1, color='b', label='SATELLITE')
plt.bar(3, np.nanmean(SW_dict_filtered['C3_M92_HIGH']), 1, color='r', label='M92 High aerosol')
plt.bar(2, np.nanmean(SW_dict_filtered['C3_M92_LOW']), 1, color='lightcoral', label='M92 Base aerosol')
plt.xlim(0,5)
bx.set_xticks([])
fs=18
plt.ylabel('Reflected SW $\mathrm{(W/m^2)}$')
plt.text(1, np.nanmean(SW_satellite_dict['C3_SATELLITE'])+10,'%1.2f'% np.nanmean(SW_satellite_dict['C3_SATELLITE']),fontsize=fs)
plt.text(3, np.nanmean(SW_dict_filtered['C3_M92_HIGH'])+10,'%1.2f'% np.nanmean(SW_dict_filtered['C3_M92_HIGH']),fontsize=fs)
plt.text(2,  np.nanmean(SW_dict_filtered['C3_M92_LOW'])+10,'%1.2f'% np.nanmean(SW_dict_filtered['C3_M92_LOW']),fontsize=fs)
plt.ylim(000,600)
plt.savefig(sav_fol+'CCN_sensitivity.png')
plt.savefig(sav_fol+'CCN_sensitivity.eps')





