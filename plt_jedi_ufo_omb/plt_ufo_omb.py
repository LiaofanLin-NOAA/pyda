'''
Purpose: Plot the hofx from GSI and UFO
         (1) Scatter plots
         (2) Histogram of the difference in hofx between GSI/UFO
         (3) Difference in hofx between GSI/UFO over heights
 
Input: UFO NetCDF files
Output: 
History Log:
   2021      : Shun Liu (https://github.com/ShunLiu-NOAA/plt_ufo_acceptance)
   2022.05.04: Liaofan Lin - Modified
'''

import numpy as np
import sys
import statistics
import math
import matplotlib.pyplot as plt
from netCDF4 import Dataset

def plt_ufo_t(filename,OBSTYPE,VarName):

   # Loading data 
   thisobstype=OBSTYPE
   thisvarname=VarName
   gsihofXBc=thisvarname+'@GsiHofXBc'
   gsihofX  =thisvarname+'@GsiHofX'
   ufohofX  =thisvarname+'@hofx'
   f=Dataset(filename, mode='r')
   gsi_observer_withqc=f.variables[gsihofXBc][:]
   gsi_observer_noqc  =f.variables[gsihofX][:]
   ufo                =f.variables[ufohofX][:]
   geopotential_height=f.variables['height@MetaData'][:]
   f.close()

   #=========================
   # Figure 1: Scatter Plot (GSI vs. UFO)
   plt.rcParams.update({'font.size': 18})

   fig = plt.figure(figsize=(8.0,7.5))
   ax=fig.add_subplot(111)

   plt.scatter(gsi_observer_withqc,ufo, color='blue',label=thisobstype, marker='o', s=3)

   plt.xlabel('gsi')
   plt.ylabel('ufo')
   plt.title(thisobstype+':gsi and ufo hofx scatter')
   figname='ufo_'+thisobstype+'_'+thisvarname+'_scatter_'+subtask+'.png'
   plt.savefig(figname,bbox_inches='tight',dpi=100)
   #=========================

   #=========================
   # Figure 2: Histogram of the difference between GSI/UFO
   diff=gsi_observer_withqc
   diff=diff - ufo
   print(diff)

   rms=float(0)
   for x in diff:
      rms=rms+x*x
      
   rms=math.sqrt(rms/len(diff))
   print("rms=",rms)

   print(diff.max(),diff.min())

   fig1 = plt.figure(figsize=(8.0,7.5))
   ax=fig1.add_subplot(111)

   plt.hist(diff,bins=50,range=(-2.00,2.00))

   plt.xlabel('(gsi-ufo)*1')
   plt.title(thisobstype+':gsi and ufo diff histogram')
   figname='ufo_'+thisobstype+'_'+thisvarname+'_hist_'+subtask+'.png'
   plt.savefig(figname,bbox_inches='tight',dpi=100)
   #=========================

   #=========================
   # Figure 3: Difference between GSI/UFO over heights
   fig2 = plt.figure(figsize=(8.0,7.5))
   ax=fig2.add_subplot(111)
   plt.scatter(diff,geopotential_height, color='b',label="rw", marker='o', s=3)

   plt.xlabel('(gsi-ufo)*1')
   plt.ylabel('geop-height')
   plt.title(thisobstype+':gsi-ufo diff in vertical')
   figname='ufo_'+thisobstype+'_'+thisvarname+'_vdiff_scatter_'+subtask+'.png'
   plt.savefig(figname,bbox_inches='tight',dpi=100)
   #=========================


#=====================================================================
#=====================================================================
if __name__ == '__main__':

   print("start ploting")
   print("ploting gsi hofx v.s. ufo hofx")
   fileame=sys.argv[1]
   OBSTYPE=sys.argv[2]
   VarName=sys.argv[3]
   subtask=sys.argv[4]
   plt_ufo_t(fileame,OBSTYPE,VarName)
   print("ploting done")

