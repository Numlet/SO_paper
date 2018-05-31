#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:19:16 2017

@author: eejvt
"""

from base_imports import *
CTT_map=OrderedDict()
CTT_map_flatten=OrderedDict()

from CTT_satellite import CTT_satellite_dict


for i in range(100):
    plt.close()

#rcParams['legend.frameon'] = 'False'
CTT_bins=np.linspace(200,275,25)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','brown','k','grey','silver']
list_clouds=['C1','C2','C3']

for cloud in list_clouds:
    icol=0
    plt.figure()
    plt.title(cloud)
    mask=np.zeros((300,300))
    
    for param in list_params:
        key=cloud+'_'+param
        print key
        lw=2
        ls='-'
        if 'SATELLITE' in key:
            CTT_map[key]=stc.clean_cube(CTT_satellite_dict[key])
            lw=4
            ls='--'
            
            bins,pdf=PDF(CTT_map[key][~np.isnan(CTT_map[key])],CTT_bins)
            pdf_SATELLITEELLITEELLITE=np.copy(pdf)
        else:
            if 'C3' in key:
                itime=13
            if key=='C3_DM10':
                itime=12
            if 'C1' in key:
                itime=16
            if 'C2' in key:
                itime=17
#                    print key
            if 'GLOBAL' in key:
        #        if 'C2' in key:
        #            continue
                sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
#                cube_CTT=iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0][itime,:,:]
                cube_CTT=iris.load(ukl.Obtain_name(run_path[key]+'L1/','CTT'))[0][itime,:,:]
#                cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
        #        cube = cube.regrid(sample_cube, iris.analysis.Linear())
                cube_CTT= cube_CTT.regrid(sample_cube, iris.analysis.Linear())
#                cube_SW = cube_SW.regrid(sample_cube, iris.analysis.Linear())
            else:
                cube_CTT=stc.clean_cube(iris.load(run_path[key]+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
#                cube_LWP=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'L1/','LWP'))[0])[itime,:,:]
#                cube_SW=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0])[itime,:,:]

            CTT_map[key]=cube_CTT.data
            bins,pdf=PDF(CTT_map[key][~np.isnan(CTT_map[key])],CTT_bins)



        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
        plt.xlabel('Cloud top Temperature K')
        plt.ylabel('Normalized frecuecy')
        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
        plt.legend(loc='best',fontsize=12)
        plt.savefig(sav_fol+'PDF_CTT_'+cloud+'.png')





        print param, key,cloud
        print CTT_map[key].shape
        print np.isnan(CTT_map[key]).sum()/float(CTT_map[key].size)
        print CTT_map[key].max(),CTT_map[key].max()
        mask=mask+np.isnan(CTT_map[key])
        print np.array([mask>1]).sum()/float(CTT_map[key].size)
    for param in list_params:
        key=cloud+'_'+param

        CTT_map_flatten[key]=CTT_map[key][mask==0].flatten()
        print key
        print CTT_map_flatten[key].shape
        print np.corrcoef(CTT_map_flatten[cloud+'_'+'SATELLITE'],CTT_map_flatten[key])
        print np.std(CTT_map_flatten[key])
#            CTT_map[key]=jl.congrid(np.load(pspc_fol+'CTT_distribution_'+key+'.npy'),(30,30))
#            bins,pdf=PDF(CTT_map[key][~np.isnan(CTT_map[key])],CTT_bins)
#        r=np.corrcoef(pdf,pdf_SATELLITEELLITEELLITE)[0,1]
#        plt.xlabel('Reflected CTT radiation $W/m^2$')
#        plt.ylabel('Normalized frecuecy')
#        plt.plot(bins,pdf,label=key+' R=%1.2f'%r,c=list_colors[icol],lw=lw,ls=ls)
        icol=icol+1
#    plt.legend(loc='best',fontsize=12)
#    plt.savefig(sav_fol+'PDF_CTT_'+cloud+'.png')










