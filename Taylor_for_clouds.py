#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:55:51 2017

@author: eejvt
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:35:26 2017

@author: eejvt
"""

from base_imports import *
import taylor_diagram_copin as td


SW_map=OrderedDict()
LWP_map=OrderedDict()

from SW_satellite import SW_satellite_dict
from LWP_satellite import LWP_satellite_dict
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
list_colors=['b','y','r','green','brown','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    fig=plt.figure()
#    plt.title(cloud+' SW ')
    ax1 = fig.add_subplot(1,2,1, xlabel='X', ylabel='Y')
#    ax2 = dia.setup_axes(fig, 122)



#    ax=plt.subplot(1,1,1)
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
            pdf_SATELLITE=np.copy(pdf)
            dia = td.TaylorDiagram(pdf)
            ax = dia.setup_axes(fig, 122)
            ax1.plot(bins,pdf,'k-', label='Data')
        else:
            SW_map[key]=np.load(pspc_fol+'SW_distribution_filtered_'+key+'.npy')
#            SW_map[key]=jl.congrid(np.load(pspc_fol+'SW_distribution_'+key+'.npy'),(30,30))
            bins,pdf=PDF(SW_map[key][~np.isnan(SW_map[key])],SW_bins)
#            dia.plot_sample(pdf_SATELLITE+0.005*np.random.rand(len(pdf)),'bo')#, color=list_colors[icol],label=param)
            ax1.plot(bins,pdf,'-',color=list_colors[icol], label='Model 1')
            dia.plot_sample(pdf)
#        r=np.corrcoef(pdf,pdf_SATELLITE)[0,1]
#        plt.xlabel('Reflected SW radiation $W/m^2$')
#        plt.ylabel('Normalized frecuecy')
#        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
    plt.show()
#    plt.legend(loc='best',fontsize=12)
#    plt.savefig(sav_fol+'PDF_SW_'+cloud+'.png')
#    LWP_map[key]=np.load(pspc_fol+'LWP_distribution_'+key+'.npy')
#%%
for i in range(100):
    plt.close()
