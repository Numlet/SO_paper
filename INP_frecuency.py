#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:58:17 2017

@author: eejvt
"""


import numpy as np
import sys
sys.path.append('/nfs/see-fs-01_users/eejvt/PYTHON_CODE')
import Jesuslib as jl
import os
from scipy.io.idl import readsav
from glob import glob
from scipy.io import netcdf
import matplotlib.pyplot as plt
import scipy as sc
from scipy.stats.stats import pearsonr
from glob import glob
from scipy.io.idl import readsav
from mpl_toolkits.basemap import Basemap
import datetime
#from matplotlib.colors import logNorm
from matplotlib import colors, ticker, cm
from scipy.io import netcdf
import scipy as sc

from base_imports import *

for i in range(100):
    plt.close()

INP_feldspar_alltemps_daily=np.load('/nfs/a201/eejvt/MARINE_PARAMETERIZATION/DAILY/INP_feldext_alltemps_daily.npy', mmap_mode='r')#cm3
INP_marine_alltemps_daily=np.load('/nfs/a201/eejvt/MARINE_PARAMETERIZATION/DAILY/INP_marine_alltemps_daily.npy', mmap_mode='r')#m3
#INP_marine_alltemps=np.load('/nfs/a201/eejvt//MARINE_PARAMETERIZATION/FOURTH_TRY/INP_marine_alltemps.npy')#m3
from pprint import pprint
plt.figure()

#INP=INP_feldspar_alltemps_daily*1e6+INP_marine_alltemps_daily

temps=np.linspace(-37,0,38)
temps=temps[::-1]
#INP_range=INP[:,25:26,46:57,0:5,:100]
#INP_range=INP[:,25:26,46:57,0:1,:100]


#plt.plot(temps,GLO_low(temps),'k--')
plt.plot(temps,max_INP,'ko')
plt.plot(temps,min_INP,'ko')
plt.plot(temps,mean_INP,'ko')
#plt.plot(temps,INP_range.max(axis=(1,2,3,4)),'ko')
#plt.plot(temps,INP_range.max(axis=(1,2,3,4)),'ko')
#plt.plot(temps,INP_range.max(axis=(1,2,3,4)),'ko')
#plt.plot(temps,np.exp(np.log(INP_range).mean(axis=(1,2,3,4))),'ko')
#plt.plot(temps,INP_range.min(axis=(1,2,3,4)),'ko')
#plt.plot(temps,INP_range.min(),'ko')
#plt.plot(temps,INP_range.max(),'ko')
plt.plot(temps,GLO_low(temps),'k--')
plt.plot(temps,GLO_mean(temps),'k--')
plt.plot(temps,GLO_high(temps),'k--')
plt.yscale('log')

#INP_range.min(axis=(1,2,3,4)).tolist()

#%%

#land_boolean=np.ones(x1.budgets_mm[0,30,:,:,:].mean(axis=-1).shape)
#land_boolean[x1.budgets_mm[0,30,:,:,:].mean(axis=-1)>0]=0
#jl.plot(land_boolean)
#
#
#np.save('/nfs/a201/eejvt/land_boolean.npy',land_boolean)
#
#land_boolean_nohighlats=np.copy(land_boolean)
#land_boolean_nohighlats[55:,:]=0
#land_boolean_nohighlats[:6,:]=0
#jl.plot(land_boolean_nohighlats)
#np.save('/nfs/a201/eejvt/land_boolean_nohighlats.npy',land_boolean_nohighlats)
land_boolean_nohighlats=np.load('/nfs/a201/eejvt/land_boolean_nohighlats.npy')
#jl.plot(land_boolean_nohighlats)




level=25
levelmax=30

level=20
levelmax=25
t=20
INP_total=INP_feldspar_alltemps_daily[t,level:levelmax,]*1e6+INP_marine_alltemps_daily[t,level:levelmax,]
INP_total=INP_total*1e-3

bins=np.linspace(-5,1,30)
bins=np.linspace(-5,3,30)
#bins_tick=np.linspace(-6,8,18)
bins_tick=np.linspace(-6,8,15)
bins_tick=np.linspace(-5,1,7)
bins_tick=np.linspace(-5,3,9)
a=[]
b=[]
INP_total_sea=np.copy(INP_total)
for i in range(INP_total.shape[0]):
    print i
    for j in range(INP_total.shape[-1]):
        for ilat in range(INP_total.shape[1]):
            for ilon in range(INP_total.shape[2]):
                if land_boolean_nohighlats[ilat,ilon]:
                    a.append(INP_total[i,ilat,ilon,j])
                    INP_total_sea[i,ilat,ilon,j]=1e-99
#b=INP_total[]
plt.figure()
#
#lon=-45

maxlat=75
minlat=45
ilatmxn=jl.find_nearest_vector_index(jl.lat,maxlat)
ilatminn=jl.find_nearest_vector_index(jl.lat,minlat)
ilatmxs=jl.find_nearest_vector_index(jl.lat,-maxlat)
ilatmins=jl.find_nearest_vector_index(jl.lat,-minlat)
lon=-160
lon_pacific=-160
ilon=jl.find_nearest_vector_index(jl.lon180,lon)
ilon_pacific=jl.find_nearest_vector_index(jl.lon180,lon_pacific)

print levelmax,  10**(np.log10(INP_total[:,ilatmxn:ilatminn,ilon,:].flatten()).mean()-np.log10(INP_total[:,ilatmins:ilatmxs,ilon,:].flatten()).mean())



#%%

#
#alpha=0.5
#plt.figure()
##land_INP=INP_total[i,land_boolean_nohighlats.astype(int),j].flatten()
##plt.hist(np.log10(INP_total.flatten()),bins,color='green',normed=1,label='all')
##plt.hist(np.log10(a),bins,color='silver',normed=1,alpha=0.5,label='Polar')#44:60
#plt.hist(np.log10(a),bins,color='green',normed=1,alpha=alpha,label='75$^o$N-75$^o$S Land')#44:60
#
##plt.hist(np.log10(INP_total_sea[:,ilatmins:ilatmxs,:,:].flatten()),bins,color='blue',normed=1,alpha=alpha,label='40-70$^o$S %i$^o$W'%(-lon))#44:60
#plt.hist(np.log10(INP_total[:,ilatmins:ilatmxs,ilon,:].flatten()),bins,color='blue',normed=1,alpha=alpha,label='40-70$^o$S %i$^o$W'%(-lon))#44:60
##plt.hist(np.log10(INP_total[46:57,:,:].flatten()),bins,color='blue',normed=1,alpha=0.5,label='40-70S')
##plt.hist(np.log10(INP_total[:32,:,:].flatten()),bins,color='brown',normed=1,alpha=0.5,label='north')
##plt.hist(np.log10(INP_total[32:,:,:].flatten()),bins,color='blue',normed=1,alpha=0.5,label='south')
##plt.hist(np.log10(INP_total[57:,:,:].flatten()),bins,color='white',normed=1,alpha=0.5)
#
##plt.hist(np.log10(INP_total_sea[:,ilatmxn:ilatminn,:,:].flatten()),bins,color='r',normed=1,alpha=alpha,label='40-70$^o$N %i$^o$W'%(-lon))#4:19 35-75
#plt.hist(np.log10(INP_total[:,ilatmxn:ilatminn,ilon,:].flatten()),bins,color='r',normed=1,alpha=alpha,label='40-70$^o$N %i$^o$W'%(-lon))#4:19 35-75
##plt.hist(np.log10(INP_total[:,ilatmxn:ilatminn,ilon_pacific,:].flatten()),bins,color='orange',normed=1,alpha=alpha,label='40-70$^o$N %i$^o$W'%(-lon_pacific))#4:19 35-75
##plt.hist(np.log10(INP_total[:,6:17,64,:].flatten()),bins,color='r',normed=1,alpha=0.5,label='40-70$^o$N 180$^o$W')#4:19 35-75
#
#plt.axvline(np.log10(GLO_low(-t)*1e-3),lw=1,ls='--',color='k',label='SO range')
#plt.axvline(np.log10(GLO_high(-t)*1e-3),lw=1,ls='--',color='k')
#plt.axvline(np.log10(INP_total[:,ilatmins:ilatmxs,ilon,:].flatten()).mean(),lw=3,color='b')#,label='Mean 40-70$^oS 30$^o$W')
#plt.axvline(np.log10(INP_total[:,ilatmxn:ilatminn,ilon,:].flatten()).mean(),lw=3,color='r')#,label='Mean 40-70$^oN 30$^o$W')
#plt.axvline(np.log10(a).mean(),lw=3,color='g')#,label='Land')
#plt.legend()
#plt.title('$[INP]_{-20^oC}$ frecuency 850-600hpa')
#plt.xticks(bins_tick,['$10^{%i}$'%i for i in bins_tick])
#plt.ylabel('Normalized frecuency')
#plt.xlabel('$[INP]_{-20^oC}$   $L^{-1}$')
##plt.yscale('log')
#plt.savefig(sav_fol+'INP_histogram.png')
#%%
alpha=0.6
plt.figure()
#land_INP=INP_total[i,land_boolean_nohighlats.astype(int),j].flatten()
#plt.hist(np.log10(INP_total.flatten()),bins,color='green',normed=1,label='all')
#plt.hist(np.log10(a),bins,color='silver',normed=1,alpha=0.5,label='Polar')#44:60
plt.hist(np.log10(a),bins,color='green',normed=1,alpha=alpha,label='75$^o$N-75$^o$S Land')#44:60

plt.hist(np.log10(INP_total_sea[:,ilatmins:ilatmxs,:,:].flatten()),bins,color='blue',normed=1,alpha=alpha,label='40-70$^o$S Ocean')#44:60
#plt.hist(np.log10(INP_total_sea[:,ilatmins:ilatmxs,ilon,:].flatten()),bins,color='blue',normed=1,alpha=alpha,label='40-70$^o$S %i$^o$W'%(-lon))#44:60
#plt.hist(np.log10(INP_total[46:57,:,:].flatten()),bins,color='blue',normed=1,alpha=0.5,label='40-70S')
#plt.hist(np.log10(INP_total[:32,:,:].flatten()),bins,color='brown',normed=1,alpha=0.5,label='north')
#plt.hist(np.log10(INP_total[32:,:,:].flatten()),bins,color='blue',normed=1,alpha=0.5,label='south')
#plt.hist(np.log10(INP_total[57:,:,:].flatten()),bins,color='white',normed=1,alpha=0.5)

plt.hist(np.log10(INP_total_sea[:,ilatmxn:ilatminn,:,:].flatten()),bins,color='r',normed=1,alpha=alpha,label='40-70$^o$N Ocean')#4:19 35-75
#plt.hist(np.log10(INP_total_sea[:,ilatmxn:ilatminn,ilon,:].flatten()),bins,color='r',normed=1,alpha=alpha,label='40-70$^o$N Ocean')#4:19 35-75
#plt.hist(np.log10(INP_total[:,ilatmxn:ilatminn,ilon_pacific,:].flatten()),bins,color='orange',normed=1,alpha=alpha,label='40-70$^o$N %i$^o$W'%(-lon_pacific))#4:19 35-75
#plt.hist(np.log10(INP_total[:,6:17,64,:].flatten()),bins,color='r',normed=1,alpha=0.5,label='40-70$^o$N 180$^o$W')#4:19 35-75

plt.axvline(np.log10(GLO_low(-t)*1e-3),lw=1,ls='--',color='k',label='SO range')
plt.axvline(np.log10(GLO_high(-t)*1e-3),lw=1,ls='--',color='k')

so_mean=INP_total_sea[:,ilatmins:ilatmxs,:,:].flatten()
so_mean=so_mean[so_mean>1e-90]
plt.axvline(np.log10(so_mean).mean(),lw=3,color='b')#,label='Mean 40-70$^oS 30$^o$W')
no_mean=INP_total_sea[:,ilatmxn:ilatminn,:,:].flatten()
no_mean=no_mean[no_mean>1e-90]
plt.axvline(np.log10(no_mean).mean(),lw=3,color='r')#,label='Mean 40-70$^oN 30$^o$W')
plt.axvline(np.log10(a).mean(),lw=3,color='g')#,label='Land')
plt.legend()
plt.title('b) $\mathrm{[INP]_{-20^oC}}$ frequency')
plt.xticks(bins_tick,['$10^{%i}$'%i for i in bins_tick])
plt.ylabel('Normalized frequency')
plt.xlabel('$\mathrm{[INP]_{-20^oC}}$   $\mathrm{(L^{-1})}$')
#plt.yscale('log')
plt.savefig(sav_fol+'INP_histogram.png')
plt.savefig(sav_fol+'INP_histogram.eps')

#
#plt.figure()
#plt.plot()

#%%

'''
level=20
levelmax=26

t=20
INP_total=INP_feldspar_alltemps_daily[t,level:levelmax,]*1e6+INP_marine_alltemps_daily[t,level:levelmax,]
INP_total=INP_total*1e-3

bins=np.linspace(0,6,30)
bins=np.linspace(-5,4,30)
#bins_tick=np.linspace(-6,8,18)
bins_tick=np.linspace(-6,8,15)
bins_tick=np.linspace(-5,4,10)
a=[]

for i in range(INP_total.shape[0]):
    print i
    for j in range(INP_total.shape[-1]):
        for ilat in range(INP_total.shape[1]):
            for ilon in range(INP_total.shape[2]):
                if land_boolean_nohighlats[ilat,ilon]:
                    a.append(INP_total[i,ilat,ilon,j])

#b=INP_total[]
plt.figure()
#
#land_INP=INP_total[i,land_boolean_nohighlats.astype(int),j].flatten()
#plt.hist(np.log10(INP_total.flatten()),bins,color='green',normed=1,label='all')
#plt.hist(np.log10(a),bins,color='silver',normed=1,alpha=0.5,label='Polar')#44:60
plt.hist(np.log10(a),bins,color='green',normed=1,alpha=0.5,label='75$^o$N-75$^o$S Land')#44:60
plt.hist(np.log10(INP_total[:,46:57,:,:].flatten()),bins,color='blue',normed=1,alpha=0.5,label='40-70$^o$S 30$^o$W')#44:60
#plt.hist(np.log10(INP_total[46:57,:,:].flatten()),bins,color='blue',normed=1,alpha=0.5,label='40-70S')
#plt.hist(np.log10(INP_total[:32,:,:].flatten()),bins,color='brown',normed=1,alpha=0.5,label='north')
#plt.hist(np.log10(INP_total[32:,:,:].flatten()),bins,color='blue',normed=1,alpha=0.5,label='south')
#plt.hist(np.log10(INP_total[57:,:,:].flatten()),bins,color='white',normed=1,alpha=0.5)
plt.hist(np.log10(INP_total[:,6:17,:,:].flatten()),bins,color='r',normed=1,alpha=0.5,label='40-70$^o$N 30$^o$W')#4:19 35-75

plt.axvline(np.log10(GLO_low(-t)*1e-3),lw=1,ls='--',color='k',label='SO range')
#plt.axvline(np.log10(GLO_high(-t)*1e-3),lw=1,ls='--',color='k')
#plt.axvline(np.log10(INP_total[:,46:57,:,:].flatten()).mean(),lw=3,color='b')#,label='Mean 40-70$^oS 30$^o$W')
#plt.axvline(np.log10(INP_total[:,6:17,:,:].flatten()).mean(),lw=3,color='r')#,label='Mean 40-70$^oN 30$^o$W')
plt.axvline(np.log10(a).mean(),lw=3,color='g')#,label='Land')
plt.legend()
plt.title('$[INP]_{-20^oC}$ North and South Atlantic 850-600hpa')
plt.xticks(bins_tick,['$10^{%i}$'%i for i in bins_tick],fontsize=15)
plt.ylabel('Normalized frecuency')
plt.xlabel('$[INP]_{-20^oC}$   $L^{-1}$',fontsize=15)
#plt.yscale('log')
plt.savefig(sav_fol+'INP_histogram_20.png')
'''