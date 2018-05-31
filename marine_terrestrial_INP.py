'''
Read INP data
'''
import numpy as np
import matplotlib.pyplot as plt
import os
#os.chdir('/Users/jesusvergaratemprado/INP_DATA')
data_terrestrial=np.genfromtxt('TERRESTRIAL_INFLUENCED.dat',delimiter="\t",skip_header=1)
data_marine=np.genfromtxt('MARINE_INFLUENCED.dat',delimiter="\t",skip_header=1)



INP_terrestrial=data_terrestrial[:,2]
temperature_terrestrial=data_terrestrial[:,1]
pressure_terrestrial=data_terrestrial[:,5]
latitude_terrestrial=data_terrestrial[:,3]
longitude_terrestrial=data_terrestrial[:,4]


INP_marine=data_marine[:,2]
temperature_marine=data_marine[:,1]
pressure_marine=data_marine[:,5]
latitude_marine=data_marine[:,3]
longitude_marine=data_marine[:,4]

plt.close()
plt.plot(temperature_terrestrial,INP_terrestrial,'ro',label='Terrestrial')
plt.plot(temperature_marine,INP_marine,'b^',label='Marine')
plt.yscale('log')
plt.grid()
plt.xlabel('Temperature')
plt.ylabel('INP cm-3')
plt.legend()
plt.show()



#tm