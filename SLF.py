#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:25:42 2017

@author: eejvt
"""

from base_imports import *


LF=iris.load_cube('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/MEYERS/L1/L1_CT_SLF_supercooled_liquid_fraction_at_cloud_top.nc')
plt.imshow(LF[13,:,:].data)
print np.nanmean(LF[13,:,:].data)
plt.colorbar()
LF=iris.load_cube('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/GLO_MEAN/L1/L1_CT_SLF_supercooled_liquid_fraction_at_cloud_top.nc')
plt.imshow(LF[13,:,:].data)
print np.nanmean(LF[13,:,:].data)
plt.colorbar()
