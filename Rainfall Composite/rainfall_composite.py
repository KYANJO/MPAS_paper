import numpy as np
from numpy import *
from math import radians,cos,sin,sqrt,exp
from decimal import *
import matplotlib.pyplot as plt
import datetime
from netCDF4 import Dataset
from netCDF4 import num2date, date2num

#---READ IN DATA--------------------------------------------------------------------------------------------------------------------------

#Read in NetCDF file with all data (lon, lat, rainc, rainnc)
file='60km_idai_ERA5_mesoscale_large.nc'
ncfile = Dataset(file,'r')
lon = ncfile.variables['lon'][:]
lat = ncfile.variables['lat'][:]
rainc = ncfile.variables['rainc'][:,:,:]
rainnc = ncfile.variables['rainnc'][:,:,:]
rain=rainc+rainnc #Remember that the actual rainfall is rainc + rainnc

#Read in track
track='idai60km_track_ERA5_mesoscale_large.txt'
data=np.loadtxt(track,usecols=(2,3))
minlon=data[:,0] #centre of the TC (lon)
minlat=data[:,1] #centre of the TC (lat)

#---CREATE PLOT--------------------------------------------------------------------------------------------------------------------------

#Create plot - you can edit the number of rows & columns to add subplots
fig, axes = plt.subplots(figsize=(6,6),nrows=1,ncols=1)

#---SET CONSTANTS / DIMENSIONS / PARAMETERS----------------------------------------------------------------------------------------------

#Getting the data dimensions  
nt = len(rain)
ny = len(rain[0])
nx = len(rain[0][0])

#Indicate the resolution of the model
res=60

#Rounding the NetCDF lats & lons to two decimal places so they match with the tracks
lon=np.round(lon,2)
lat=np.round(lat,2)

#Extracting indices of central lon lat points in rainfall data
lon_idx=[]
lat_idx=[]
for x in range(0,len(minlon)):
  lon_idx.append(int(np.where(lon==minlon[x])[0]))
  lat_idx.append(int(np.where(lat==minlat[x])[0]))

#---CALCULATE RAINFALL-------------------------------------------------------------------------------------------------------------------

#Remember that the MPAS rainfall is cumulative, so if you want the rainfall at the 10th timestep, you say rain[9]-rain[8]

daily_rain=np.empty([(nt-1),ny,nx])
for t in range(0,nt-1):
  daily_rain[t]=rain[t+1]-rain[t]

#Remove first point as the rainfall is zero
lon_idx.pop(0)
lat_idx.pop(0)

#Determine how many rainfall readings we have   
nt=len(lon_idx)
  
#The rainfall plot will show 2.5 degrees either side of the centre of the TC
deg=int((111*2.5)/res)

#Extract the 2.5 degree region around the TC for each timestep
rain_plot=np.empty([nt,(deg*2)+1,(deg*2)+1])
for x in range(0,len(lon_idx)):
  rain_plot[x]=daily_rain[x,lat_idx[x]-deg:lat_idx[x]+(deg+1),lon_idx[x]-deg:lon_idx[x]+(deg+1)]

#Create mesh grid
#Here, the number before the 'j' is equal to (5*111)/resolution. 5 because 2.5 degrees either side = 5 degrees in total
X, Y = np.mgrid[0:1:9j,0:1:9j]

#Now, we average over the time axis.
#Since the data is 6-hourly, we divide by 6 to get the AVERAGE HOURLY RAINFALL  
rain_comp = (np.average(rain_plot,axis=0))/6

#---PLOT --------------------------------------------------------------------------------------------------------------------------------

#Actual Plot
key=np.arange(4,20,2)
m=axes.contourf(Y,X,rain_comp,key,cmap='Blues')
axes.set_xticks([0.1,0.3,0.5,0.7,0.9])
xticks = axes.get_xticks()  
axes.set_xticklabels(['-2','-1','0','1','2'])
axes.set_yticks([0.1,0.3,0.5,0.7,0.9])
yticks = axes.get_yticks()  
axes.set_yticklabels(['-2','-1','0','1','2'])

#Add simulation name
axes.annotate('Idai 60km mesoscale',xy=(0.03,0.95))

#Colorbar settings
cbar = fig.colorbar(m,orientation='vertical', fraction=0.05, pad=0.025)
cbar.set_label('Precipitation (mm/hr)',labelpad=5)

#Save plot
fig.savefig('Rainfall_composite_example.png', dpi=400, bbox_inches='tight')
  
