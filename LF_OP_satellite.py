#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 10:35:16 2017

@author: eejvt
"""
from base_imports import *

from pyhdf import SD

#==============================================================================
# CLOUD 3
#==============================================================================
path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'

LF_OP_satellite_dict=OrderedDict()
LF_OP_satellite_dict_undeterminated=OrderedDict()


sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')

path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
SDS_NAME  = 'Cloud_Top_Temperature'
hdf  =SD.SD(path+'modis/'+'MYD06_L2.A2014343.1325.006.2014344210847.hdf')


SDS_NAME  = 'Cloud_Phase_Infrared'
SDS_NAME  = 'Cloud_Phase_Optical_Properties'
#print hdf.datasets().keys()
sds = hdf.select(SDS_NAME)
print sds.attributes()
data = sds.get()

cube= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/DM10_REPEAT/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])


model_lons,model_lats=stc.unrotated_grid(cube)
lon_max=model_lons.max()
lon_min=model_lons.min()
lat_max=model_lats.max()
lat_min=model_lats.min()

path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
hdf  =SD.SD(path+'modis/'+'MYD03.A2014343.1325.006.2014344162340.hdf')

SDS_NAME  = 'Latitude'
sds = hdf.select(SDS_NAME)
lat = sds.get()
SDS_NAME  = 'Longitude'
sds = hdf.select(SDS_NAME)
lon = sds.get()
valids=[(lon>lon_min) & (lon<lon_max) & (lat>lat_min) & (lat<lat_max)]
data=data[valids]




#missing_fraction=np.array(data==0).sum()/float(data.size)
missing_fraction=np.array(data==0).sum()/float(data.size)
clear_fraction=np.array(data==1).sum()/float(data.size)
liquid_fraction=np.array(data==2).sum()/float(data.size)
ice_fraction=np.array(data==3).sum()/float(data.size)
undeterminated_fraction=np.array(data==4).sum()/float(data.size)

print missing_fraction,clear_fraction,liquid_fraction,undeterminated_fraction,ice_fraction


#print clear_fraction,liquid_fraction,undeterminated_fraction,ice_fraction,mixed_fraction
print clear_fraction+liquid_fraction+undeterminated_fraction+ice_fraction

cloud_fraction=liquid_fraction+undeterminated_fraction+ice_fraction
print 'CLOUD 3'
print 'liquid fraction',(liquid_fraction+undeterminated_fraction)/cloud_fraction

LF_OP_satellite_dict['C3_SATELLITE']=(liquid_fraction+undeterminated_fraction)/cloud_fraction
LF_OP_satellite_dict_undeterminated['C3_SATELLITE']=(undeterminated_fraction)/cloud_fraction

#plt.imshow(data)
#
#np.array(data==0).sum()/float(data.size)
#data[data==mask_value]=np.float64('Nan')
#print data.shape
#lat = hdf.select('Latitude')
#latitude = lat[:,:]
#lon = hdf.select('Longitude')
#longitude = lon[:,:]
#
#
#sat_lon=longitude.flatten()
#sat_lat=latitude.flatten()
#sat_data=data.flatten()
##for att in sds.attributes():
#cube = iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/L1/','CTH'))[0]
##cube = iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/All_time_steps/','All_time_steps_m01s00i254_mass_fraction_of_cloud_liquid_water_in_air.nc'))[0]
##cube_pressure = iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/All_time_steps/','All_time_steps_m01s00i408_air_pressure.nc'))[0]
###    print attAll_time_steps_m01s00i254_mass_fraction_of_cloud_liquid_water_in_air.ncAll_time_steps_m01s00i408_air_pressure.nc
##
##plt.colorbar()
##
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
#model_lons,model_lats=stc.unrotated_grid(cube)
#X,Y=np.meshgrid(model_lons, model_lats)
#
#grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
##grid_z1[np.isnan(grid_z1)]=0
#grid_z1[grid_z1<220]=np.nan
#np.nanmin(grid_z1)
#
#CTT_satellite_dict['C3_SATELLITE']=grid_z1
#plt.figure()
#plt.imshow(grid_z1)
#%%

path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/SATELLITE/'
SDS_NAME  = 'Cloud_Top_Temperature'
hdf  =SD.SD(path+'MODIS/'+'MOD06_L2.A2015060.1050.006.2015061055531.hdf')
#print hdf.datasets().keys()




SDS_NAME  = 'Cloud_Phase_Optical_Properties'
#print hdf.datasets().keys()
sds = hdf.select(SDS_NAME)
#print sds.attributes()
data = sds.get()
#data=(data+15000)*0.009999999776482582
#mask_value=-9999
#mask_value=-32767

cube= stc.clean_cube(iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SECOND_CLOUD/GLO_MEAN/A_TRAIN_COLLOCATED/','Cloud_droplet_concentratio_at_maximum_cloud_water_content'))[0])



model_lons,model_lats=stc.unrotated_grid(cube)
lon_max=model_lons.max()
lon_min=model_lons.min()
lat_max=model_lats.max()
lat_min=model_lats.min()


hdf  =SD.SD('/nfs/a201/eejvt/CASIM/ND_SATELLITE/MYD03.A2015060.1630.006.2015061161318.hdf')
SDS_NAME  = 'Latitude'
sds = hdf.select(SDS_NAME)
lat = sds.get()
SDS_NAME  = 'Longitude'
sds = hdf.select(SDS_NAME)
lon = sds.get()
valids=[(lon>lon_min) & (lon<lon_max) & (lat>lat_min) & (lat<lat_max)]
data=data[valids]





missing_fraction=np.array(data==0).sum()/float(data.size)
clear_fraction=np.array(data==1).sum()/float(data.size)
liquid_fraction=np.array(data==2).sum()/float(data.size)
ice_fraction=np.array(data==3).sum()/float(data.size)
undeterminated_fraction=np.array(data==4).sum()/float(data.size)

print missing_fraction,clear_fraction,liquid_fraction,undeterminated_fraction,ice_fraction


cloud_fraction=liquid_fraction+undeterminated_fraction+ice_fraction
print 'CLOUD 1'
print 'liquid fraction',(liquid_fraction+undeterminated_fraction)/cloud_fraction
LF_OP_satellite_dict['C1_SATELLITE']=(liquid_fraction+undeterminated_fraction)/cloud_fraction
LF_OP_satellite_dict_undeterminated['C1_SATELLITE']=(undeterminated_fraction)/cloud_fraction


#
#sds = hdf.select(SDS_NAME)
#data = sds.get()
#data=(data+15000)*0.009999999776482582
#mask_value=-9999
#mask_value=-32767
#data[data==mask_value]=np.float64('Nan')
#print data.shape
#lat = hdf.select('Latitude')
#latitude = lat[:,:]
#lon = hdf.select('Longitude')
#longitude = lon[:,:]
#
#
#sim_path='/nfs/a201/eejvt/CASIM/SECOND_CLOUD/'
#sub_folder='L1/'
#code='CTT'
#cube = iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0]
#
#cube = iris.load(ukl.Obtain_name(sim_path+'GLO_MEAN/All_time_steps/','m01s00i254'))[0]
#cube_ice = iris.load(ukl.Obtain_name(sim_path+'GLO_MEAN/All_time_steps/','m01s00i012'))[0]
#cube_pressure = iris.load(ukl.Obtain_name(sim_path+'GLO_MEAN/All_time_steps/','All_time_steps_m01s00i408_air_pressure.nc'))[0]
#
##plt.imshow(cube[15,:,:].data.mean(axis))
##plt.plot(cube[15,:,:,:].data.mean(axis=(1,2)),cube_pressure[15,:,:,:].data.mean(axis=(1,2)))
##plt.plot(cube_ice[15,:,:,:].data.mean(axis=(1,2)),cube_pressure[15,:,:,:].data.mean(axis=(1,2)))
##
#
#sat_lon=longitude.flatten()
#sat_lat=latitude.flatten()
#sat_data=data.flatten()
##for att in sds.attributes():
##cube = iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/L1/','CTT'))[0]
##    print att
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
#model_lons,model_lats=stc.unrotated_grid(cube)
#X,Y=np.meshgrid(model_lons, model_lats)
#
#grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
##grid_z1[np.isnan(grid_z1)]=0
##grid_z1[grid_z1<0]=np.nan
#grid_z1[grid_z1<220]=np.nan
#
#
#CTT_satellite_dict['C1_SATELLITE']=grid_z1
##plt.figure()
##plt.imshow(grid_z1)
##plt.colorbar()

#%%


path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/'
SDS_NAME  = 'Cloud_Top_Temperature'
hdf  =SD.SD(path+'MODIS/'+'MYD06_L2.A2015010.1645.006.2015012151745.hdf')






SDS_NAME  = 'Cloud_Phase_Optical_Properties'
#print hdf.datasets().keys()
sds = hdf.select(SDS_NAME)
print sds.attributes()
data = sds.get()
#data=(data+15000)*0.009999999776482582
#mask_value=-9999
#mask_value=-32767

cube = iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/DM10/L1','LWP'))[0]



model_lons,model_lats=stc.unrotated_grid(cube)
lon_max=model_lons.max()
lon_min=model_lons.min()
lat_max=model_lats.max()
lat_min=model_lats.min()


hdf  =SD.SD('/nfs/a201/eejvt/CASIM/ND_SATELLITE/MYD03.A2015010.1645.006.2015012123319.hdf')
SDS_NAME  = 'Latitude'
sds = hdf.select(SDS_NAME)
lat = sds.get()
SDS_NAME  = 'Longitude'
sds = hdf.select(SDS_NAME)
lon = sds.get()
valids=[(lon>lon_min) & (lon<lon_max) & (lat>lat_min) & (lat<lat_max)]
data=data[valids]


missing_fraction=np.array(data==0).sum()/float(data.size)
clear_fraction=np.array(data==1).sum()/float(data.size)
liquid_fraction=np.array(data==2).sum()/float(data.size)
ice_fraction=np.array(data==3).sum()/float(data.size)
undeterminated_fraction=np.array(data==4).sum()/float(data.size)

print missing_fraction,clear_fraction,liquid_fraction,undeterminated_fraction,ice_fraction

cloud_fraction=liquid_fraction+undeterminated_fraction+ice_fraction
print 'CLOUD 2'
print 'liquid fraction',(liquid_fraction+undeterminated_fraction)/cloud_fraction

LF_OP_satellite_dict['C2_SATELLITE']=(liquid_fraction+undeterminated_fraction)/cloud_fraction
LF_OP_satellite_dict_undeterminated['C2_SATELLITE']=(undeterminated_fraction)/cloud_fraction

#sds = hdf.select(SDS_NAME)
#data = sds.get()
#data=(data+15000)*0.009999999776482582
#mask_value=-9999
#mask_value=-32767
#data[data==mask_value]=np.float64('Nan')
#print data.shape
#lat = hdf.select('Latitude')
#latitude = lat[:,:]
#lon = hdf.select('Longitude')
#longitude = lon[:,:]
#
#
#
#sat_lon=longitude.flatten()
#sat_lat=latitude.flatten()
#sat_data=data.flatten()
#
#hdf  =SD.SD(path+'MODIS/'+'MYD06_L2.A2015010.1640.006.2015012160803.hdf')
#sds = hdf.select(SDS_NAME)
#data = sds.get()
#data=(data+15000)*0.009999999776482582
#mask_value=-9999
#mask_value=-32767
#data[data==mask_value]=np.float64('Nan')
#print data.shape
#lat = hdf.select('Latitude')
#latitude = lat[:,:]
#lon = hdf.select('Longitude')
#longitude = lon[:,:]
#
#
#
#sat_lon=np.concatenate((sat_lon,longitude.flatten()))
#sat_lat=np.concatenate((sat_lat,latitude.flatten()))
#sat_data=np.concatenate((sat_data,data.flatten()))
#
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
#model_lons,model_lats=unrotated_grid(cube)
#X,Y=np.meshgrid(model_lons, model_lats)
#grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
##grid_z1[np.isnan(grid_z1)]=0
#grid_z1[grid_z1<220]=np.nan
#
#
#CTT_satellite_dict['C2_SATELLITE']=grid_z1
#plt.figure()
#plt.imshow(grid_z1)#
#plt.colorbar()


#%%

#from pyhdf import SD
#path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/'
#SDS_NAME  = 'Cloud_Top_Height_Nadir_Night'
#SDS_NAME  = 'cloud_top_height_1km'
##hdf = SD.SD(FILE_NAME)
#SDS_NAME  = 'Cloud_Top_Height'
#SDS_NAME  = 'Cloud_Top_Temperature'
#SDS_NAME  = 'Cloud_Water_Path_37'
#SDS_NAME  = 'Cloud_Water_Path'
#hdf  =SD.SD(path+'MODIS/'+'MYD06_L2.A2015010.1645.006.2015012151745.hdf')
##print hdf.datasets().keys()
#for k in hdf.datasets().keys():
#    if 'Water' in k:
#        print k
#        sds = hdf.select(k)
#        data = sds.get()
#        print data.shape
#
#sds = hdf.select(SDS_NAME)
#data = sds.get( )
#mask_value=-9999
#data[data==mask_value]=np.float64('Nan')
#data=jl.congrid(data,hdf.select('Latitude')[:,:].shape)
##data=(data+15000)*0.009999999776482582
##mask_value=-32767
#print data.shape
#lat = hdf.select('Latitude')
#latitude = lat[:,:]
#lon = hdf.select('Longitude')
#longitude = lon[:,:]
#
#
#
#
#cloud_top= iris.load(ukl.Obtain_name('/nfs/a201/eejvt/CASIM/THIRD_CLOUD/DM10/All_time_steps','m01s09i223'))[0]
#
#sat_lon=longitude.flatten()
#sat_lat=latitude.flatten()
#sat_data=data.flatten()
#
#hdf  =SD.SD(path+'MODIS/'+'MYD06_L2.A2015010.1640.006.2015012160803.hdf')
#sds = hdf.select(SDS_NAME)
#data = sds.get( )
#import pprint
#mask_value=-9999
#data[data==mask_value]=np.float64('Nan')
#data=jl.congrid(data,hdf.select('Latitude')[:,:].shape)
##data=(data+15000)*0.009999999776482582
##mask_value=-32767
#print data.shape
#lat = hdf.select('Latitude')
#latitude = lat[:,:]
#lon = hdf.select('Longitude')
#longitude = lon[:,:]
#
#
#sat_lon=np.concatenate((sat_lon,longitude.flatten()))
#sat_lat=np.concatenate((sat_lat,latitude.flatten()))
#sat_data=np.concatenate((sat_data,data.flatten()))
#
#coord=np.zeros([len(sat_lon),2])
#coord[:,0]=sat_lon
#coord[:,1]=sat_lat
#cm=plt.cm.RdBu_r
#model_lons,model_lats=unrotated_grid(cloud_top)
#X,Y=np.meshgrid(model_lons, model_lats)
#grid_z1 = sc.interpolate.griddata(coord, sat_data, (X,Y), method='linear')
#grid_z1[np.isnan(grid_z1)]=0
#
#
##plt.figure()
##plt.figure(figsize=(15,13))
##levels=np.linspace(0.,1).tolist()
##plt.subplot(221)
##plt.contourf(X,Y,grid_z1*1e-3,levels, origin='lower',cmap=cm)
##plt.title('Satellite (MODIS)')
##cb=plt.colorbar()
##cb.set_label('CTT')
##
#CTT_satellite_dict['C2_SATELLITE']=grid_z1*1e-3
#
#
##%%
#
##
##path='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/'
##
##
##sys.path.append('/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code')
##from amsr2_daily_v7 import AMSR2daily
##amsr_data='/nfs/a201/eejvt/CASIM/SO_KALLI/SATELLITE/code/data.remss.com/amsr2/bmaps_v07.2/y2014/m12/'
##amsr_data='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/SATELLITE/AMSR2/'
##glob.glob(amsr_data+'*')
##def read_data(filename=amsr_data+'f34_20150110v7.2.gz'):
##    dataset = AMSR2daily(filename, missing=missing)
##    if not dataset.variables: sys.exit('problem reading file')
##    return dataset
##
##ilon = (169,174)
##ilat = (273,277)
##iasc = 0
##avar = 'vapor'
##missing = -999.
##
##dataset = read_data()
##
##
##sim_path='/nfs/a201/eejvt/CASIM/THIRD_CLOUD/'
##sub_folder='L1/'
##code='CTT'
##
##cube_DM10 = iris.load(ukl.Obtain_name(sim_path+'/DM10/'+sub_folder,code))[0]
##
##
##
##
##
##times=dataset.variables['time'][1,]
##
##times[times==-999.]=np.nan
##plt.figure()
##plt.imshow(times)
##plt.colorbar()
##plt.show()
##CTT=dataset.variables['cloud'][0,]
##CTT[times<15]=np.nan
##CTT[times>18]=np.nan
##CTT[CTT==missing]=np.nan
##
##lon=dataset.variables['longitude']
##lon[lon>180]=lon[lon>180]-360
##lat=dataset.variables['latitude']
##Xsat,Ysat=np.meshgrid(lon,lat)
##Xsat[np.isnan(CTT)]=np.nan
##Ysat[np.isnan(CTT)]=np.nan
##Xsat_flat=Xsat.flatten()
##Ysat_flat=Ysat.flatten()
##CTT_flat=CTT.flatten()
##Xsat_flat=Xsat_flat[np.logical_not(np.isnan(Xsat_flat))]
##Ysat_flat=Ysat_flat[np.logical_not(np.isnan(Ysat_flat))]
##CTT_flat=CTT_flat[np.logical_not(np.isnan(CTT_flat))]
##def check_nan(array):
##    return np.isnan(array).any()
##model_lons,model_lats=stc.unrotated_grid(cube_DM10)
##max_lon,min_lon=model_lons.max(),model_lons.min()
##max_lat,min_lat=model_lats.max(),model_lats.min()
##coord=np.zeros([len(Xsat_flat),2])
##coord[:,0]=Xsat_flat
##coord[:,1]=Ysat_flat
##cm=plt.cm.RdBu_r
##X,Y=np.meshgrid(model_lons, model_lats)
##grid_z1 = sc.interpolate.griddata(coord, CTT_flat, (X,Y), method='linear')
##plt.figure()
##plt.imshow(grid_z1,cmap=plt.cm.RdBu)
##
##CTT_satellite_dict['C2_SATELLITE']=grid_z1
#
