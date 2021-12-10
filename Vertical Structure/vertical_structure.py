import numpy as np
from numpy import *
from math import radians,cos,sin,sqrt,exp
from decimal import *
import matplotlib.pyplot as plt
import datetime
from netCDF4 import Dataset
from netCDF4 import num2date, date2num
import pandas as pd
from matplotlib.cm import get_cmap

#Load NetCDF file and read variables
ncfile = Dataset('60km_idai_ERA5_mesoscale_large.nc','r')
lev=ncfile.variables['lev'][:]
lon = ncfile.variables['lon'][:]
lat = ncfile.variables['lat'][:]
u = ncfile.variables['u'][:,:,:,:]
v = ncfile.variables['v'][:,:,:,:]

#Load track
data=np.loadtxt('idai60km_track_ERA5_mesoscale_large.txt',usecols=(2,3,4))
minlon=data[:,0]
minlat=data[:,1]
maxwind=data[:,2]

#Calculate wind speed
wspd=((u**2)+(v**2))**0.5
lon=np.round(lon,2)
lat=np.round(lat,2)

#Create plot
fig, axes = plt.subplots(figsize=(6,6),nrows=1,ncols=1)

#Create a dataframe to automatically find the timestep of max intensity & the corresponding lat & lon points.
df = pd.DataFrame({'MaxWind':maxwind[:],'CentreLon':minlon[:],'CentreLat':minlat[:]})
maxpoint=(df[['MaxWind']].idxmax())[0]
clat=int((np.where(lat==df.CentreLat[maxpoint]))[0])
clon=int((np.where(lon==df.CentreLon[maxpoint]))[0])

#Assign plot parameters & label locations
deg=int((111*5)/60)
wspd_mi=wspd[maxpoint,:,clat,clon-deg:clon+(deg+1)]
lon_plot=lon[clon-deg:clon+(deg+1)]
actual_lon=lon[clon]
lon_labels=[(actual_lon-4),(actual_lon-3),(actual_lon-2),(actual_lon-1),(actual_lon),(actual_lon+1),(actual_lon+2),(actual_lon+3),(actual_lon+4)]

#Plot
key=np.arange(0,48,4)
m=axes.contourf(lon_plot,lev,wspd_mi,key,cmap=get_cmap("jet"))
axes.invert_yaxis()
axes.set_xticks(lon_labels)
xticks = axes.get_xticks()  
axes.set_xticklabels(['-4','-3','-2','-1','0','1','2','3','4'])

#Add annotation
axes.annotate('60km mesoscale',xy=(0.03,0.95),xycoords='axes fraction',color='white')

#Colourbar settings
cbar = fig.colorbar(m, orientation='vertical', fraction=0.05, pad=0.025)

#Save figure
fig.savefig('Vertical Structure Idai - 60km mesoscale.png', dpi=400, bbox_inches='tight')  
