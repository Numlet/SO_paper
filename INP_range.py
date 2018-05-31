#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:00:02 2017

@author: eejvt
"""

from base_imports import *


n05=56000*1e-6
n05_dust=56000*1e-6
n05_GLOMAP=21.26#cm-3 surface SO
n05_bug_meters=56000
lw=3
plt.figure()

temps=np.arange(-37,0,1)

marker='^'
marker_size=50
INP_obs_total=jl.read_INP_data("/nfs/see-fs-01_users/eejvt/PYTHON_CODE/INP_DATA/DM15.dat",header=1)
temps_obs=INP_obs_total[:,1]
concentrations=INP_obs_total[:,2]*1e3
lats=INP_obs_total[:,3]






plt.title('a) [INP] concentrations')
plt.xlabel('T $\mathrm{(^oC)}$')
plt.ylabel('[INP] $\mathrm{(L^{-1})}$')
plt.yscale('log')
#plt.grid()

temps=np.array(temps_for_INP)

plt.plot(temps,meyers_param(temps)*1e-3,'r',lw=lw,label='M92 Meyers et al. (1992)')

plt.plot(temps[:],demott_dust(temps,n05_dust)[:]*1e-3,'peru',lw=lw,label='DM15 DeMott et al. (2015)')
plt.plot(temps[:],demott(temps,n05_GLOMAP)[:]*1e-3,'green',lw=lw,label='DM10 DeMott et al. (2010)')

Gh=GLO_high(temps)*1e-3
Gl=GLO_low(temps)*1e-3
#
#Gh=np.array(max_INP)*1e-3
#Gl=np.array(min_INP)*1e-3
#
#for i in range(len(Gh)):
#    if Gh[-i]<Gh[-i-1]
plt.fill_between(temps[:],np.array(max_INP)*1e-3,Gl,label='GLOMAP range South Atlantic Vergara-Temprado et al. (2017)',alpha=0.08,color='blue')

plt.plot(temps[:],np.array(max_INP)*1e-3,'black',lw=lw,label='GLOMAP INP Highest (VT17_HIGH)')
plt.plot(temps[:],Gl,'silver',lw=lw,label='GLOMAP INP Lowest (VT17_LOW)')


#plt.plot(temps[:],np.array(mean_INP)*1e-3,'grey',lw=lw,ls='-',label='GLOMAP mean South Atlantic VT17')
plt.plot(temps[:],np.array(mean_INP)*1e-3,'grey',lw=lw,ls='-',label='GLOMAP INP Mean (VT17_MEAN)')
#plt.plot(temps[:],np.array(mean_INP)*1e-3,'k',lw=lw,ls='-.',label='GLOMAP mean South Atlantic VT17')

#plot=plt.scatter(temps_obs,concentrations,c='b',marker=marker,s=marker_size,label='Marine INP observations DeMott et al. (2016)')

#plt.annotate(s='', xy=(-10,1*1e-3), xytext=(-10,10*1e-3), arrowprops=dict(arrowstyle='<->'))
#plt.annotate(s='', xy=(-15,1*1e-3), xytext=(-15,100*1e-3), arrowprops=dict(arrowstyle='<->'),label='bigg73',color='y')
#plt.plot([-15,-15],[1*1e-3,100*1e-3],c='y',lw=3,label='SO INP range 50-60S Bigg (1973)')
#plt.annotate(s='', xy=(-15,10*1e-3), xytext=(-15,80*1e-3), arrowprops=dict(arrowstyle='<->'))

#plt.arrow(-15,1*1e-3, -15,100*1e-3, head_width=0.05, head_length=0.1, fc='k', ec='k')

data_terrestrial=np.genfromtxt('TERRESTRIAL_INFLUENCED.dat',delimiter="\t",skip_header=1)
data_marine=np.genfromtxt('MARINE_INFLUENCED.dat',delimiter="\t",skip_header=1)
INP_terrestrial=data_terrestrial[:,2]
temperature_terrestrial=data_terrestrial[:,1]
pressure_terrestrial=data_terrestrial[:,5]
latitude_terrestrial=data_terrestrial[:,3]
longitude_terrestrial=data_terrestrial[:,4]
INP_marine=data_marine[:,2]
temperature_marine=data_marine[:,1]
pressure_marine=data_marine[:,5]
latitude_marine=data_marine[:,3]
longitude_marine=data_marine[:,4]

#plt.close()
plt.scatter(temperature_terrestrial,INP_terrestrial*1e3,color='brown',label='Terrestrial INP observations',alpha=0.95)
plt.plot(temperature_marine,INP_marine*1e3,'b^',label='Marine INP observations',alpha=0.95)
mpl.rcParams['legend.frameon'] = 'False'



plt.legend(loc='lower left',prop={'size':10})
plt.xlim(-37,-1)
plt.ylim(1e-7,1e3)
plt.savefig(sav_fol+'INP_range.png')
plt.savefig(sav_fol+'INP_range.eps')
#
#for _ in range(200):
#    plt.close()