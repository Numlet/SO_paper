#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 17:33:11 2017

@author: eejvt
"""


from base_imports import *
#from CDNC_satellite import CDNC_satellite_dict

from LF_OP_satellite import LF_OP_satellite_dict,LF_OP_satellite_dict_undeterminated
from LF_IR_satellite import LF_IR_satellite_dict,LF_IR_satellite_dict_undeterminated

Temp_min=-35+273.15
#Temp_min=0

CTPhase_liquid=OrderedDict()
CTPhase_ice=OrderedDict()
CTPhase_mixed=OrderedDict()


plt.figure(figsize=(20,20))
i=1

for key in run_path:
    print key
    if 'C1' in key:itime=16
    if 'C2' in key:itime=17
    if 'C3' in key:itime=13
    if 'GLOBAL' in key:
        sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
        CTTice=iris.load(run_path[key]+'L1/L1_CTT_ICE_Cloud_ice_top_temperature.nc')[0][itime,]
        CTTice = CTTice.regrid(sample_cube, iris.analysis.Linear())
        CTTliquid=iris.load(run_path[key]+'L1/L1_CTT_LIQUID_Cloud_liquid_top_temperature.nc')[0][itime,]
        CTTliquid = CTTliquid.regrid(sample_cube, iris.analysis.Linear())
    else:
#    if 'C3_DM10' in key:continue
#    if 'C3_DM15' in key:continue
        CTTice=iris.load(run_path[key]+'L1/L1_CTT_ICE_Cloud_ice_top_temperature.nc')[0][itime,]
        CTTliquid=iris.load(run_path[key]+'L1/L1_CTT_LIQUID_Cloud_liquid_top_temperature.nc')[0][itime,]

    CTPhase=CTTliquid*0+1
    CTPhase=CTTliquid*0+1
    
    CTPhase.units=''
    CTPhase.data[CTTice.data>CTTliquid.data]=1#liquid
    CTPhase.data[CTTice.data<CTTliquid.data]=2#ice
    CTPhase.data[CTTice.data==CTTliquid.data]=3#mixed
    CTPhase.data[np.isnan(CTTliquid.data)]=0#no_cloud
#    CTPhase=iris.load(run_path[key]+'L1/L1_CTPhase_Cloud_top_phase.nc')[0][itime,]
    CTPhase_liquid[key]=float(np.array([CTPhase.data==1]).sum())/(np.array([CTPhase.data==1]).sum()+np.array([CTPhase.data==3]).sum()+np.array([CTPhase.data==2]).sum())
    CTPhase_ice[key]=float(np.array([CTPhase.data==2]).sum())/(np.array([CTPhase.data==1]).sum()+np.array([CTPhase.data==3]).sum()+np.array([CTPhase.data==2]).sum())
    CTPhase_mixed[key]=float(np.array([CTPhase.data==3]).sum())/(np.array([CTPhase.data==1]).sum()+np.array([CTPhase.data==3]).sum()+np.array([CTPhase.data==2]).sum())
    plt.subplot(6,5,i)
    plt.title(key)
    print key,  str(CTPhase_liquid[key])+' '+str(CTPhase_mixed[key])+ ' '+str(CTPhase_ice[key])
    plt.imshow(CTPhase.data)
#    plt.imshow(CTTliquid.data)
    plt.colorbar()
    i=i+1
#%%


list_params=['SATELLITE','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_params=['SATELLITE_IR','SATELLITE_OP','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['royalblue','cyan','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    CTPhase_liquid[cloud+'_SATELLITE_OP']=LF_OP_satellite_dict[cloud+'_SATELLITE']-LF_OP_satellite_dict_undeterminated[cloud+'_SATELLITE']
    CTPhase_mixed[cloud+'_SATELLITE_OP']=LF_OP_satellite_dict_undeterminated[cloud+'_SATELLITE']
    CTPhase_ice[cloud+'_SATELLITE_OP']=1-CTPhase_liquid[cloud+'_SATELLITE_OP']
    CTPhase_liquid[cloud+'_SATELLITE_IR']=LF_IR_satellite_dict[cloud+'_SATELLITE']
    CTPhase_mixed[cloud+'_SATELLITE_IR']=LF_IR_satellite_dict_undeterminated[cloud+'_SATELLITE']
    CTPhase_ice[cloud+'_SATELLITE_IR']=1-CTPhase_liquid[cloud+'_SATELLITE_IR']-CTPhase_mixed[cloud+'_SATELLITE_IR']

N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
plt.figure(figsize=(15,6))
fig, ax = plt.subplots(figsize=(20,10))
width = 0.1       # the width of the bars
iparam=0

for param in list_params:
    print param
    means_liquid = tuple([CTPhase_liquid[cloud+'_'+param] for cloud in list_clouds])
    means_mixed = tuple([CTPhase_mixed[cloud+'_'+param] for cloud in list_clouds])
    means_ice = tuple([1-CTPhase_liquid[cloud+'_'+param]-CTPhase_mixed[cloud+'_'+param] for cloud in list_clouds])
    means_total = tuple([1 for cloud in list_clouds])
    means_mixliq = tuple([CTPhase_liquid[cloud+'_'+param] + CTPhase_mixed[cloud+'_'+param] for cloud in list_clouds])

    

    rects1 = ax.bar(ind+iparam*width+0.1, means_liquid, width, color=list_colors[iparam], label=param,hatch='.')
    rects1 = ax.bar(ind+iparam*width+0.1, means_mixed, width,bottom=means_liquid, color=list_colors[iparam], alpha=0.3,hatch='\\')
    rects1 = ax.bar(ind+iparam*width+0.1, means_ice, width,bottom=means_mixliq, color=list_colors[iparam],alpha=0.0)#,hatch='*')
    iparam=iparam+1
rects1 = ax.bar(0,0, 0, color='powderblue', label='Mixed-phase/Uncertain',hatch='\\')
#rects1 = ax.bar(0,0, 0, color='powderblue', label='Ice',hatch='*')
rects1 = ax.bar(0,0, 0, color='powderblue', label='Liquid',hatch='.')
plt.legend()
ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
ax.set_xticklabels(tuple(list_clouds))
ax.set_title('Cloud top phase Optical Properties (OP) and Infrared (IR)')
ax.set_ylabel('')
#plt.ylim(0,0.25)
plt.ylabel('Phase Fraction')
plt.xlim(0,4)
#plt.ylim(0,280)


plt.savefig(sav_fol+'CTPhase_Optical_barplot.png')
plt.savefig(sav_fol+'CTPhase_Optical_barplot.eps')
plt.show()
#%%



#CTPhase=temp_cloud_top*0+1













