#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:34:03 2017

@author: eejvt
"""

from base_imports import *

import matplotlib as mpl
mpl.rcParams['legend.frameon'] = 'False'

#from LWP_low_cloud import LWP_dict
#from SW_low_cloud import SW_dict
LWP_dict=np.load(pspc_fol+'LWP_dict.npy').item()
SW_dict=np.load(pspc_fol+'SW_dict.npy').item()
LWP_dict=np.load(pspc_fol+'LWP_dict_filtered.npy').item()
SW_dict=np.load(pspc_fol+'SW_dict_filtered.npy').item()


Temp_min=-25
#Temp_min=0
#SW_dict=OrderedDict()


plt.figure(figsize=(20,20))
i=1
itime=12

INP_dict=OrderedDict()
INP_median_dict=OrderedDict()
INP_max_dict=OrderedDict()
INP_min_dict=OrderedDict()
INP_99_dict=OrderedDict()
INP_1_dict=OrderedDict()

INPs=[]
WaterContents=[]
for key in run_path:
    if 'C1' in key:
        itime=16
#        continue
    if 'C2' in key:
        itime=16
    if 'C3' in key:
        itime=12
    if 'C3_DM10' in key:
        itime=11
#    print key
    if 'GLOBAL' in key:
        continue
    itime=12
    cube=stc.clean_cube(iris.load(run_path[key]+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]

    cube_SW=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0])[itime,:,:]
    cube_water=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s00i254_mass_fraction_of_cloud_liquid_water_in_air.nc')[0])[itime,:,:]
    cube_ice=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s00i012_mass_fraction_of_cloud_ice_in_air.nc')[0])[itime,:,:]
    cube_cloud=cube_water+cube_ice
    cube_temp=stc.clean_cube(iris.load(run_path[key]+'L1/L1_temperature_Temperature.nc')[0])[itime,:,:]
    cube_temp_C=cube_temp-273.15

    cube_water_conc=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'L1/','L1_mcon_lw_Mass'))[0])[itime,:,:]


#    SW_dict[key]=cube_SW.data.mean()
    
    mask=cube_water.data<1e-5

    temps_for_param=cube_temp_C.data
    temps_for_param[mask]=np.nan
#    print pspc_fol+key
#    temps_for_param[temps_for_param<Temp_min]=np.nan
    temps_for_param[temps_for_param>0]=np.nan
    t=np.sort(temps_for_param[~np.isnan(temps_for_param)])
#    t=t[~np.isnan(t)]
    t_84=t[len(t)*0.84]
    t_16=t[len(t)*0.16]

    t_99=t[len(t)*0.97]
    t_1=t[len(t)*0.03]
#    temps_for_param[temps_for_param>t_5]=np.nan
#    temps_for_param[temps_for_param<t_95]=np.nan
    INP=param[key[3:]](temps_for_param)
    np.save(pspc_fol+'temps_'+key,temps_for_param)
    INP[INP==0]=np.nan
    INP=INP.flatten()
    INP=INP[np.logical_not(np.isnan(INP))]
    np.save(pspc_fol+'INP_'+key,INP)

    
    mean_INP=np.mean(INP)
    median_INP=param[key[3:]](np.median(temps_for_param[~np.isnan(temps_for_param)]))
    max_INP=param[key[3:]](t_84)
    min_INP=param[key[3:]](t_16)
    max99_INP=param[key[3:]](t_99)
    min1_INP=param[key[3:]](t_1)
#    plt.hist(t,100)
#    plt.axvline(t_16,c='k')
#    plt.axvline(t_84,c='b')
#    plt.axvline(t[len(t)*0.5],c='r')
#    plt.axvline(np.median(temps_for_param[~np.isnan(temps_for_param)]),c='g')
    


    print key,np.median(temps_for_param[~np.isnan(temps_for_param)]), median_INP
    WC=cube_water.data
    WC=WC[~np.isnan(temps_for_param)]
#    WC=WC[np.logical_not(np.isnan(WC))]



    INP_min_dict[key]=min_INP
    INP_max_dict[key]=max_INP

    INP_1_dict[key]=min1_INP
    INP_99_dict[key]=max99_INP
    
    INP_median_dict[key]=median_INP
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
#    print cube
    i=i+1

#%%



#from LWP_low_cloud import LWP_dict
#from SW_low_cloud import SW_dict
LWP_dict=np.load(pspc_fol+'LWP_dict.npy').item()
SW_dict=np.load(pspc_fol+'SW_dict.npy').item()
LWP_dict=np.load(pspc_fol+'LWP_dict_filtered.npy').item()
SW_dict=np.load(pspc_fol+'SW_dict_filtered.npy').item()


Temp_min=-25
#Temp_min=0
#SW_dict=OrderedDict()


plt.figure(figsize=(20,20))
i=1
itime=12
INP_dict=OrderedDict()
INP_median_dict=OrderedDict()
INP_max_dict=OrderedDict()
INP_min_dict=OrderedDict()
INP_99_dict=OrderedDict()
INP_1_dict=OrderedDict()

INPs=[]
WaterContents=[]
for key in run_path:
    if 'C1' in key:
        itime=16
#        continue
    if 'C2' in key:
        itime=16
    if 'C3' in key:
        itime=12
    if 'C3_DM10' in key:
        itime=11
#    print key
    if 'GLOBAL' in key:
        continue

    cube=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_CTT_Cloud_top_temperatureA-train_collocated.nc')[0])[:,:]

    cube_SW=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s01i208_toa_outgoing_shortwave_fluxA-train_collocated.nc')[0])[:,:]
    cube_water=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s00i254_mass_fraction_of_cloud_liquid_water_in_airA-train_collocated.nc')[0])[:,:]
    cube_ice=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/All_time_steps_m01s00i012_mass_fraction_of_cloud_ice_in_airA-train_collocated.nc')[0])[:,:]
    cube_cloud=cube_water+cube_ice
    cube_temp=stc.clean_cube(iris.load(run_path[key]+'A_TRAIN_COLLOCATED/L1_temperature_TemperatureA-train_collocated.nc')[0])[:,:]
    cube_temp_C=cube_temp-273.15

    cube_water_conc=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'A_TRAIN_COLLOCATED/','L1_mcon_lw_Mass'))[0])[:,:]


    mask=cube_water.data<1e-5

    temps_for_param=cube_temp_C.data
    temps_for_param[mask]=np.nan
#    print pspc_fol+key
#    temps_for_param[temps_for_param<Temp_min]=np.nan
    temps_for_param[temps_for_param>0]=np.nan
    t=np.sort(temps_for_param[~np.isnan(temps_for_param)])
#    t=t[~np.isnan(t)]
    t_84=t[len(t)*0.84]
    t_16=t[len(t)*0.16]

    t_99=t[len(t)*0.97]
    t_1=t[len(t)*0.03]
#    temps_for_param[temps_for_param>t_5]=np.nan
#    temps_for_param[temps_for_param<t_95]=np.nan
    INP=param[key[3:]](temps_for_param)
    np.save(pspc_fol+'temps_'+key,temps_for_param)
    INP[INP==0]=np.nan
    INP=INP.flatten()
    INP=INP[np.logical_not(np.isnan(INP))]
    np.save(pspc_fol+'INP_'+key,INP)

    
    mean_INP=np.mean(INP)
    median_INP=param[key[3:]](np.median(temps_for_param[~np.isnan(temps_for_param)]))
    max_INP=param[key[3:]](t_84)
    min_INP=param[key[3:]](t_16)
    max99_INP=param[key[3:]](t_99)
    min1_INP=param[key[3:]](t_1)
#    plt.hist(t,100)
#    plt.axvline(t_16,c='k')
#    plt.axvline(t_84,c='b')
#    plt.axvline(t[len(t)*0.5],c='r')
#    plt.axvline(np.median(temps_for_param[~np.isnan(temps_for_param)]),c='g')
    


    print key,np.median(temps_for_param[~np.isnan(temps_for_param)]), median_INP
    WC=cube_water.data
    WC=WC[~np.isnan(temps_for_param)]
#    WC=WC[np.logical_not(np.isnan(WC))]



    INP_min_dict[key]=min_INP
    INP_max_dict[key]=max_INP

    INP_1_dict[key]=min1_INP
    INP_99_dict[key]=max99_INP
    
    INP_median_dict[key]=median_INP
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
#    print cube
    i=i+1











#%%
from scipy.optimize import curve_fit

def f(x, A, B): # this is your 'straight line' y=f(x)
    return A*x + B



list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']
list_markers=['o','^','*']
#SW_dict['C1_SATELLITE']=0
#SW_dict['C2_SATELLITE']=0
#SW_dict['C3_SATELLITE']=0
N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
fig, ax = plt.subplots()
width = 0.1       # the width of the bars
iparam=0
plt.figure(figsize=(16,6))

ax=plt.subplot(1,2,1)
bx=plt.subplot(1,2,2)

for i in range(N):
    # bx.axhline(SW_dict[list_clouds[i]+'_SAT'],color='b',lw=2,label='Satellite',ls='--')
    # ax.axhline(LWP_dict[list_clouds[i]+'_SAT'],color='b',lw=2,label='Satellite',ls='--')
    cloud_lwp=[]
    cloud_sw=[]
    cloud_inp=[]
    
    for iparam in range(len(list_params)):
        if list_params[iparam] =='GLOBAL':
            continue
        key=list_clouds[i]+'_'+list_params[iparam]
        msize=150
        ax.errorbar(INP_median_dict[key]*1e-3,LWP_dict[key],
                    xerr=[[INP_median_dict[key]*1e-3-INP_min_dict[key]*1e-3],[INP_max_dict[key]*1e-3-INP_median_dict[key]*1e-3]],
                    linestyle="None",c='k',zorder=1,elinewidth=2)
        bx.errorbar(INP_median_dict[key]*1e-3,SW_dict[key],
                    xerr=[[INP_median_dict[key]*1e-3-INP_min_dict[key]*1e-3],[INP_max_dict[key]*1e-3-INP_median_dict[key]*1e-3]],
                    linestyle="None",c='k',zorder=1,elinewidth=2)
        
        dashax=ax.errorbar(INP_median_dict[key]*1e-3,LWP_dict[key],
                    xerr=[[INP_median_dict[key]*1e-3-INP_1_dict[key]*1e-3],[INP_99_dict[key]*1e-3-INP_median_dict[key]*1e-3]],
                    linestyle="None",c='k',zorder=1,ls='-.')
        dashbx=bx.errorbar(INP_median_dict[key]*1e-3,SW_dict[key],
                    xerr=[[INP_median_dict[key]*1e-3-INP_1_dict[key]*1e-3],[INP_99_dict[key]*1e-3-INP_median_dict[key]*1e-3]],
                    linestyle="None",c='k',zorder=1,ls='-.')
        dashax[-1][0].set_linestyle('-.')
        dashbx[-1][0].set_linestyle('-.')
#        ax.scatter(INP_median_dict[key]*1e-3,LWP_dict[key],c=list_colors[iparam],s=msize,lw=1,marker=list_markers[i])
#        bx.scatter(INP_median_dict[key]*1e-3,SW_dict[key],c=list_colors[iparam],s=msize,lw=1,marker=list_markers[i])
        ax.scatter(INP_median_dict[key]*1e-3,LWP_dict[key],c=list_colors[iparam],s=msize,lw=1,marker=list_markers[i], linewidth='0')
        bx.scatter(INP_median_dict[key]*1e-3,SW_dict[key],c=list_colors[iparam],s=msize,lw=1,marker=list_markers[i], linewidth='0')
        cloud_inp.append(INP_median_dict[key]*1e-3)
        cloud_sw.append(SW_dict[key])
        cloud_lwp.append(LWP_dict[key])
        
        
#        ax.errorbar(INP_median_dict[key]*1e-3,LWP_dict[key],xerr=[[INP_median_dict[key]*1e-3-INP_min_dict[key]*1e-3,INP_max_dict[key]*1e-3-INP_median_dict[key]*1e-3]], linestyle="None",c='k')
#        bx.errorbar([INP_median_dict[key]*1e-3],[LWP_dict[key]],xerr=[[INP_median_dict[key]*1e-3-INP_min_dict[key]*1e-3,INP_max_dict[key]*1e-3-INP_median_dict[key]*1e-3]], linestyle="None",c='k')
        # if i==2 or i==5:
            # bx.legend(prop={'size':8})
#            bx.legend()
#        if i==0:
#            ax.scatter([],[],label=list_params[iparam],marker='o',c=list_colors[iparam])
        bx.set_xlabel('[INP] ($\mathrm{L^{-1}}$)')
        ax.set_xlabel('[INP] ($\mathrm{L^{-1}}$)')
#        break
    bx.scatter([],[],label=list_clouds[i],marker=list_markers[i],c='k')
    ax.scatter([],[],label=list_clouds[i],marker=list_markers[i],c='k')
#    x = 1e-2
    A,B = curve_fit(f, np.log(cloud_inp),cloud_lwp)[0]
    cloud_sw=np.array(cloud_sw)[np.array(cloud_inp)<2]
    cloud_inp_for_sw=np.array(cloud_inp)[np.array(cloud_inp)<2]
    C,D = curve_fit(f, np.log(cloud_inp_for_sw),cloud_sw)[0]
#    y = 350
    INPs=np.logspace(-7,1)
    print A,B,C,D
    print 'Slope SW=',C
    print i
    ax.plot(INPs,f(np.log(INPs),A,B),'--',label='Fit to:'+list_clouds[i]+' $\mathrm{R^2=}$%1.2f'%np.corrcoef(np.log(cloud_inp),cloud_lwp)[0,1]**2)
    bx.plot(INPs,f(np.log(INPs),C,D),'--',label='Fit to:'+list_clouds[i]+' $\mathrm{R^2=}$%1.2f'%np.corrcoef(np.log(cloud_inp_for_sw),cloud_sw)[0,1]**2)
#    ax.grid()
#    bx.grid()
#    xerr = 9e-3
#    bx.errorbar(x, y, xerr=[[xerr], [2*xerr]],linestyle="None",c='k')
#    bx.errorbar(1e-2,250,xerr=[[1e-4],[1e-1]],c='k')
    ax.set_ylabel('Liquid Water Path (mm)')
    bx.set_ylabel('Reflected SW radiation ($\mathrm{W/m^2}$)')
    ax.set_xlim(1e-8,1e2)
    bx.set_xlim(1e-8,1e2)
    ax.set_title('a) Liquid Water Path ')
    bx.set_title('b) Reflected SW radiation ')
    ax.set_xscale('log')
    bx.set_xscale('log')
bx.legend(loc='best')
ax.legend(loc='best')
plt.savefig(sav_fol+'INP_relation.png')
plt.savefig(sav_fol+'INP_relation.eps')



#plt.legend()
#ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
#ax.set_xticklabels(tuple(list_clouds))
#ax.set_ylabel('LWP mm')
#plt.ylim(0,0.25)

#%%
#for i in range(100):
#    plt.close()


#%%
# plt.figure()
# list_colors=['b','y','r','green','brown','k','grey','silver','lime','violet','g','m','c','ivory','beige']
#
# for i in range(len(INPs)):
#     plt.scatter(INPs[i],WaterContents[i],c=list_colors[i],s=1, lw = 0)
# plt.xscale('log')
# plt.yscale('log')
# plt.ylim(1e-7,1e-3)
# plt.show()
#
#
# #%%
# plt.figure()
# plt.hist(temps_for_param[~np.isnan(temps_for_param)])#,np.logspace(-8,-2,30).tolist())
# #plt.xscale('log')
# plt.yscale('log')
#
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
