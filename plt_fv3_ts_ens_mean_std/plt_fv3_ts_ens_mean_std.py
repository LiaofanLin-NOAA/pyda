'''
Purpose: Plot the time series (ts) of ensemble mean and STD of each member
 
Input: FV3 dyn or phy forecast files

Output: 

History Log:
   2022.04.04: Liaofan Lin - Created
'''


#%% ====================================
#   Loading libraries
#   ====================================
import matplotlib 
import matplotlib.pyplot as plt
import numpy as np
import yaml
import sys 
import os
import math
import pickle
from netCDF4 import Dataset

#Necessary to generate figs when not running an Xserver (e.g. via PBS)
plt.switch_backend('agg')


#%% =====================================
#   Variables to be edited
#   =====================================
SWITCH_DATA_PROCESS = False
SWITCH_PLOTTING     = True


#CASEID = 54
#casedir = "/scratch1/BMC/zrtrr/llin/220101_rrfs_dev1/STMP/tmpnwprd/RRFS_CONUS_13km_case54_enkf_20210915_3days"
#size_cycle  = 24  # number of cycles

CASEID = 53
casedir = "/scratch1/BMC/zrtrr/llin/220101_rrfs_dev1/STMP/tmpnwprd/RRFS_CONUS_13km_case53_efsoi_20210915_3days"
size_cycle  = 16  # number of cycles


size_member = 20  # size of ensemble members

 
# Cycle time information
YEAR = '2021'
DATE = ['0915','0916','0917']
HOUR = ['00','03','06','09','12','15','18','21'] 
 
# Specifying the layer of interest
#   - RRFS has a total of 65 atmoephric layers.  Layer 65 is the bottom of atmosphere
#   - RUC LSM has 9 layers, while Noah LSM has 4.
NO_LAYER = 65  

# File type: dyn or phy
#   - Variables in dyn: tmp, spfh, vgrd, ugrd, ...
#   - Variables in phy: soilw1, soilw2, ...
FILE_TYPE = 'dyn' 

# Variables
#VARIABLE_STR = 'tmp'
VARIABLE_STR = 'spfh'
 
# Figure Title
#FIGURE_TITLE = 'Ensemble Statistics for 3-h Temperature Fcst (Layer 65) [K]'
FIGURE_TITLE = 'Ensemble Statistics for 3-h Specific Humidity Fcst (Layer 65) [m3/m3]'


#%% =====================================
#   Data Process 
#   =====================================
if SWITCH_DATA_PROCESS == True:

    # Define Variables
    ens_avg = np.zeros((size_member,size_cycle))
    ens_std = np.zeros((size_member,size_cycle))

    print('Case ' + str(CASEID)) 

    # Loading variables of interest from each member and each cycle
    for cc in range(0,size_cycle):
    
        # Construct the time string
        TIME_STR = YEAR + DATE[math.floor(cc/8)] + HOUR[cc%8]
    
        print('Processing ' + VARIABLE_STR +' data on ' + TIME_STR)
    
        for mm in range(0,size_member):
    
            # Contstruct the member string
            if mm+1 < 10:
                mem_str = '0'+str(mm+1)
            else:
                mem_str = str(mm+1)

    
            # Read a variable
            fname = casedir + '/' + TIME_STR + '/mem00' + mem_str + '/fcst_fv3lam/' + FILE_TYPE + 'f003.nc'
            # print(fname) # print file path and name
            ncfile = Dataset(fname)   
            var = np.squeeze( ncfile.variables[VARIABLE_STR][:])
            ncfile.close() 
             
            var_2d = var[NO_LAYER-1,:,:]
            var_2d_avg = np.mean(var_2d[:])
            var_2d_std = np.std(var_2d[:])
        
        
            ens_avg[mm,cc] = var_2d_avg
            ens_std[mm,cc] = var_2d_std
          
            #print(np.shape(var)) # print variable dimension
             
        
    # Open the pickle file
    outfile = open('./data_output/ens_stat_case'+str(CASEID)+'_'+VARIABLE_STR+'.pkl','wb')
    pickle.dump([ens_avg, ens_std],outfile)
    outfile.close()

    
      
#%% =====================================
#   Plotting
#   =====================================
if SWITCH_PLOTTING == True:
 
    print('Plotting ' + VARIABLE_STR +' data for Case ' + str(CASEID))
 
    # Figure Properties
    left_x = 0.26
    top_y  = 1
    vspace = 0.9
    hspace = 0.25
    width = 0.22
    height = 0.8
    
    # Read pickle files
    infile = open('./data_output/ens_stat_case'+str(CASEID)+'_'+VARIABLE_STR+'.pkl','rb')
    [ens_avg, ens_std] = pickle.load(infile)
    infile.close()    
                  
    # Plots
    plt.rcParams.update({'font.size': 14})
    fig = plt.subplots(2, 1, figsize=(10, 10))

    # subplot 01
    ax1 = plt.subplot(2,1,1)
    ax1.set_position([0.13, 0.57, 0.8, 0.38])
    plt.xlim(-0.5,24.5)
    
    if VARIABLE_STR == 'tmp':
        plt.ylim(290,299)
    else:
        plt.ylim(0.0094,0.0114)

    plt.plot(np.transpose(ens_avg))

    plt.grid(True)
    plt.xlabel('Cycles Every 3h From ' + YEAR + DATE[0] + HOUR[0])
    plt.ylabel('Ensemble Mean')
    plt.title(FIGURE_TITLE)

    # subplot 02
    ax2 = plt.subplot(2,1,2)
    ax2.set_position([0.13, 0.07, 0.8, 0.38])

    plt.plot(np.transpose(ens_std))
    plt.grid(True)
    plt.xlabel('Cycles Every 3h From ' + YEAR + DATE[0] + HOUR[0])
    plt.ylabel('Ensemble STD')
    plt.xlim(-0.5,24.5)
    
    if VARIABLE_STR == 'tmp':
        plt.ylim(5,7.5)
    else:
        plt.ylim(0.0042,0.0056)
        

   
    #plt.savefig(VARIABLE + '.png',bbox_inches='tight',dpi=300)
    plt.savefig(VARIABLE_STR + '_layer_' + str(NO_LAYER) + '_case' + str(CASEID)+'.png',bbox_inches='tight',dpi=100)
    plt.clf()
            
            
    