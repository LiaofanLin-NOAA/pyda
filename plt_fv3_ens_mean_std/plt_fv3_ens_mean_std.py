'''
Purpose: Plot the ensemble mean mean and STD (maps and domain mean time series)
 
Input: FV3 dyn or phy forecast files

Output: 

History Log:
   2022.04.08: Liaofan Lin - Created
'''


#%% ====================================
#   Loading libraries
#   ====================================
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import yaml
import sys 
import os
import math
import pickle
from netCDF4 import Dataset

# For Basemap (python book 2021.08.19)
import matplotlib.image as mpimg
import matplotlib.offsetbox as mpob
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap




#Necessary to generate figs when not running an Xserver (e.g. via PBS)
plt.switch_backend('agg')


#%% =====================================
#   Variables to be edited
#   =====================================
SWITCH_DP_GET_DATA       = False
SWITCH_DP_DM_CALCULATION = False
SWITCH_PLT_MAP           = True
SWITCH_PLT_TS            = True


# ------------------------------------------
SIZE_CASE  = 2
SIZE_CYCLE = 16  # number of cycles

CASEID  = [53,54]
CASEDIR = ["/scratch1/BMC/zrtrr/llin/220101_rrfs_dev1/STMP/tmpnwprd/RRFS_CONUS_13km_case53_efsoi_20210915_3days",\
           "/scratch1/BMC/zrtrr/llin/220101_rrfs_dev1/STMP/tmpnwprd/RRFS_CONUS_13km_case54_enkf_20210915_3days"]
# ------------------------------------------


# size of ensemble members
SIZE_MEMBER = 20  
 
# Cycle time information
YEAR = '2021'
DATE = ['0915','0916','0917']
HOUR = ['00','03','06','09','12','15','18','21'] 
 
# Specifying the layer of interest
#   - RRFS has a total of 65 atmoephric layers.  Layer 65 is the bottom of atmosphere
#   - RUC LSM has 9 layers, while Noah LSM has 4.
NO_LAYER = 65  


# Specifying the horizontal dimensions
XDIM = 393
YDIM = 225


# File type: dyn or phy
#   - Variables in dyn: tmp, spfh, vgrd, ugrd, ...
#   - Variables in phy: soilw1, soilw2, ...
FILE_TYPE = 'dyn' 

# Variables
VARIABLE_STR = 'tmp'
#VARIABLE_STR = 'spfh'
 
# Figure Title
FIGURE_TITLE = 'Statistics for 3-h Temperature Fcst (Layer 65) [K]'
#FIGURE_TITLE = 'Ensemble Statistics for 3-h Specific Humidity Fcst (Layer 65) [g/kg]'




#%%============================================================================
#  functions for plotting a map
# =============================================================================    
def func_plot_map(var_2d, lon, lat, TIME_STR, FIGURE_TITLE, VARIABLE_STR, caseid_str, figure_title02):

    # Create a figure
    plt.rcParams.update({'font.size': 14})
    fig,axes = plt.subplots(1, 1, figsize=(11,6))
    
    # Colormap
    cmap=plt.cm.get_cmap('jet',24)
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, cmap.N)
    
    #
    ax1 = plt.subplot(1,1,1)
    ax1.set_position([0.05, 0.05, 0.80, 0.80])
    
    # Computing the mean
    lon_0 = lon.mean()
    lat_0 = lat.mean()   
        
    m = Basemap(width=5100000,height=2900000,\
                resolution='l',projection='lcc',\
                lat_ts=23,lat_0=lat_0+1.25,lon_0=lon_0)
        
    # Create lon/lat suitable for the projection
    LON,LAT = m(lon,lat)    
        
    # Plot 2D variable
    cs = m.pcolor(LON,LAT,var_2d,cmap=cmap)
 
    plt.title(FIGURE_TITLE + '\n' \
              'Ensemble '+ figure_title02 +': Initialized at ' + TIME_STR[0:8] + ' ' + TIME_STR[8:10] + 'UTC')
           
    # Add boundary
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
            
    # Colorbar
    cbar_ax = fig.add_axes([0.88, 0.05, 0.015, 0.800])
    fig.colorbar(cs, cax=cbar_ax)

    # Colorbar limit
    if (VARIABLE_STR == 'tmp') & (figure_title02 == 'Mean'):
        plt.clim(273,310)
    elif (VARIABLE_STR == 'tmp') & (figure_title02 == 'STD'): 
        plt.clim(0,3)
    elif (VARIABLE_STR == 'spfh') & (figure_title02 == 'Mean'): 
        plt.clim(0.00125,0.02125)        
    elif (VARIABLE_STR == 'spfh') & (figure_title02 == 'STD'): 
        plt.clim(0,0.004)        
    else:
        print('WARNING: the color bar limit for this variable is not decided yet')

    # save Figure
    plt.savefig('./figures/Ens_' + figure_title02 + '_case'+ caseid_str + '_time_' + TIME_STR + '_' + VARIABLE_STR + '.png',\
                bbox_inches='tight',dpi=100)
    plt.close()  








#%% =============================================
#   Data Process (Getting Data From Each Member)
#   =============================================
if SWITCH_DP_GET_DATA == True:

    for index_case in range(0,SIZE_CASE):    
   
        print('Getting ' + VARIABLE_STR +' data for case ' + str(CASEID[index_case]))

        for cc in range(0,SIZE_CYCLE):
                
            # Construct the time string
            TIME_STR = YEAR + DATE[math.floor(cc/8)] + HOUR[cc%8]
            print('  - Initialized at ' + TIME_STR)    
                
            # Define variables
            var_2d_allens = np.zeros((SIZE_MEMBER,YDIM,XDIM))
                   
            for mm in range(0,SIZE_MEMBER):
    
                # Contstruct the member string
                if mm+1 < 10:
                    mem_str = '0'+str(mm+1)
                else:
                    mem_str = str(mm+1)        
    
                # Read a variable
                fname = CASEDIR[index_case] + '/' + TIME_STR + '/mem00' + mem_str + '/fcst_fv3lam/' + FILE_TYPE + 'f003.nc'
                ncfile = Dataset(fname)   
                var = np.squeeze( ncfile.variables[VARIABLE_STR][:])
                ncfile.close() 

                # Collect the data into the big array
                var_2d_allens[mm,:,:] = var[NO_LAYER-1,:,:]
 
            # Compute ens mean and std
            var_2d_avg = np.mean(var_2d_allens,axis=0)
            var_2d_std = np.std(var_2d_allens,axis=0)    

            # Save data into a pickle file
            outfile = open('./data_output/ens_stat_case' + str(CASEID[index_case]) + '_time_' + TIME_STR + '_' + VARIABLE_STR + '.pkl','wb')
            pickle.dump([var_2d_avg, var_2d_std],outfile)
            outfile.close()
                
#%% =============================================
#   Data Process (Computing Domain Mean Values)
#   =============================================
if SWITCH_DP_DM_CALCULATION == True:      
    
    for index_case in range(0,SIZE_CASE):    
   
        print('Processing ' + VARIABLE_STR +' data for case ' + str(CASEID[index_case]))

        # Define variables
        var_avg_dm = np.zeros((SIZE_CYCLE))
        var_std_dm = np.zeros((SIZE_CYCLE))

        for cc in range(0,SIZE_CYCLE):
                
            # Construct the time string
            TIME_STR = YEAR + DATE[math.floor(cc/8)] + HOUR[cc%8]
                          
            # Read pickle files
            infile = open('./data_output/ens_stat_case' + str(CASEID[index_case]) + '_time_' + TIME_STR + '_' + VARIABLE_STR + '.pkl','rb')
            [var_2d_avg, var_2d_std] = pickle.load(infile)
            infile.close() 
            
            var_avg_dm[cc] = np.mean(var_2d_avg)
            var_std_dm[cc] = np.mean(var_2d_std)
            
        # Save data into a pickle file
        outfile = open('./data_output/ens_stat_case' + str(CASEID[index_case]) + '_domain_mean_' + VARIABLE_STR + '.pkl','wb')
        pickle.dump([var_avg_dm,var_std_dm],outfile)
        outfile.close()            
            
#%% =====================================
#   Plotting (Maps)
#   =====================================
if SWITCH_PLT_MAP == True: 
     
    # Getting lon and lat
    fname = CASEDIR[0] + '/' + YEAR + DATE[0] + HOUR[0] + '/mem0001/fcst_fv3lam/' + FILE_TYPE + 'f003.nc'
    ncfile = Dataset(fname)   
    lon = np.squeeze( ncfile.variables['lon'][:])
    lat = np.squeeze( ncfile.variables['lat'][:])
    ncfile.close()     
     
    for index_case in range(0,SIZE_CASE):    
   
        print('Plotting maps for ' + VARIABLE_STR +' data for case ' + str(CASEID[index_case]))

        for cc in range(0,SIZE_CYCLE):    
            
            # Construct the time string
            TIME_STR = YEAR + DATE[math.floor(cc/8)] + HOUR[cc%8]
            print('  - Initialized at ' + TIME_STR)
            
            # Read pickle files
            infile = open('./data_output/ens_stat_case' + str(CASEID[index_case]) + '_time_' + TIME_STR + '_' + VARIABLE_STR + '.pkl','rb')
            [var_2d_avg, var_2d_std] = pickle.load(infile)
            infile.close()             
            
            
            func_plot_map(var_2d_avg,lon,lat,TIME_STR,FIGURE_TITLE,VARIABLE_STR,str(CASEID[index_case]),'Mean')
            func_plot_map(var_2d_std,lon,lat,TIME_STR,FIGURE_TITLE,VARIABLE_STR,str(CASEID[index_case]),'STD')
            
           
#%% ============================================
#   Plotting (Time Series of Domain Mean Values)
#   ============================================
if SWITCH_PLT_TS == True: 
        
    # Define variables
    var_avg_dm_all = np.zeros((SIZE_CASE,SIZE_CYCLE))    
    var_std_dm_all = np.zeros((SIZE_CASE,SIZE_CYCLE)) 
        
    for index_case in range(0,SIZE_CASE):    
   

        # Save data into a pickle file
        infile = open('./data_output/ens_stat_case' + str(CASEID[index_case]) + '_domain_mean_' + VARIABLE_STR + '.pkl','rb')
        [var_avg_dm,var_std_dm] = pickle.load(infile)
        infile.close() 
        
        var_avg_dm_all[index_case,:] = var_avg_dm
        var_std_dm_all[index_case,:] = var_std_dm
        
        
    # Create a figure
    plt.rcParams.update({'font.size': 14})
    fig,axes = plt.subplots(2, 1, figsize=(10,10))   
    
    # subplot 01
    ax1 = plt.subplot(2,1,1)
    ax1.set_position([0.13, 0.57, 0.8, 0.38])
    #plt.xlim(-0.5,24.5)
    
    #if VARIABLE_STR == 'tmp':
    #    plt.ylim(290,299)
    #else:
    #    plt.ylim(0.0094,0.0114)

    plt.plot(np.transpose(var_avg_dm_all))

    plt.grid(True)
    plt.xlabel('Cycles Every 3h From ' + YEAR + DATE[0] + HOUR[0])
    plt.ylabel('Ensemble Mean')
    plt.title(FIGURE_TITLE)
    plt.legend( ('Case ' +str(CASEID[0])+': EFSOI' , 'Case '+str(CASEID[1]) + ': EnKF'  ) )

    # subplot 02
    ax2 = plt.subplot(2,1,2)
    ax2.set_position([0.13, 0.07, 0.8, 0.38])

    plt.plot(np.transpose(var_std_dm_all))
    plt.grid(True)
    plt.xlabel('Cycles Every 3h From ' + YEAR + DATE[0] + HOUR[0])
    plt.ylabel('Ensemble STD')
    #plt.xlim(-0.5,24.5)
    
    #if VARIABLE_STR == 'tmp':
    #    plt.ylim(5,7.5)
    #else:
    #    plt.ylim(0.0042,0.0056)    
        
        
    # save the plot
    plt.savefig('./figures/'+ VARIABLE_STR + '_layer_' + str(NO_LAYER) + '_ens_stat_dm.png',bbox_inches='tight',dpi=100)
    plt.close()       