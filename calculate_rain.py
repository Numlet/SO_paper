#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:53:46 2017

@author: eejvt
"""

from base_imports import *

def save_cube(cube):
    """
    Saves cube as a netCDF file.
    """
    saving_name=saving_folder_l1+'L1_'+cube._var_name+'_'+cube.long_name+'.nc'
    iris.save(cube,saving_name, netcdf_format="NETCDF4")
    print 'saved:',cube.long_name

for run in run_path:
    print run_path[run]
    path=run_path[run]
    folder=path+'All_time_steps/'
    density=iris.load_cube(path+'L1/'+'L1_air_density_Density of air.nc')
    rain_mmr=iris.load_cube(path+'All_time_steps/'+'All_time_steps_m01s00i272_RAIN_AFTER_TIMESTEP_________________.nc')
#    rain_concentration=rain_mmr*density
    height_cube=density.copy()
    saving_folder_l1=path+'L1/'
    height=np.ones(density.shape[1:])
    try:
        height_1d=rain_mmr.coord('atmosphere_hybrid_height_coordinate').points
        length_gridbox_cube=rain_mmr[0].copy()
        length_gridbox_cube.units=rain_mmr.coord('atmosphere_hybrid_height_coordinate').units
    except:
        h=iris.load(ukl.Obtain_name(path+'All_time_steps/','m01s15i101'))[0]
        length_gridbox_cube=rain_mmr[0].copy()
        length_gridbox_cube.units=h.units
        height_1d=h.data.mean(axis=(1,2))
        
    for i in range(height.shape[0]):
        height[i,]=height[i,]*height_1d[i]
    
        height_cube_data=height_cube.data
    for i in range(height_cube.shape[0]):
        
        height_cube_data[i,]=height
        print 'height calculated from potential_temperature cube'
        height_cube.data=height_cube_data
    try:
        height_cube.units=rain_mmr.coord('atmosphere_hybrid_height_coordinate').units
    except:
        height_cube.units=h.units
            
            
    base=np.zeros(height.shape[1:])
    length_gridbox=np.zeros(height.shape)
    #length_gridbox.data=np.zeros(length_gridbox.data.shape)
    
    for i in range(height.shape[0]):
        if i==0:
            length_gridbox[0,]=height[0,]
        else:
            length_gridbox[i,]=height[i,]-height[i-1,]
            print height[i,0,0]
            print height[i-1,0,0]
            print '---'
            print height[i,0,0]-height[i-1,0,0]
            print '---'
    
    length_gridbox_cube.data=length_gridbox
    length_gridbox_cube.remove_coord('forecast_reference_time')
    length_gridbox_cube.remove_coord('forecast_period')
    #length_gridbox_cube.remove_coord('time')
    
    #length_gridbox_cube=iris.coords.AuxCoord(length_gridbox,
    #                          long_name='length_gridbox',
    #                          units='meter^1')#J/(kg·K)
    
    rain_mc=density*rain_mmr
    rain_mc.long_name='Mass_concentration_of_rain'
    rain_mc._var_name='mcon_rain'
    save_cube(rain_mc)
    RWP_column=np.empty(rain_mc.data.shape[0]).tolist()
    
    for i in range(rain_mc.data.shape[0]):
        RWP_column[i]=(rain_mc[i,]*length_gridbox_cube)
    
    RWP_cube_list=iris.cube.CubeList(RWP_column)
    RWP=RWP_cube_list.merge()[0]
    RWP=RWP.collapsed(['model_level_number'],iris.analysis.SUM)
    RWP._var_name='RWP'
    RWP.long_name='Rain_water_path'
    save_cube(RWP)
    



jl.send_email()