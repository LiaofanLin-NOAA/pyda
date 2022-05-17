'''
Purpose: x
 
Input: JEDI obs NetCDF file

Output: 

History Log:
   2022.05.11: Liaofan Lin - Created
'''

import numpy as np
import sys
from netCDF4 import Dataset

#=====================================================================
if __name__ == '__main__':
 
    # ===============================================
    # General Information
    # ===============================================    
    # Get arguments
    filename = sys.argv[1]    

    print(" ")
    print("===================================================") 
    print("PRINTING GENERAL INFORMATION") 
    print("===================================================") 
    print("--- File Name ---") 
    print(f"  {filename}")
    
    # Read the file
    f = Dataset(filename, mode='r')
    press   = f.variables['air_pressure@MetaData'][:]
    obstype = f.variables['air_temperature@ObsType'][:]
    
    
    # Print All Variables
    print(" ")
    print("--- All Variables ---") 
    for i in f.variables.keys():
        print(f"  {i}")
    
    # Close the file
    f.close()    

    print(" ")
    print("===================================================") 
    print("PRINTING INFORMATION FOR SPECIFIC VARIABLE: air_pressure@MetaData") 
    print("===================================================") 
                
    print("--- The Total Length of the Data ---")
    print("  -> " + str(len(press)))
    
    
    print(" ")
    print("--- Size of Data Under Some Pressure Levels [unit in Pa] ---")   
    press_levels = [    0, 10000, 20000, 30000, 40000, 50000, \
                    60000, 70000, 80000, 90000,100000]
                     
    for i in range(0,len(press_levels)-1):
        
        itemindex = np.where((press > press_levels[i]) & (press <= press_levels[i+1]) )
        press_level_size = len(itemindex[0][:])
        print("  -> From " + str(press_levels[i]) + " to " + str(press_levels[i+1]) + ": " + str(press_level_size) )
        
        
    print(" ")
    print("===================================================") 
    print("PRINTING INFORMATION FOR SPECIFIC VARIABLE: air_temperature@ObsType") 
    print("===================================================")         
    print("--- The Total Length of the Data ---")
    print("  -> " + str(len(obstype)))    
    
    print(" ")
    print("--- Print the Content ---")     
    print(obstype)  
    
        
        
        