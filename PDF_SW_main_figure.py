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
mpl.rcParams['legend.fontsize']= 25

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']
list_title=['c)','d)','e)']
PDFs={}
i=0
for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(list_title[i]+' '+cloud)

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
        PDFs[key]=pdf
        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
    plt.xlabel('Reflected SW radiation $\mathrm{(W/m^2)}$')
    plt.ylabel('Normalized frequency')
    plt.plot(bins,PDFs[cloud+'_SATELLITE'],label='SATELLITE',c='b',lw=lw*2,ls='--')
    plt.plot(bins,PDFs[cloud+'_GLOBAL'],label='GLOBAL MODEL',c='y',lw=lw,ls='-')
    plt.plot(bins,PDFs[cloud+'_M92'],label='M92',c='r',lw=lw,ls='-')
    three_PDF=np.zeros((len(PDFs[cloud+'_M92']),3))
    three_PDF[:,0]=PDFs[cloud+'_VT17_LOW']
    three_PDF[:,1]=PDFs[cloud+'_VT17_MEAN']
    three_PDF[:,2]=PDFs[cloud+'_VT17_HIGH']
    upp=three_PDF.max(axis=1)
    bot=three_PDF.min(axis=1)
    plt.fill_between(bins, upp,bot,alpha=0.5,color='grey',label='VT17 range')
#    plt.plot(bins,PDFs[cloud+'_SATELLITE'],label=key,c=list_colors[icol],lw=lw*2,ls='--')
    plt.legend(loc='best',fontsize=12)
    plt.savefig(sav_fol+'PDF_main_SW_'+cloud+'.png')
    plt.savefig(sav_fol+'PDF_main_SW_'+cloud+'.eps')
    i=i+1
#    LWP_map[key]=np.load(pspc_fol+'LWP_distribution_'+key+'.npy')
#%%

