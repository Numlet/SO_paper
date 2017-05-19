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

sav_fol='/nfs/see-fs-01_users/eejvt/SO_paper/'



n05=56000*1e-6
n05_dust=56000*1e-6
n05_GLOMAP=21.26#cm-3 surface SO 
n05_bug_meters=56000


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




#def choose_param

from collections import OrderedDict

run_path=OrderedDict()

run_path={}
run_path['C1_GLOBAL']='/nfs/a201/eejvt/CASIM/SO_KALLI/GLOBAL/'
run_path['C1_M92']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/MEYERS/'#
#run_path['C1_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/DEMOTT_GLO_N05_HAMISHPROF/'#
run_path['C1_DM10']='/nfs/a201/eejvt/CASIM/SO_KALLI/TRY2/ALL_ICE_PROC/'#
run_path['C1_VT17_HIGH']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLO_HIGH/'
run_path['C1_VT17_MEAN']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLO_MEAN/'
run_path['C1_VT17_MIN']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GLO_MIN/'
run_path['C1_DM15']='/nfs/a201/eejvt/CASIM/SO_KALLI/NO_CLOUD_SQUEME/GP_HAMISH_DMDUST/'#

sim_path_C2='/nfs/a201/eejvt/CASIM/SECOND_CLOUD'

run_path['C2_GLOBAL']=sim_path_C2+'/GLOBAL/'
run_path['C2_M92']=sim_path_C2+'/MEYERS/'
run_path['C2_DM10']=sim_path_C2+'/DM10/'
run_path['C2_VT17_HIGH']=sim_path_C2+'/GLO_HIGH/'
run_path['C2_VT17_MEAN']=sim_path_C2+'/GLO_MEAN/'
run_path['C2_VT17_MIN']=sim_path_C2+'/GLO_MIN/'
run_path['C2_DM15']=sim_path_C2+'/GP_HAM_DMDUST/'

sim_path_C3='/nfs/a201/eejvt/CASIM/THIRD_CLOUD'
run_path['C3_GLOBAL']=sim_path_C3+'/GLOBAL/'
run_path['C3_M92']=sim_path_C3+'/MEYERS/'
run_path['C3_DM10']=sim_path_C3+'/DM10/'
run_path['C3_VT17_HIGH']=sim_path_C3+'/GLO_HIGH/'
run_path['C3_VT17_MEAN']=sim_path_C3+'/GLO_MEAN/'
run_path['C3_VT17_MIN']=sim_path_C3+'/GLO_MIN/'
run_path['C3_DM15']=sim_path_C3+'/DM_DUST/'

        

cloud_it={}
cloud_it['C1']=13
cloud_it['C2']=16
cloud_it['C3']=17
        
        
        
#