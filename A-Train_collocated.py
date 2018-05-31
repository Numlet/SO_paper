#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 09:19:58 2017

@author: eejvt
"""

from base_imports import *

run_path=OrderedDict()
run_path_collocated=OrderedDict()
run_path_wc=OrderedDict()

#run_path={}
#run_path['C3_GLOBAL']='/nfs/a201/eejvt/CASIM/SO_KALLI/GLOBAL/'
run_path['C3_M92']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/MEYERS_RIGHT_PROFILE/'#
#run_path['C3_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/DEMOTT_GLO_N05_HAMISHPROF/'#
#run_path['C3_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/'#
#run_path['C3_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/DM10_REPEAT/'#
run_path['C1_VT17_MEAN_HA']='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/VT17_MEAN_HIGH_AEROSOL/'#
run_path['C1_VT17_MEAN_lA']='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/VT17_MEAN_LOW_AEROSOL/'#
#run_path['C1_VT17_MEAN_LA']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLOMAP_PROFILE_DM/'#
#run_path['C3_VT17_HIGH']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLO_HIGH/'


try: 
    breaker = False #our mighty loop exiter!
    for key in run_path:
#        print key
        
        cloud=key[:2]
#        if not cloud=='C2':
#            continue
#        if not 'GLOBAL' in key:
#            continue
        print key
        L1=glob.glob(run_path[key]+'L1/*nc')
        all_time_steps=glob.glob(run_path[key]+'All_time_steps/*nc')
        ukl.create_folder(run_path[key]+'A_TRAIN_COLLOCATED')
        all_files=np.concatenate((L1,all_time_steps)).tolist()
#        all_files=L1
        for path_name in all_files:
            
    #        print path_name
            if 'L1' in path_name:
                file_name=path_name[len(run_path[key]+'L1/'):]
            else:
                file_name=path_name[len(run_path[key]+'All_time_steps/'):]
            print key, file_name
            cube=iris.load_cube(path_name)
    #       
            if 'time' in [coord.standard_name for coord in cube.coords()]:
                print len(cube.coord('time').points)
            #            if (len(cube.coord('time').points)>2) & (len(cube.coord('time').points)<12):
                if (len(cube.coord('time').points)>10):
                    hours=[time.hour for time in get_times_as_datetime(cube)]
            #            if hours!=np.arange(0,len(hours),dtype=int).tolist():
            #                 print 'EWRRORROEROERIIOHFOIEHRO--------------------------------'
            #                 print cube,key
            #                 breaker = True 
            #                 break
                    if cloud=='C1':
                        i16=int(jl.find_nearest_vector_index(hours,16))
                        i17=int(jl.find_nearest_vector_index(hours,17))
                        collocated_cube=(cube[i16,]+cube[i17,])/2.
                        print collocated_cube
                        saving_name=run_path[key]+'A_TRAIN_COLLOCATED/'+file_name[:-3]+'A-train_collocated.nc'
                        iris.save(collocated_cube,saving_name, netcdf_format="NETCDF4")
                    if cloud=='C2':
                        i16=int(jl.find_nearest_vector_index(hours,16))
                        i17=int(jl.find_nearest_vector_index(hours,17))
                        collocated_cube=(0.25*cube[i16,]+0.75*cube[i17,])
                        print collocated_cube
                        saving_name=run_path[key]+'A_TRAIN_COLLOCATED/'+file_name[:-3]+'A-train_collocated.nc'
                        iris.save(collocated_cube,saving_name, netcdf_format="NETCDF4")
                    if cloud=='C3':
            #                    collocated_cube=(0.25*cube[16,]+0.75*cube[17,])
            #                hours=[time.hour for time in get_times_as_datetime(cube)]
                        i13=int(jl.find_nearest_vector_index(hours,13))
                        i14=int(jl.find_nearest_vector_index(hours,14))
                        collocated_cube=(0.65*cube[i13,]+0.35*cube[i14,])
                        print collocated_cube
                        saving_name=run_path[key]+'A_TRAIN_COLLOCATED/'+file_name[:-3]+'A-train_collocated.nc'
                        iris.save(collocated_cube,saving_name, netcdf_format="NETCDF4")
            #                if hours[12]!=12:
            #                    print key
            #                    break
                        if hours[i13]!=13 or hours[i14]!=14:
                            print 'EWRRORROEROERIIOHFOIEHRO--------------------------------'
                            breaker = True 
            
            #                    print collocated_cube
            #                    saving_name=run_path[key]+'A_TRAIN_COLLOCATED/'+file_name[:-3]+'A-train_collocated.nc'
            #                    iris.save(collocated_cube,saving_name, netcdf_format="NETCDF4")
            #                break
        if breaker: # the interesting part!
            break   # <--- !            
#    except:continue
except:
    jl.send_error()


#jl.send_email()







#%%
#import traceback
#try:
#    
#    a=54
#    b='asdfasd'
#    print a/b
#except :
#    jl.send_error()


#
