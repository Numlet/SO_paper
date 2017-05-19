#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:34:03 2017

@author: eejvt
"""

from base_imports import *

Temp_min=-100+273.15
Temp_min=0
SW_dict=OrderedDict()


plt.figure(figsize=(20,20))
i=1
itime=12
for key in run_path:
    if 'C1' in key:
        itime=11
        continue
    if 'C2' in key:
        itime=16
    if 'C3' in key:
        itime=16
    print key
    if 'GLOBAL' in key:
        continue
    cube=stc.clean_cube(iris.load(run_path[key]+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
    
    cube_SW=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0])[itime,:,:]
    
    mask=cube.data<Temp_min
    plt.subplot(5,5,i)

    masked_cube=cube.data
    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
    masked_cube=cube_SW.data
    masked_cube[mask]=np.nan
#    plt.imshow(cube[12,:,:].data)
    plt.imshow(masked_cube[:,:])
    SW_dict[key]=np.nanmean(masked_cube)
    plt.colorbar()
    print cube
    i=i+1
SW_dict['C3_GLOBAL']=SW_dict['C2_GLOBAL']