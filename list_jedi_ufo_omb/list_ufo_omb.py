'''
Purpose: Print out list information, if there is a difference (given a threshold) 
         in hofx between GSI and UFO.
 
Input: UFO NetCDF files

Output: 

History Log:
   2021      : Ming Hu or Shun Liu or someone else?
   2022.05.04: Liaofan Lin - Modified
'''

import numpy as np
import sys
import statistics
import math
import matplotlib.pyplot as plt
from netCDF4 import Dataset


def list_ufo_var(filename,OBSTYPE,VarName):

   thisobstype = OBSTYPE
   thisvarname = VarName
   gsihofXBc   = thisvarname+'@GsiHofXBc'
   gsihofX     = thisvarname+'@GsiHofX'
   ufohofX     = thisvarname+'@hofx'
   obstype     = thisvarname+'@ObsType'
   useflag     = thisvarname+'@GsiUseFlag'
   f = Dataset(filename, mode='r')
   gsi_observer_withqc = f.variables[gsihofXBc][:]
   gsi_observer_noqc   = f.variables[gsihofX][:]
   ufo                 = f.variables[ufohofX][:]
   geopotential_height = f.variables['height@MetaData'][:]
   lat                 = f.variables['latitude@MetaData'][:]
   lon                 = f.variables['longitude@MetaData'][:]
   otype               = f.variables[obstype][:]
   oflag               = f.variables[useflag][:]
   oele                = f.variables['station_elevation@MetaData'][:]
   sid                 = f.variables['station_id@MetaData'][:,:]
   f.close()

   diff = gsi_observer_noqc - ufo
   print("Numbers of hofx Difference Between GSI and UFO: " + str(len(diff)))

   for n in range(0, len(diff)):
      if abs(diff[n]) > 0.0005:
        print("n=",n," SID={}".format(sid[n][0:7])," diff=",diff[n], " ufo=", ufo[n], " gsi=",gsi_observer_noqc[n],
              "lat=",lat[n]," lon=",lon[n], " otype=", otype[n], " oflag=",oflag[n],
              " height=",geopotential_height[n]," oele=",oele[n])

#=====================================================================
if __name__ == '__main__':

   filename = sys.argv[1]
   OBSTYPE  = sys.argv[2]
   VarName  = sys.argv[3]
   subtask  = sys.argv[4]
   
   print("listing gsi hofx v.s. ufo hofx, for")
   print("  - File:" + filename)
   print("  - ObsYype:" + OBSTYPE)
   print("  - Variable: " + VarName)
   
   list_ufo_var(filename,OBSTYPE,VarName)
   
   print("listing done ")
   print("===========================")
