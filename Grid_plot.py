#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 10:19:58 2017

@author: eejvt
"""

from base_imports import *
from SW_satellite import SW_satellite_dict
from LWP_satellite import LWP_satellite_dict

congrid=True
no_bounds=True
cut=50

plt.figure(figsize=(40,20))
#plt.figure()

list_params=['SAT','GLOBAL','M92','DM10','VT17_MEAN']
list_colors=['b','y','r','green','grey']
list_clouds=['C1','C2','C3']

levels_sw=np.linspace(0,800,15).tolist()
levels_lwp=np.linspace(0,0.5,15).tolist()

ix=len(list_params)
iy=len(list_clouds)

clean_value=50
iplot=1
icloud=0
cmap=plt.cm.Reds
levels_LWP=np.linspace(0,0.5,3).tolist()
#levels_LWP=[0.1,0.2,0.3,0.4,0.5]
levels_LWP=np.linspace(0,0.5,11).tolist()
#levels_LWP[0]=0.001
LWP_dict=OrderedDict()

for cloud in list_clouds:
    LWP_dict[cloud]=OrderedDict()
    print cloud
    iparam=0
    itime=cloud_it[cloud]
    for param in list_params:
        name=cloud+'_'+param
        print name
        cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[cloud+'_M92']+'L1/','LWP'))[0],clean_value)
        if param=='SAT':
            LWP=LWP_satellite_dict[name]
            LWP=LWP[clean_value:,clean_value:]
            LWP=LWP[:-clean_value,:-clean_value]
            cube=cube_high_res.copy()
            cube.data[:,:,:]=np.nan
            cube.data[itime,:,:]=LWP
        elif param=='GLOBAL':
            cube=iris.load(ukl.Obtain_name(run_path[name]+'L1/','LWP'))[0]
            cube = cube.regrid(cube_high_res, iris.analysis.Linear())
        else:
            cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[name]+'L1/','LWP'))[0],clean_value)
        model_lons,model_lats=stc.unrotated_grid(cube_high_res)
        X,Y=np.meshgrid(model_lons, model_lats)

        plt.subplot(iy,ix,iplot)
        plt.title(name)
        CS=plt.contourf(X,Y,cube[itime,:,:].data,levels_LWP) 
        LWP_dict[cloud][name]=cube[itime,:,:].data
#        plt.clabel(CS, inline=1, fmt='%1.0f')
        plt.colorbar()
        iplot=iplot+1
plt.savefig(sav_fol+'Grid_LWP.png')

#%%
iplot=1
plt.figure(figsize=(40,20))
cmap=plt.cm.RdBu_r
#plt.figure()
levels_SW=np.linspace(0,750,15).tolist()
for cloud in list_clouds:
    print cloud
    iparam=0
    itime=cloud_it[cloud]
    for param in list_params:
        name=cloud+'_'+param
        print name
        cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[cloud+'_M92']+'All_time_steps/','m01s01i208'))[0],clean_value)
        if param=='SAT':
            SW=SW_satellite_dict[name]
            SW=SW[clean_value:,clean_value:]
            SW=SW[:-clean_value,:-clean_value]
            cube=cube_high_res.copy()
            cube.data[:,:,:]=np.nan
            cube.data[itime,:,:]=SW
        elif param=='GLOBAL':
            cube=iris.load(ukl.Obtain_name(run_path[name]+'All_time_steps/','m01s01i208'))[0]
            cube = cube.regrid(cube_high_res, iris.analysis.Linear())
        else:
            cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[name]+'All_time_steps/','m01s01i208'))[0],clean_value)
        model_lons,model_lats=stc.unrotated_grid(cube_high_res)
        X,Y=np.meshgrid(model_lons, model_lats)

        plt.subplot(iy,ix,iplot)
        plt.title(name)
        plt.contourf(X,Y,cube[itime,:,:].data,levels_SW,cmap=cmap) 
        cb=plt.colorbar()
        if list_params[-1]==param:
            cb.set_label('$W/m^2$')
        iplot=iplot+1
plt.savefig(sav_fol+'Grid_SW.png')
#plt.contourf(cube[itime,].data)            
        

#%%
#variable='SW'
#for cloud in list_clouds:
#
#LWP_dict
#bins=np.linspace(0,850,15).tolist()
#stc.plot_PDF(runs_dict,bins,variable_name=variable)
#
#
#




