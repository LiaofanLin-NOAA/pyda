'''
Purpose: x
 
Input: GSI diag NetCDF file

Output: 

History Log:
   2022.05.11: Liaofan Lin - Created
'''

import numpy as np
import sys
from netCDF4 import Dataset


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
    o_type = f.variables['Observation_Type'][:] 
    
    # Print All Variables
    print(" ")
    print("--- All Variables ---") 
    for i in f.variables.keys():
        print(f"  {i}")
    
    # Close the file
    f.close()
    
    # ===============================================
    # Variable Observation_Type
    # ===============================================
    print(" ")
    print("===================================================") 
    print("PRINTING INFORMATION FOR SPECIFIC VARIABLE: Observation_Type") 
    print("===================================================") 
        
    print(" ")
    print("--- Total Length of the Data ---")
    print("  -> " + str(len(o_type)))
    

    
    print(" ")
    print("--- All Available Data Types ---")    
    uniqueValues, indicesList = np.unique(o_type, return_index=True)
    print(f"  -> {uniqueValues}")
    
    print(" ")
    print("--- Size of Each Data Type ---")
    for i in range(0,len(uniqueValues)):
         
        itemindex = np.where(o_type==uniqueValues[i])
        o_type_size = len(itemindex[0][:])
        print("  -> Obs Type " + str(uniqueValues[i]) + ": " + str(o_type_size))
    
    
    
    
    