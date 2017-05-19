#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:05:05 2017

@author: eejvt
"""

from base_imports import *




sim_path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/'
sub_folder='L1/'
code='CINC'

cube_DM10 = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0])
#cube_GLO_HIGH = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/GLO_HIGH/'+sub_folder,code))[0])
cube_GLO_MEAN = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/GLO_MEAN/'+sub_folder,code))[0])
cube_GLO_MIN = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/GLO_MIN/'+sub_folder,code))[0])
cube_GP_HAM_DMDUST = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/GP_HAM_DMDUST/'+sub_folder,code))[0])
cube_MEYERS = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/MEYERS/'+sub_folder,code))[0])


cube_global= iris.load(ukl.Obtain_name(sim_path+'/GLOBAL/'+sub_folder,code))[0]

cube_global = cube_global.regrid(cube_DM10, iris.analysis.Linear())



runs_dict=OrderedDict()
#runs_dict['Satellite']=grid_z1
runs_dict['GLOBAL']=cube_global[it].data
runs_dict['MEYERS']=cube_MEYERS[it].data
runs_dict['DM10']=cube_DM10[it].data
runs_dict['GLO_HIGH']=cube_GLO_HIGH[it].data
#runs_dict['MEYERS (CS)']=cube_csbm[13].data
#runs_dict['MEYERS']=cube_m[13].data
#runs_dict['3_ORD_LESS']=cube_3ord[13].data
#runs_dict['2_ORD_LESS']=cube_2l[13].data
#runs_dict['2_ORD_MORE']=cube_2m[13].data
#runs_dict['OLD_MICRO']=cube_oldm[13].data
#runs_dict['GLOPROF']=cube_gloprof[13].data
runs_dict['GLO_MEAN']=cube_GLO_MEAN[it].data
runs_dict['GLO_MIN']=cube_GLO_MIN[it].data
runs_dict['GP_HAM_DMDUST']=cube_GP_HAM_DMDUST[it].data
         
levels=np.arange(0.00,0.6,0.05).tolist()
same_bins=np.linspace(0.00,0.6,100)
levels=np.linspace(cube_DM10[it].data.min(),cube_DM10[it].data.max(),15).tolist()
same_bins=np.linspace(cube_DM10[it].data.min(),cube_DM10[it].data.max(),150).tolist()

#levels=np.linspace(runs_dict['Satellite (AMSR2)'].min(),runs_dict['Satellite (AMSR2)'].max(),15)
stc.plot_map(runs_dict,levels,lat=X,lon=Y,variable_name='LWP mm')
stc.plot_PDF(runs_dict,same_bins,
             variable_name='LWP mm')
