#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 09:41:40 2017

@author: eejvt
"""

from base_imports import *
import matplotlib as mpl
mpl.rcParams['legend.frameon']=False

list_params=['GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['y','r','green','brown','k','grey','silver']
list_clouds=['C1','C2','C3']
plt.close()
plt.close()
plt.close()
#    rain_mmr=iris.load_cube(path+'All_time_steps/'+'All_time_steps_m01s00i272_RAIN_AFTER_TIMESTEP_________________.nc')
'All_time_steps_m01s00i079_SNOW_NUMBER_AFTER_TIMESTEP__________.nc'
var='IWP'
var='L1_RWP_Rain_water_path.nc'
variables=['IWP','LWP','RWP']
variables=['SNOW']#,'LWP','RWP']
clean_value=50
for cloud in list_clouds:
    print cloud
    plt.figure()
    iparam=0
    plt.title(cloud+' ' +var)
    itime=cloud_it[cloud]
    icol=0
    for param in list_params:
        for var in variables:
            name=cloud+'_'+param
            print name
#            cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[cloud+'_M92']+'L1/',var))[0])
#            cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[cloud+'_M92']+'L1/',var))[0])
            if param=='GLOBAL':
                continue
#                cube=iris.load(ukl.Obtain_name(run_path[name]+'L1/',var))[0]
#                cube = cube.regrid(cube_high_res, iris.analysis.Linear())
            else:
#                cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[name]+'L1/',var))[0],clean_value)
                cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[name]+'All_time_steps/','SNOW_NUMBER_AFTER_TIMESTEP'))[0],clean_value)
            model_lons,model_lats=stc.unrotated_grid(cube_high_res)
            X,Y=np.meshgrid(model_lons, model_lats)
            times=cube.coord('time').points[1:]
#            rain=cube.data.mean(axis=(1,2))[1:]
            rain=cube.data.mean(axis=(2,3))[1:].sum(axis=1)
            if var=='IWP':ls='--'
            if var=='RWP':ls='-.'
            if var=='LWP':ls='-'
            plt.plot(times, rain,ls=ls,c=list_colors[icol],lw=4,label=list_params[icol])
            plt.yscale('log')
            plt.xlabel('time')
            plt.ylabel('Snow number')
            plt.title('Snow number')
        plt.legend(loc='best')
        icol=icol+1
        plt.savefig('/nfs/see-fs-01_users/eejvt/CASIM_hydrometeors/snow_number.png')
#            plt.legend()








#%%












