#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:34:03 2017

@author: eejvt
"""

from base_imports import *
from LWP_low_cloud import LWP_dict
from SW_low_cloud import SW_dict



Temp_min=-25
#Temp_min=0
#SW_dict=OrderedDict()


plt.figure(figsize=(20,20))
i=1
itime=12
INP_dict=OrderedDict()

INPs=[]
WaterContents=[]
for key in run_path:
    if 'C1' in key:
        itime=11
#        continue
    if 'C2' in key:
        itime=16
    if 'C3' in key:
        itime=16
    print key
    if 'GLOBAL' in key:
        continue
    
    cube=stc.clean_cube(iris.load(run_path[key]+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
    
    cube_SW=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0])[itime,:,:]
    cube_water=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s00i254_mass_fraction_of_cloud_liquid_water_in_air.nc')[0])[itime,:,:]
    cube_ice=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s00i012_mass_fraction_of_cloud_ice_in_air.nc')[0])[itime,:,:]
    cube_cloud=cube_water+cube_ice
    cube_temp=stc.clean_cube(iris.load(run_path[key]+'L1/L1_temperature_Temperature.nc')[0])[itime,:,:]
    cube_temp_C=cube_temp-273.15
    
    cube_water_conc=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'L1/','L1_mcon_lw_Mass'))[0])[itime,:,:]

    mask=cube_water.data<1e-5
    temps_for_param=cube_temp_C.data
    temps_for_param[temps_for_param<Temp_min]=np.nan
    temps_for_param[temps_for_param>-2]=np.nan
    temps_for_param[mask]=np.nan
    INP=param[key[3:]](temps_for_param)
    INP[INP==0]=np.nan
    INP=INP.flatten()
    INP=INP[np.logical_not(np.isnan(INP))]
    mean_INP=np.mean(INP)
    WC=cube_water.data
    WC=WC[~np.isnan(temps_for_param)]
#    WC=WC[np.logical_not(np.isnan(WC))]

    INP_dict[key]=mean_INP
    INPs.append(INP.flatten())
    WaterContents.append(WC)
    print np.nanmax(temps_for_param),np.nanmin(temps_for_param)
    plt.subplot(4,5,i)
    plt.title(key+' %1.1e'%mean_INP)
    masked_cube=cube.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
#    masked_cube=cube_SW.data
#    masked_cube[mask]=np.nan
#    plt.imshow(cube[12,:,:].data)
    plt.imshow(masked_cube[:,:])
#    SW_dict[key]=np.nanmean(masked_cube)
    plt.colorbar()
    print cube
    i=i+1


#SW_dict['C3_GLOBAL']=SW_dict['C2_GLOBAL']

#%%

list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_MIN']
list_colors=['y','r','green','brown','k','grey','silver']
list_clouds=['C1','C2','C3']
#SW_dict['C1_SAT']=0
#SW_dict['C2_SAT']=0
#SW_dict['C3_SAT']=0
N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
fig, ax = plt.subplots()
width = 0.1       # the width of the bars
iparam=0
plt.figure(figsize=(20,20))
for i in range(N):
    ax=plt.subplot(2,3,i+1)
    bx=plt.subplot(2,3,i+1+3)
    bx.axhline(SW_dict[list_clouds[i]+'_SAT'],color='b',lw=2,label='Satellite',ls='--')
    ax.axhline(LWP_dict[list_clouds[i]+'_SAT'],color='b',lw=2,label='Satellite',ls='--')
    for iparam in range(len(list_params)):
        if list_params[iparam] =='GLOBAL':
            continue
        key=list_clouds[i]+'_'+list_params[iparam]
        ax.scatter(INP_dict[key],LWP_dict[key],c=list_colors[iparam],s=100,lw=1,label=list_params[iparam])
        bx.scatter(INP_dict[key],SW_dict[key],c=list_colors[iparam],s=100,lw=1,label=list_params[iparam])
        if i==2 or i==5:
            bx.legend()
#            bx.legend()
        bx.set_xlabel('INP')
    ax.set_ylabel('LWP')
    bx.set_ylabel('SW radiation')
    ax.set_xlim(1e-2,1e5)
    bx.set_xlim(1e-2,1e5)
    ax.set_title(list_clouds[i])
    ax.set_xscale('log')
    bx.set_xscale('log')
#plt.legend()
#ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
#ax.set_xticklabels(tuple(list_clouds))
#ax.set_ylabel('LWP mm')
#plt.ylim(0,0.25)




#%%
plt.figure()
list_colors=['b','y','r','green','brown','k','grey','silver','lime','violet','g','m','c','ivory','beige']

for i in range(len(INPs)):
    plt.scatter(INPs[i],WaterContents[i],c=list_colors[i],s=1, lw = 0)
plt.xscale('log')
plt.yscale('log')
plt.ylim(1e-7,1e-3)
plt.show()


#%%
plt.figure()
plt.hist(temps_for_param[~np.isnan(temps_for_param)])#,np.logspace(-8,-2,30).tolist())
#plt.xscale('log')
plt.yscale('log')

#%%
#data=cube_cloud.data.flatten()
#data=data[data!=0]
#data=data[data<10**-7]
#plt.hist(data,np.logspace(-10,1,100))
#plt.xscale('log')
#plt.yscale('log')
#
#plt.figure()
#plt.contourf(cube_cloud.data[30,],np.logspace(-10,1,10),levels=np.logspace(-9,1,10),cmap=plt.cm.jet,norm = LogNorm())
#plt.colorbar()
