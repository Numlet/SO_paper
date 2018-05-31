#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:31:44 2017

@author: eejvt
"""

from base_imports import *




#%%
path='/nfs/a201/eejvt/CALIPSO_SA/'


c1_file='CAL_LID_L2_05kmCLay-Standard-V4-10.2015-03-01T16-23-33ZD.nc'


cubes=iris.load(path+c1_file)
for cube in cubes:
    name=cube.name()
    if not '/' in name: print name