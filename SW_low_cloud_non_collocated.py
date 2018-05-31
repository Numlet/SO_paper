"""
Created on Mon May  8 14:00:57 2017
@author: eejvt
"""

from base_imports import *
#cube_large=iris.load('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/LARGE_DOMAIN/All_time_steps/All_time_steps_m01s00i254_mass_fraction_of_cloud_liquid_water_in_air.nc')[0]
#cube_large=iris.load('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/LARGE_DOMAIN/All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0]
#cube_large_regrid=cube_large.regrid(cube, iris.analysis.Linear())
from SW_satellite import SW_satellite_dict
from CTT_satellite import CTT_satellite_dict
from LWP_satellite import LWP_satellite_dict

Temp_min=-35+273.15
#Temp_min=0

SW_dict=OrderedDict()
SW_dict_filtered=OrderedDict()

LWP_min=0.01
plt.figure(figsize=(20,20))
i=1
itime=12
for key in run_path:
    if 'C3' in key:
        itime=14
#        if key=='C3_DM10':
#            itime=11
    if 'C1' in key:
        itime=16
    print key
    if 'GLOBAL' in key:
#        if 'C2' in key:
#            continue
        sample_cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
        cube_SW=iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0][:,:]
        cube_LWP=iris.load(ukl.Obtain_name(run_path[key]+'L1/','LWP'))[0][itime,:,:]
        cube=stc.clean_cube(iris.load(run_path[key[:-6]+'DM10']+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
#        cube = cube.regrid(sample_cube, iris.analysis.Linear())
        cube_LWP = cube_LWP.regrid(sample_cube, iris.analysis.Linear())
        cube_SW = cube_SW.regrid(sample_cube, iris.analysis.Linear())
    else:
        cube=stc.clean_cube(iris.load(run_path[key]+'L1/L1_CTT_Cloud_top_temperature.nc')[0])[itime,:,:]
        cube_LWP=stc.clean_cube(iris.load(ukl.Obtain_name(run_path[key]+'L1/','LWP'))[0])[itime,:,:]
        cube_SW=stc.clean_cube(iris.load(run_path[key]+'All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')[0])
    mask=[(cube.data<Temp_min) | (cube_LWP.data<LWP_min)]
    print np.any(cube_LWP.data<LWP_min) 
#    print cube_SW.coord('time').points
    masked_cube=cube.data
    masked_cube[mask]=np.nan
#    plt.imshow(cube.data[:,:])
    if 'C3' in key:
        masked_cube=0.45*cube_SW[13,].data+0.55*cube_SW[14,].data
    elif 'C2' in key:
        masked_cube=0.25*cube_SW[16,].data+0.75*cube_SW[17,].data
    elif 'C1' in key:
        masked_cube=(cube_SW[16,].data+cube_SW[17,].data)/2.
        
#    masked_cube[mask]=np.nan

    np.save(pspc_fol+'SW_distribution_'+key,masked_cube)
    SW_dict[key]=np.mean(masked_cube[~np.isnan(masked_cube)])
    masked_cube[mask]=np.nan
    np.save(pspc_fol+'SW_distribution_filtered_'+key,masked_cube)
    levels=np.linspace(0,850,15).tolist()
    SW_dict_filtered[key]=np.mean(masked_cube[~np.isnan(masked_cube)])
    if 'C2' in key:
#        plt.hist(cube.)
        plt.subplot(3,3,i)
        plt.imshow(masked_cube[:,:],vmin=0,vmax=850)
        plt.title(key+str(SW_dict[key]))
        plt.colorbar()
#    print cube
        i=i+1

for key in SW_satellite_dict:
    print key
    sat_mask=[(CTT_satellite_dict[key]<Temp_min) | (LWP_satellite_dict[key]<LWP_min)][0]
    
    SW_dict[key]=np.mean(SW_satellite_dict[key])
    SW_dict_data[key]=np.copy(SW_satellite_dict[key])
    masked_data=np.copy(SW_satellite_dict[key])
    masked_data[sat_mask]=np.nan
    SW_dict_filtered[key]=np.nanmean(masked_data)
    SW_dict_filtered_data[key]=np.copy(masked_data)


#SW_dict['C2_GLOBAL']=SW_dict['C1_GLOBAL']#fix to avoid breaking, correct!! also the global runs will give more problems as there is not enough low cloud
#%%


#
#
#path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/'
#from scipy.io import netcdf
#
#mb=netcdf.netcdf_file(path+'CERES/'+'CERES_SSF_NPP-XTRK_Edition1A_Subset_2015030100-2015030223.nc','r') 
#
#times_ceres=mb.variables['time'].data*24*60*60
#
#
#LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
#lon=mb.variables['lon'].data
#lat=mb.variables['lat'].data
#
#ti=15#h
#te=16#h
#
#tdi=(datetime.datetime(2015,03,1,ti)-datetime.datetime(1970,1,1)).total_seconds()
#tde=(datetime.datetime(2015,03,1,te)-datetime.datetime(1970,1,1)).total_seconds()
#
#t16=(datetime.datetime(2015,03,1,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
#    
#sim_path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/'
#
##cube_DM10 =  stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0])
#cube_DM10 = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0])
#
##SW_dict[C1]
#
#reload(stc)
#model_lons,model_lats=stc.unrotated_grid(cube_DM10)
##times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
#times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
#sat_lon=lon[times_range]
#sat_lat=lat[times_range]
#sat_LW=LW[times_range]
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
##model_lons=np.linspace(-5,20,500)
#X,Y=np.meshgrid(model_lons, model_lats)
##Xo,Yo=np.meshgrid(lon_old,lat_old)
##data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
##grid_z0 = sc.interpolate.griddata(coord, sat_SW, (X,Y), method='nearest')
#grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
#plt.imshow(grid_z1)
#sat_cube=cube_DM10[16,:,:]
#sat_cube.data=grid_z1
#SW_dict['C1_SATELLITE']=np.nanmean(grid_z1)
#SW_dict_filtered['C1_SATELLITE']=np.nanmean(grid_z1)
#
##%%
#path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/'
#from scipy.io import netcdf
#mb=netcdf.netcdf_file(path+'CERES/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2015011000-2015011123.nc','r') 
#
#times_ceres=mb.variables['time'].data*24*60*60
#LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
##SW[SW>1400]=0
#lon=mb.variables['lon'].data
#lat=mb.variables['lat'].data
#
#ti=15#h
#te=18#h
#
#tdi=(datetime.datetime(2015,01,10,ti)-datetime.datetime(1970,1,1)).total_seconds()
#tde=(datetime.datetime(2015,01,10,te)-datetime.datetime(1970,1,1)).total_seconds()
#
#t16=(datetime.datetime(2015,01,10,16)-datetime.datetime(1970,1,1)).total_seconds()/3600.
#    
#sim_path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/'
#
#cube_DM10 = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0])
##SW_dict['C2_SATELLITE']=np.nanmean(grid_z1)
#reload(stc)
#model_lons,model_lats=stc.unrotated_grid(cube_DM10)
##times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
#times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
#sat_lon=lon[times_range]
#sat_lat=lat[times_range]
#sat_LW=LW[times_range]
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
##model_lons=np.linspace(-5,20,500)
#X,Y=np.meshgrid(model_lons, model_lats)
##Xo,Yo=np.meshgrid(lon_old,lat_old)
##data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
##grid_z0 = sc.interpolate.griddata(coord, sat_SW, (X,Y), method='nearest')
#grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
#SW_dict['C2_SATELLITE']=np.nanmean(grid_z1)
#SW_dict_filtered['C2_SATELLITE']=np.nanmean(grid_z1)
##%%
#path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
#from scipy.io import netcdf
#cubes  =iris.load(path+'ceres/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc')
#mb=netcdf.netcdf_file(path+'ceres/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc','r') 
#mb=netcdf.netcdf_file(path+'ceres_all_SO/'+'CERES_SSF_Aqua-XTRK_Edition4A_Subset_2014120900-2014121023.nc','r') 
#
##SW=cubes[1]
##model_lons=np.arange(-0.02*250,250*0.02,0.02)[0:]
##model_lats=np.arange(-0.02*250-52,250*0.02-52,0.02)
#
##model_lons=np.linspace(-7,17)
##model_lats=np.linspace(-47.5,-58)
#times_ceres=mb.variables['time'].data*24*60*60
#
##model_lons=model_lons+lon_offset
#
#LW=np.copy(mb.variables['CERES_SW_TOA_flux___upwards'].data)
##SW[SW>1400]=0
#lon=mb.variables['lon'].data
#lat=mb.variables['lat'].data
#
#ti=13#h
#te=15#h
#
#tdi=(datetime.datetime(2014,12,9,ti)-datetime.datetime(1970,1,1)).total_seconds()
#tde=(datetime.datetime(2014,12,9,te)-datetime.datetime(1970,1,1)).total_seconds()
#
#t13=(datetime.datetime(2014,12,9,14)-datetime.datetime(1970,1,1)).total_seconds()/3600.
#cube = stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/All_time_steps/','m01s01i208'))[0])
##cube_DM10 = stc.clean_cube(iris.load(ukl.Obtain_name(sim_path+'/DM10/All_time_steps/','m01s01i208'))[0])
#
#reload(stc)
#model_lons,model_lats=stc.unrotated_grid(cube)
##times_range=np.argwhere((times_ceres >= tdi) & (times_ceres <=tde))
#times_range=np.logical_and([times_ceres >= tdi],[times_ceres <=tde])[0]
#sat_lon=lon[times_range]
#sat_lat=lat[times_range]
#sat_LW=LW[times_range]
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
##model_lons=np.linspace(-5,20,500)
#X,Y=np.meshgrid(model_lons, model_lats)
##Xo,Yo=np.meshgrid(lon_old,lat_old)
##data_old= sc.interpolate.griddata(coord_model, cube_oldm.data.flatten(), (X,Y), method='linear')
##grid_z0 = sc.interpolate.griddata(coord, sat_SW, (X,Y), method='nearest')
#grid_z1 = sc.interpolate.griddata(coord, sat_LW, (X,Y), method='linear')
#
#SW_dict['C3_SATELLITE']=np.nanmean(grid_z1)
#SW_dict_filtered['C3_SATELLITE']=np.nanmean(grid_z1)
#
#
#plt.imshow(grid_z1)


#%%
#SW_dict['C2_GLOBAL']=0
#SW_dict['C3_GLOBAL']=0
np.save(pspc_fol+'SW_dict',SW_dict)
np.save(pspc_fol+'SW_dict_filtered',SW_dict_filtered)

list_params=['SATELLITE','GLOBAL','M92','DM10','DM15','VT17_HIGH','VT17_MEAN','VT17_LOW']
list_colors=['b','y','r','green','peru','k','grey','silver']
list_clouds=['C1','C2','C3']

N = len(list_clouds)
ind = np.arange(N)  # the x locations for the groups
fig, ax = plt.subplots()
width = 0.1       # the width of the bars
iparam=0
for param in list_params:
    means = tuple([SW_dict_filtered[cloud+'_'+param] for cloud in list_clouds])
    std = tuple([SW_dict_filtered[cloud+'_'+param]*0.0 for cloud in list_clouds])


    rects1 = ax.bar(ind+iparam*width, means, width, color=list_colors[iparam], yerr=std,label=param)
    iparam=iparam+1
plt.legend()
ax.set_xticks(ind +len(list_params)*width/2 +width / 2)
ax.set_xticklabels(tuple(list_clouds))
plt.ylim(200,600)
plt.xlim(0,5)

ax.set_title('a) Reflected SW radiation')
ax.set_ylabel('Reflected SW radiation $\mathrm{W/m^2}$')

plt.savefig(sav_fol+'SW_reflected_barplot.png')