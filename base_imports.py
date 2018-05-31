#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:47:48 2017

@author: eejvt
"""


import numpy as np
import sys
sys.path.append('/nfs/see-fs-01_users/eejvt/PYTHON_CODE')
import Jesuslib as jl
import matplotlib.style
matplotlib.style.use('classic')

import os
from scipy.io.idl import readsav
from glob import glob
from scipy.io import netcdf
import matplotlib.pyplot as plt
import scipy as sc
from scipy.stats.stats import pearsonr
from glob import glob
from scipy.io.idl import readsav
from mpl_toolkits.basemap import Basemap
import datetime
from matplotlib.colors import LogNorm
from matplotlib import colors, ticker, cm
from scipy.io import netcdf
import scipy as sc
sys.path.append('/nfs/see-fs-01_users/eejvt/PYTHON_CODE/Satellite_Comparison')
import satellite_comparison_suite as stc
import iris
dir_scripts='/nfs/see-fs-01_users/eejvt/UKCA_postproc'#Change this to the downloaded folder
sys.path.append(dir_scripts)
import UKCA_lib as ukl
import glob
sav_fol='/nfs/see-fs-01_users/eejvt/SO_paper/'
pspc_fol='/nfs/a201/eejvt/CASIM/PSPC_DATA/'
from pyhdf import SD
import matplotlib as mpl


mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['font.size'] = 20
mpl.rcParams['legend.fontsize']= 15
mpl.rcParams['legend.frameon'] = 'False'

n05=56000*1e-6
n05_dust=56000*1e-6
n05_GLOMAP=21.26#cm-3 surface SO
n05_bug_meters=56000

def get_times_as_datetime(cube):
    list_times=cube.coord('time').units.num2date(cube.coord('time').points).tolist()
    return list_times

#All the outputs are in m-3
#all the temps have to be given in C
def meyers_param(T,units_cm=0):
    a=-0.639
    b=0.1296
    return np.exp(a+b*(100*(jl.saturation_ratio_C(T)-1)))*1e3#m-3

def demott_dust(T,N=n05_dust):
    a_demott = 0.0
    b_demott = 1.25
    c_demott = 0.46
    d_demott = -11.6
    cf = 3.0
    Tp01=0.01-T

    dN_imm = 1.0e3*cf*(N)**(a_demott*(Tp01)+b_demott)*np.exp(c_demott*(Tp01)+d_demott)
    return dN_imm


def demott(T,N=n05_GLOMAP):
    a_demott=5.94e-5
    b_demott=3.33
    c_demott=0.0264
    d_demott=0.0033
    Tp01=0.01-T
    dN_imm=1e3*a_demott*(Tp01)**b_demott*(N)**(c_demott*Tp01+d_demott)
    return dN_imm


def GLO_high(Tc):
    #!GLOMAP SO maximum INP parameterization based of Feldspar and Marine
    #   !organic aerosols.
    INP=np.exp(-5.147-1.06*Tc-1.6219e-1*Tc**2-1.4335e-2*Tc**3-4.7019e-4*Tc**4-5.12168e-6*Tc**5)
    return INP
def GLO_mean(Tc):
    #    !GLOMAP SO mean INP parameterization based of Feldspar and Marine
    #    !organic aerosols.
    INP=np.exp(-8.6516-1.0503*Tc-1.5545e-1*Tc**2-1.3496e-2*Tc**3-4.302e-4*Tc**4-4.5357e-6*Tc**5)
    return INP
def GLO_low(Tc):
    #    !GLOMAP SO minimum INP parameterization based of Feldspar and Marine
    #    !organic aerosols.
    INP=np.exp(-1.2118e+1-6.4187e-1*Tc-4.4918e-2*Tc**2-3.4394e-3*Tc**3-8.9326e-5*Tc**4-6.9993e-7*Tc**5)
    return INP

def check_nan(array):
    return np.isnan(array).any()


from collections import OrderedDict


param=OrderedDict()
param['M92']=meyers_param
param['DM10']=demott
param['DM15']=demott_dust
param['VT17_HIGH']=GLO_high
param['VT17_MEAN']=GLO_mean
param['VT17_LOW']=GLO_low
#def choose_param


run_path=OrderedDict()
run_path_collocated=OrderedDict()
run_path_wc=OrderedDict()

#run_path={}
run_path['C3_GLOBAL']='/nfs/a201/eejvt/CASIM/SO_KALLI/GLOBAL/'
run_path['C3_M92']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/MEYERS/'#
run_path['C3_M92']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/MEYERS_RIGHT_PROFILE/'#

run_path['C3_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/DEMOTT_GLO_N05_HAMISHPROF/'#
run_path['C3_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/'#
run_path['C3_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/DM10_REPEAT/'#
run_path['C3_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLOMAP_PROFILE_DM/'#
run_path['C3_VT17_HIGH']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLO_HIGH/'
run_path['C3_VT17_MEAN']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLO_MEAN/'
run_path['C3_VT17_LOW']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLO_MIN/'
run_path['C3_DM15']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GP_HAMISH_DMDUST/'#

sim_path_C1='/nfs/a201/eejvt/CASIM/SECOND_CLOUD'

run_path['C1_GLOBAL']=sim_path_C1+'/GLOBAL/'
run_path['C1_M92']=sim_path_C1+'/MEYERS/'
run_path['C1_DM10']=sim_path_C1+'/DM10/'
run_path['C1_VT17_HIGH']=sim_path_C1+'/GLO_HIGH/'
run_path['C1_VT17_MEAN']=sim_path_C1+'/GLO_MEAN/'
run_path['C1_VT17_LOW']=sim_path_C1+'/GLO_MIN/'
run_path['C1_DM15']=sim_path_C1+'/GP_HAM_DMDUST/'

sim_path_wc='/nfs/a201/eejvt/CASIM/WHOLE_CYCLONE'
run_path_wc['C1_GLOBAL']=sim_path_C1+'/GLOBAL/'
run_path_wc['C1_M92']=sim_path_wc+'/MEYERS/'
run_path_wc['C1_VT17_MEAN']=sim_path_wc+'/VT17_MEAN/'



sim_path_C2='/nfs/a201/eejvt/CASIM/THIRD_CLOUD'
run_path['C2_GLOBAL']=sim_path_C2+'/GLOBAL/'
run_path['C2_M92']=sim_path_C2+'/MEYERS/'
run_path['C2_DM10']=sim_path_C2+'/DM10/'
run_path['C2_VT17_HIGH']=sim_path_C2+'/GLO_HIGH/'
run_path['C2_VT17_MEAN']=sim_path_C2+'/GLO_MEAN/'
run_path['C2_VT17_LOW']=sim_path_C2+'/GLO_MIN/'
run_path['C2_DM15']=sim_path_C2+'/DM_DUST/'


#for key in run_path:
#    run_path_collocated[key]=run
#
#

cloud_it={}
cloud_it['C3']=13
cloud_it['C1']=16
cloud_it['C2']=17


def unrotated_grid(cube):
    rotated_cube=isinstance(cube.coord('grid_longitude').coord_system,iris.coord_systems.RotatedGeogCS)
    if rotated_cube:
        pole_lat=cube.coord('grid_latitude').coord_system.grid_north_pole_latitude
        pole_lon=cube.coord('grid_longitude').coord_system.grid_north_pole_longitude
        lons, lats =iris.analysis.cartography.unrotate_pole(cube.coord('grid_longitude').points,cube.coord('grid_latitude').points,pole_lon,pole_lat)
    else:
        lons=cube.coord('grid_longitude').points
        lats=cube.coord('grid_latitude').points
    return lons,lats


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




max_INP=[0.005883385377183883,
 0.009189837845786452,
 0.014355279089974667,
 0.022426279663887487,
 0.035041161528422994,
 0.0547691992936143,
 0.08565267422080879,
 0.13408808035777434,
 0.21029997441732057,
 0.33091870575824306,
 0.5237843851750961,
 0.837646981153638,
 1.3635203667637412,
 2.739284582005597,
 6.445839408293471,
 16.179615319152475,
 42.521726886376534,
 115.01419887075012,
 316.13950779564686,
 873.4225027730198,
 2391.6094119367453,
 6313.096011833937,
 15135.689784847562,
 30005.70305195412,
 47613.89453809925,
 75634.49163287842,
 103568.88725559277,
 104839.90909508808,
 105138.91313806176,
 105601.81371179223,
 106324.81590905786,
 107454.0693270266,
 109217.84520593286,
 111972.67821374536,
 116275.43895593286,
 122995.90184655786,
 133492.55809655786,
 149887.23778405786]

mean_INP=[0.0006643551335725025,
 0.0010377069050818962,
 0.001620941364482327,
 0.002532167988750253,
 0.0039561836861334325,
 0.006182514554180749,
 0.009665838348660336,
 0.015123018392361154,
 0.023691562899488136,
 0.03719449578024836,
 0.0585967517557166,
 0.09282206526800497,
 0.1482810096948136,
 0.2398633810837054,
 0.3950668186884211,
 0.6669972526046696,
 1.1630259912026446,
 2.1096663034587313,
 4.003836248027252,
 7.972279660508055,
 16.630163885944018,
 36.061508271067844,
 79.72625891295438,
 172.27192518416481,
 339.31951063079117,
 583.0129007189229,
 954.4804919108026,
 1388.5702484434687,
 1728.115981144875,
 2014.7806711026499,
 2316.8663685076076,
 2703.760816726174,
 3245.655030258315,
 4022.888903355971,
 5154.1508623347145,
 6823.03162711599,
 9315.733740626767,
 13079.636521633685]

min_INP=[2.8544803904326104e-06,
 4.458698945083808e-06,
 6.964867186537741e-06,
 1.0880781400422477e-05,
 1.700138742472562e-05,
 2.6573434136328806e-05,
 4.155870450163481e-05,
 6.506221564677916e-05,
 0.00010204918291076135,
 0.0001606009683906574,
 0.00025426081144360065,
 0.00040678250074272404,
 0.0006626102029840064,
 0.001111895623005213,
 0.001953992593115736,
 0.003665581190499683,
 0.0074518704092250265,
 0.01653592971175688,
 0.03964833764500633,
 0.08299436677434069,
 0.13703405388903142,
 0.234875249914448,
 0.4252200011263641,
 0.8251883063005294,
 1.7163392010736642,
 2.8853993711696218,
 4.618609804409737,
 7.487168972975537,
 12.262291438855831,
 19.732497175429586,
 30.66311174909225,
 46.54572071444697,
 60.08420910638299,
 81.27241574941127,
 108.9346564650732,
 143.73600991966305,
 198.09205850364742,
 282.9905417800146]

temps_for_INP=[0.0,
 -1.0,
 -2.0,
 -3.0,
 -4.0,
 -5.0,
 -6.0,
 -7.0,
 -8.0,
 -9.0,
 -10.0,
 -11.0,
 -12.0,
 -13.0,
 -14.0,
 -15.0,
 -16.0,
 -17.0,
 -18.0,
 -19.0,
 -20.0,
 -21.0,
 -22.0,
 -23.0,
 -24.0,
 -25.0,
 -26.0,
 -27.0,
 -28.0,
 -29.0,
 -30.0,
 -31.0,
 -32.0,
 -33.0,
 -34.0,
 -35.0,
 -36.0,
 -37.0]

#
