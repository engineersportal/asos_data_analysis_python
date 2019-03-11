# Python code for introducing numpy and matplotlib
import csv,datetime
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot') # plot styling choice

# acquiring the data from a temperature station
data_array = []
with open('64060KLGA201807.dat','r',newline='') as f:
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        curr_vector = [ii for ii in row[0].split(' ') if ii!='']
        if curr_vector[2]!='NP':
            continue
        data_array.append(curr_vector)
# taking only the time and temperature data
time_vector = [datetime.datetime(int((ii[1])[3:7]),int((ii[1])[7:9]),
                                 int((ii[1])[9:11]),int((ii[1])[11:13]),
                                 int((ii[1])[13:15])) for ii in data_array]
time_hour = [ii.hour for ii in time_vector]
temps = [float(ii[8]) for ii in data_array]

# Calculating hourly statistics with numpy
hourly_avg,hourly_std = [],[]
for hour in range(0,24):
    curr_array = []
    for ii in range(0,len(time_vector)):
        if (time_vector[ii]).hour==hour:
            curr_array.append(temps[ii])
    hourly_avg.append(np.mean(curr_array)) # calculate hourly mean
    hourly_std.append(np.std(curr_array)) # calculate hourly standard deviation

# plotting routing
fig = plt.figure(figsize=(14,8)) #
plt.plot(time_hour,temps,linestyle='',marker='o',zorder=1,
         label='Monthly Scatter') # scatter plot
plt.plot(np.arange(0,24),hourly_avg,label='Hourly Average',
         linewidth=5) # line plot with average
# standard deviation bars
plt.fill_between(np.arange(0,24),np.subtract(hourly_avg,hourly_std),
                 np.add(hourly_avg,hourly_std),label='STDev',
                 color=[130.0/255.0,130.0/255.0,130.0/255.0],
                 alpha=0.35)
plt.plot(np.arange(0,24),np.subtract(hourly_avg,hourly_std),
         linewidth=1,color='k',linestyle='dashed',alpha=0.8) # lower deviation
plt.plot(np.arange(0,24),np.add(hourly_avg,hourly_std),
         linewidth=1,color='k',linestyle='dashed',alpha=0.8) # upper deviation
# styling the plot with labels, limits, and legend
plt.xlabel('Time of Day [Hour]',fontsize=18)
plt.ylabel('Temperature [$^\circ$F]',fontsize=18)
plt.xlim([-0.1,23.1])
plt.ylim([(np.min(hourly_avg)-2.0*np.mean(hourly_std)),
          (2.0*np.mean(hourly_std)+np.max(hourly_avg))])
plt.legend(fontsize=16)
plt.savefig('asos_analysis_python.png',dpi=200)
plt.show()
