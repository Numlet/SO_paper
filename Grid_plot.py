#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 10:19:58 2017

@author: eejvt
"""

from base_imports import *
from SW_satellite import SW_satellite_dict
from LWP_satellite import LWP_satellite_dict
from mpl_toolkits.axes_grid1 import make_axes_locatable

congrid=True
no_bounds=True
cut=50
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as plticker

#%%
plt.figure(figsize=(25,10))
#plt.figure()

mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['font.size'] = 14
mpl.rcParams['legend.fontsize']= 12

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','grey']
list_clouds=['C1','C2','C3']

levels_sw=np.linspace(0,800,15).tolist()
levels_lwp=np.linspace(0,0.5,15).tolist()

ix=len(list_params)
iy=len(list_clouds)

clean_value=50
iplot=1
icloud=0
#cmap=plt.cm.Reds
levels_LWP=np.linspace(0,0.5,3).tolist()
#levels_LWP=[0.1,0.2,0.3,0.4,0.5]
levels_LWP=np.linspace(0,0.6,11).tolist()
#levels_LWP[0]=0.001
LWP_dict=OrderedDict()
cmap=plt.cm.RdBu_r
for cloud in list_clouds:
    LWP_dict[cloud]=OrderedDict()
    print cloud
    iparam=0
    itime=cloud_it[cloud]
    for param in list_params:
        name=cloud+'_'+param
        print name
        cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[cloud+'_M92']+'A_TRAIN_COLLOCATED/','LWP'))[0],clean_value)
        if param=='SATELLITE':
            LWP=LWP_satellite_dict[name]
            LWP=LWP[clean_value:,clean_value:]
            LWP=LWP[:-clean_value,:-clean_value]
            cube=cube_high_res.copy()
            cube.data[:,:]=np.nan
            cube.data[:,:]=LWP
        elif param=='GLOBAL':
            cube=iris.load(ukl.Obtain_name(run_path[name]+'A_TRAIN_COLLOCATED/','LWP'))[0]
            cube = cube.regrid(cube_high_res, iris.analysis.Linear())
        else:
            cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[name]+'A_TRAIN_COLLOCATED/','LWP'))[0],clean_value)
        model_lons,model_lats=stc.unrotated_grid(cube_high_res)
        X,Y=np.meshgrid(model_lons, model_lats)

        ax=plt.subplot(iy,ix,iplot)
        plt.title(name)
        im=plt.contourf(X,Y,cube[:,:].data,levels_LWP,cmap=cmap) 
        LWP_dict[cloud][name]=cube[:,:].data
#        plt.clabel(CS, inline=1, fmt='%1.0f')
        loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
        ax.xaxis.set_major_locator(loc)
        if param==list_params[-1]:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)

            cb=plt.colorbar(im, cax=cax)
            cb.set_label('$mm$')
        iplot=iplot+1
#plt.savefig(sav_fol+'Grid_LWP.png')

#%%
iplot=1
plt.figure(figsize=(25,10))
cmap=plt.cm.RdBu_r
#plt.figure()
levels_SW=np.linspace(0,700,15).tolist()
for cloud in list_clouds:
    print cloud
    iparam=0
    
    for param in list_params:
        name=cloud+'_'+param
        itime=cloud_it[cloud]
        
        print name
        
        if name=='C3_DM10':
            itime=11
        
        cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[cloud+'_M92']+'A_TRAIN_COLLOCATED/','m01s01i208'))[0],clean_value)
        if param=='SATELLITE':
            SW=SW_satellite_dict[name]
            SW=SW[clean_value:,clean_value:]
            SW=SW[:-clean_value,:-clean_value]
            cube=cube_high_res.copy()
            cube.data[:,:]=np.nan
            cube.data[:,:]=SW
        elif param=='GLOBAL':
            cube=iris.load(ukl.Obtain_name(run_path[name]+'A_TRAIN_COLLOCATED/','m01s01i208'))[0]
            cube = cube.regrid(cube_high_res, iris.analysis.Linear())
        else:
            cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[name]+'A_TRAIN_COLLOCATED/','m01s01i208'))[0],clean_value)
        model_lons,model_lats=stc.unrotated_grid(cube_high_res)
        X,Y=np.meshgrid(model_lons, model_lats)

        ax=plt.subplot(iy,ix,iplot)
        plt.title(name)
        im=plt.contourf(X,Y,cube[:,:].data,levels_SW,cmap=cmap) 
        loc = plticker.MultipleLocator(base=3.0) # this locator puts ticks at regular intervals
        ax.xaxis.set_major_locator(loc)
        if param==list_params[-1]:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)

            cb=plt.colorbar(im, cax=cax)
#            cb=plt.colorbar()
            cb.set_label('$W/m^2$')
        iplot=iplot+1
#plt.savefig(sav_fol+'Grid_SW.png')
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




