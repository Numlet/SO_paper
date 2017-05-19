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

list_params=['SAT','GLOBAL','M92','DM10','VT17_MEAN']
list_colors=['b','y','r','green','grey']
list_clouds=['C1','C2','C3']

levels_sw=np.linspace(0,800,15).tolist()
levels_lwp=np.linspace(0,0.5,15).tolist()

icloud=0
for cloud in list_clouds:
    print cloud
    iparam=0
    itime=cloud_it[key[:2]]
    for param in list_params:
        name=cloud+'_'+param
        print name
        if param=='SAT':
            LWP=LWP_satellite_dict[key]
        if param=='GLOBAL':
            cube=iris.load(run_path[key]+'/L1/L1_LWP_Liquid_water_path.nc')[0]




plt.contourf(cube[itime,].data)            
        









