#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:35:26 2017

@author: eejvt
"""

from base_imports import *



SW_map=OrderedDict()
LWP_map=OrderedDict()
LW_map=OrderedDict()
CTT_map=OrderedDict()
CDNC_map=OrderedDict()

from SW_satellite import SW_satellite_dict
from LWP_satellite import LWP_satellite_dict
from LW_satellite import LW_satellite_dict
from CTT_satellite import CTT_satellite_dict
#from CDNC_satellite import CDNC_satellite_dict
for i in range(100):
    plt.close()
def PDF(data,nbins=100):
    min_val=data.min()
    max_val=data.max()
    if isinstance(nbins,np.ndarray):
        bins=nbins
        data=data.flatten()
        data=data[data>bins[0]]
        data=data[data<bins[-1]]
    else:
        bins=np.linspace(min_val,max_val,nbins)
    size_bin=bins[1:]-bins[:-1]
    bins_midpoint=(bins[1:]-bins[:-1])/2.+bins[1:]
    number_ocurrencies=np.zeros_like(bins_midpoint)
    for ibin in range(len(number_ocurrencies)):
        larger=[data>bins[ibin]]
        smaller=[data<bins[ibin+1]]
        
        number_ocurrencies[ibin]=np.sum(np.logical_and(larger,smaller))
        
    normalized_pdf=number_ocurrencies/float(len(data))/size_bin
    return bins_midpoint,normalized_pdf
import matplotlib as mpl
mpl.rcParams['legend.frameon'] = 'False'
#rcParams['legend.frameon'] = 'False'
#%%
SW_bins=np.linspace(0,900, 19*2)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(cloud)

    for param in list_params:
        key=cloud+'_'+param
        
        print key
        lw=2
        ls='-'
        if 'SATELLITE' in key:
            SW_map[key]=SW_satellite_dict[key]
            lw=4
            ls='--'
            
            bins,pdf=PDF(SW_map[key][~np.isnan(SW_map[key])],SW_bins)
            pdf_SATELLITEELLITEELLITE=np.copy(pdf)
        else:
            SW_map[key]=np.load(pspc_fol+'SW_distribution_filtered_'+key+'.npy')
#            SW_map[key]=jl.congrid(np.load(pspc_fol+'SW_distribution_'+key+'.npy'),(30,30))
            bins,pdf=PDF(SW_map[key][~np.isnan(SW_map[key])],SW_bins)
        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
        plt.xlabel('Reflected SW radiation $\mathrm{(W/m^2)}$')
        plt.ylabel('Normalized frecuency')
        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
    plt.legend(loc='best',fontsize=12)
    plt.savefig(sav_fol+'PDF_SW_'+cloud+'.png')
    plt.savefig(sav_fol+'PDF_SW_'+cloud+'.eps')
#    LWP_map[key]=np.load(pspc_fol+'LWP_distribution_'+key+'.npy')
#%%

LWP_bins=np.linspace(0,0.55, 19*9)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(cloud)

    for param in list_params:
        
        key=cloud+'_'+param
        
        print key
        lw=2
        ls='-'
        if 'SATELLITE' in key:
            LWP_map[key]=LWP_satellite_dict[key]
            lw=7
            ls='--'
            
            bins,pdf=PDF(LWP_map[key][~np.isnan(LWP_map[key])],LWP_bins)
            pdf_SATELLITEELLITEELLITE=np.copy(pdf)
        else:
            LWP_map[key]=np.load(pspc_fol+'LWP_distribution_filtered_'+key+'.npy')
#            SW_map[key]=jl.congrid(np.load(pspc_fol+'SW_distribution_'+key+'.npy'),(30,30))
            bins,pdf=PDF(LWP_map[key][~np.isnan(LWP_map[key])],LWP_bins)
        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
        plt.xlabel('Liquid Water Path (mm)')
        plt.ylabel('Normalized frecuency')
        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
    plt.legend(loc='best',fontsize=12)
    plt.savefig(sav_fol+'PDF_LWP_'+cloud+'.png')
    plt.savefig(sav_fol+'PDF_LWP_'+cloud+'.eps')
#%%
LWP_bins=np.linspace(0.0,0.55, 19*1)
LWP_bins=np.logspace(-4,0, 20)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(cloud)

    for param in list_params:
        
        key=cloud+'_'+param
        
        print key
        lw=2
        ls='-'
        if 'SATELLITE' in key:
            LWP_map[key]=LWP_satellite_dict[key]
            lw=7
            ls='--'
            
            bins,pdf=PDF(LWP_map[key][~np.isnan(LWP_map[key])],LWP_bins)
            pdf_SATELLITEELLITEELLITE=np.copy(pdf)
        else:
            LWP_map[key]=np.load(pspc_fol+'LWP_distribution_filtered_'+key+'.npy')
#            SW_map[key]=jl.congrid(np.load(pspc_fol+'SW_distribution_'+key+'.npy'),(30,30))
            data=LWP_map[key]
            data[np.isnan(data)]=0
            data_con=jl.congrid(data,(30,30))
            data_con[data_con==0]=np.nan
            data_con=data_con[~np.isnan(data_con)].flatten()
            bins,pdf=PDF(data_con,LWP_bins)
            
            
            data=LWP_map[key]
            data[np.isnan(data)]=0
            data[np.isnan(data)]=0
            bins,pdf=PDF(data,LWP_bins)
#            bins,pdf=PDF(LWP_map[key][~np.isnan(LWP_map[key])],LWP_bins)
        pdf_log=np.log(pdf)
        pdf_sat_log=np.log(pdf_SATELLITEELLITEELLITE)
        valids=[(pdf_log>-9999) & (pdf_sat_log>-9999)]
        pdf_log=pdf_log[valids]
        pdf_sat_log=pdf_sat_log[valids]
        r=np.corrcoef(pdf_log,pdf_sat_log)[0,1]
        if r==np.nan: break
        plt.xlabel('Liquid Water Path (mm)')
        plt.ylabel('Normalized frecuency')
        plt.yscale('log')
        plt.xscale('log')
        plt.xlim(2e-3,1e1)
        plt.ylim(0.01,100)
        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
    plt.legend(loc='upper right',fontsize=12)
    plt.savefig(sav_fol+'PDF_LWP_log_coarse_all_'+cloud+'.png')
    plt.savefig(sav_fol+'PDF_LWP_log_coarse_all_'+cloud+'.eps')
#%%
LW_bins=np.linspace(0,0.25, 19*7)
LW_bins=np.linspace(175,260, 19*3)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(cloud)

    for param in list_params:
        key=cloud+'_'+param
        
        print key
        lw=2
        ls='-'
        if 'SATELLITE' in key:
            LW_map[key]=LW_satellite_dict[key]
            lw=5
            ls='--'
            
            bins,pdf=PDF(LW_map[key][~np.isnan(LW_map[key])],LW_bins)
            pdf_SATELLITEELLITEELLITE=np.copy(pdf)
        else:
            LW_map[key]=np.load(pspc_fol+'LW_distribution_filtered_'+key+'.npy')
#            SW_map[key]=jl.congrid(np.load(pspc_fol+'SW_distribution_'+key+'.npy'),(30,30))
            bins,pdf=PDF(LW_map[key][~np.isnan(LW_map[key])],LW_bins)
        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
        plt.xlabel('LW')
        plt.ylabel('Normalized frecuency')
        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
    plt.legend(loc='best',fontsize=12)
    plt.savefig(sav_fol+'PDF_LW_'+cloud+'.png')
    plt.savefig(sav_fol+'PDF_LW_'+cloud+'.eps')

#%%
CTT_bins=np.linspace(0,0.25, 19*7)
CTT_bins=np.linspace(240,275, 19*4)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(cloud)

    for param in list_params:
        key=cloud+'_'+param
        
        print key
        lw=2
        ls='-'
        if 'SATELLITE' in key:
            CTT_map[key]=CTT_satellite_dict[key]
            lw=5
            ls='--'
            
            bins,pdf=PDF(CTT_map[key][~np.isnan(CTT_map[key])],CTT_bins)
            pdf_SATELLITEELLITEELLITE=np.copy(pdf)
        else:
            CTT_map[key]=np.load(pspc_fol+'CTT_distribution_filtered_'+key+'.npy')
#            SW_map[key]=jl.congrid(np.load(pspc_fol+'SW_distribution_'+key+'.npy'),(30,30))
            bins,pdf=PDF(CTT_map[key][~np.isnan(CTT_map[key])],CTT_bins)
        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
        plt.xlabel('Cloud Top Temperature $\mathrm{(^{o}K)}$')
        plt.ylabel('Normalized frecuency')
        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
    plt.legend(loc='best',fontsize=12)
    plt.savefig(sav_fol+'PDF_CTT_'+cloud+'.png')
    plt.savefig(sav_fol+'PDF_CTT_'+cloud+'.eps')


#%%

CDNC_bins=np.linspace(0,0.25, 19*7)
CDNC_bins=np.linspace(0,150, 19*4)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_params=['SATELLITE','M92','DM10','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(cloud)

    for param in list_params:
        key=cloud+'_'+param
        
        print key
        lw=2
        ls='-'
        if 'SATELLITE' in key:
            CDNC_map[key]=CDNC_satellite_dict[key]
            lw=5
            ls='--'
            
            bins,pdf=PDF(CDNC_map[key][~np.isnan(CDNC_map[key])],CDNC_bins)
            pdf_SATELLITEELLITEELLITE=np.copy(pdf)
        else:
            CDNC_map[key]=np.load(pspc_fol+'CDNC_distribution_filtered_'+key+'.npy')*1e-6
#            SW_map[key]=jl.congrid(np.load(pspc_fol+'SW_distribution_'+key+'.npy'),(30,30))
            bins,pdf=PDF(CDNC_map[key][~np.isnan(CDNC_map[key])],CDNC_bins)
        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
        plt.xlabel('CDNC')
        plt.ylabel('Normalized frecuency')
        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
    plt.legend(loc='best',fontsize=12)
    plt.savefig(sav_fol+'PDF_CDNC_'+cloud+'.png')
    plt.savefig(sav_fol+'PDF_CDNC_'+cloud+'.eps')
#%%
#for i in range(100):
#    plt.close()
#

plt.figure()
plt.imshow(LWP_map[key])
plt.colorbar()

plt.plot(LWP_map[key].flatten(),CDNC_map[key].flatten(),'bo')



