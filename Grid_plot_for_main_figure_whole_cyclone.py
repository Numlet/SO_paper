#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 10:19:58 2017

@author: eejvt
"""

from base_imports import *
from SW_satellite import SW_satellite_dict
from LWP_satellite import LWP_satellite_dict
#%%
congrid=True
no_bounds=True
cut=50

plt.figure(figsize=(20,5))
#plt.figure()

list_params=['SATELLITE','GLOBAL','M92','VT17_MEAN']
list_colors=['b','y','r','grey']
list_clouds=['C1']

levels_sw=np.linspace(0,800,15).tolist()
levels_lwp=np.linspace(0,0.5,15).tolist()

ix=len(list_params)
iy=len(list_clouds)

clean_value=1
iplot=1
icloud=0
cmap=plt.cm.RdBu
levels_LWP=np.linspace(0,0.5,3).tolist()
#levels_LWP=[0.1,0.2,0.3,0.4,0.5]
levels_LWP=np.linspace(0,0.5,11).tolist()
#levels_LWP[0]=0.001
LWP_dict=OrderedDict()

for cloud in list_clouds:
    LWP_dict[cloud]=OrderedDict()
    print cloud
    iparam=0
    itime=cloud_it[cloud]
    for param in list_params:
        name=cloud+'_'+param
        print name
        cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path_wc[cloud+'_M92']+'L1/','LWP'))[0],clean_value)
        if param=='SATELLITE':
            continue
            LWP=LWP_satellite_dict[name]
            LWP=LWP[clean_value:,clean_value:]
            LWP=LWP[:-clean_value,:-clean_value]
            cube=cube_high_res.copy()
            cube.data[:,:,:]=np.nan
            cube.data[itime,:,:]=LWP
        elif param=='GLOBAL':
            cube=iris.load(ukl.Obtain_name(run_path_wc[name]+'L1/','LWP'))[0]
            cube = cube.regrid(cube_high_res, iris.analysis.Linear())
        else:
            cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path_wc[name]+'L1/','LWP'))[0],clean_value)
        model_lons,model_lats=stc.unrotated_grid(cube_high_res)
        print model_lats.max(),model_lats.min()
        X,Y=np.meshgrid(model_lons, model_lats)

        plt.subplot(iy,ix,iplot)
        plt.title(name)
        if param=='SATELLITE':plt.ylabel('Latitude')
        plt.xlabel('Longitude')
        CS=plt.contourf(X,Y,cube[itime,:,:].data,levels_LWP) 
        LWP_dict[cloud][name]=cube[itime,:,:].data
#        plt.clabel(CS, inline=1, fmt='%1.0f')
        plt.colorbar()
        iplot=iplot+1
plt.savefig(sav_fol+'Grid_main_figure_LWP.png')

#%%
from mpl_toolkits.axes_grid1 import make_axes_locatable
iplot=1
plt.figure(figsize=(20,5))
cmap=plt.cm.RdBu_r
#plt.figure()
levels_SW=np.linspace(0,750,15).tolist()
for cloud in list_clouds:
    print cloud
    iparam=0
    
    for param in list_params:
        name=cloud+'_'+param
        itime=cloud_it[cloud]
        
        print name
        
        if name=='C3_DM10':
            itime=11
        
        cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path_wc[cloud+'_M92']+'All_time_steps/','m01s01i208'))[0],clean_value)
        model_lons,model_lats=stc.unrotated_grid(cube_high_res)

        cube_high_res=cube_high_res[:,:,150:]
        model_lons=model_lons[150:]
        if param=='SATELLITE':
#            continue
            SW=SW_satellite_dict_wc[name]
            SW=SW[clean_value:,clean_value:]
            SW=SW[:-clean_value,:-clean_value]
            cube=cube_high_res.copy()
            cube.data[:,:,:]=np.nan
            cube.data[itime,:,:]=SW
        elif param=='GLOBAL':
            cube=iris.load(ukl.Obtain_name(run_path_wc[name]+'All_time_steps/','m01s01i208'))[0][:,:,150:]
            cube = cube.regrid(cube_high_res, iris.analysis.Linear())
        else:
            cube=stc.clean_cube(iris.load(ukl.Obtain_name(run_path_wc[name]+'All_time_steps/','m01s01i208'))[0],clean_value)[:,:,150:]
        X,Y=np.meshgrid(model_lons, model_lats)

        ax=plt.subplot(iy,ix,iplot)
        if param=='SATELLITE':plt.ylabel('Latitude')
        plt.xlabel('Longitude')

        plt.title(name)
        im=plt.contourf(X,Y,cube[itime,:,:].data,levels_SW,cmap=cmap) 
        if param==list_params[-1]:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)

            cb=plt.colorbar(im, cax=cax)
#            cb=plt.colorbar()
            cb.set_label('$W/m^2$')
        iplot=iplot+1
plt.savefig(sav_fol+'Grid_main_figure_SW.png')
plt.savefig(sav_fol+'Grid_main_figure_SW.eps')
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
#%%

plt.figure()
cmap=plt.cm.RdBu_r
clean_value=10

cube_high_res=stc.clean_cube(iris.load(ukl.Obtain_name(run_path_wc['C1'+'_M92']+'L1/','CTT'))[0],clean_value)
cube_surface_pressure=stc.clean_cube(iris.load(ukl.Obtain_name(run_path_wc['C1'+'_M92']+'All_time_steps/','pre'))[0],clean_value)[:,0,:,:]
cube_surface_temperature=stc.clean_cube(iris.load(ukl.Obtain_name(run_path_wc['C1'+'_M92']+'All_time_steps/','temp'))[0],clean_value)[:,0,:,:]

model_lons,model_lats=stc.unrotated_grid(cube_high_res)
X,Y=np.meshgrid(model_lons, model_lats)

xl=-200
yl=100
CS=plt.contourf(X[:xl,yl:],Y[:xl,yl:],cube_high_res[12,:xl,yl:].data,cmap=cmap)
plt.colorbar(label='K')

#C=plt.contour(X[:xl,yl:],Y[:xl,yl:],cube_surface_pressure[12,:xl,yl:].data*0.01,[950,960,970,980,990,1000,1010,1020,1030],colors='k')
#plt.clabel(C,fontsize=15,inline=1,fmt='%1.0f hpa')
C=plt.contour(X[:xl,yl:],Y[:xl,yl:],cube_surface_temperature[12,:xl,yl:].data,np.linspace(265,280,15).tolist(),colors='k')
plt.clabel(C,fontsize=15,inline=1,fmt='%1.0f k')
plt.title('Cloud Top temperature C1')
plt.text(-22.5,-64.5,'L',fontsize=30)
#plt.savefig(sav_fol+'CTT_for_thesis.png')



