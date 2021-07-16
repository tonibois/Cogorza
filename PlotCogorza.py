import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

at=pd.read_csv('BAC.csv')

y=at['in_blood_alcohol']
y_smoothed = gaussian_filter1d(y, sigma=5)

plt.figure(figsize = (15, 8))
plt.xlabel("Tiempo (min)")
plt.ylabel("alcohol en sangre (g/L)")
plt.title("Simulacion del alcohol en sangre (g/L)")

plt.plot(at['time'], y_smoothed)
#plt.plot(at['time'],at['in_blood_alcohol'])
plt.plot(at['time'],at['input_alcohol']*1000)
plt.xlim(0,500)
plt.axhline(y = 0.3, color = 'b', linestyle = '-')
plt.axhline(y = 0.8, color = 'g', linestyle = '-')
plt.axhline(y = 1.5, color = 'y', linestyle = '-')
plt.axhline(y = 3.0, color = 'orange', linestyle = '-')
plt.axhline(y = 5.0, color = 'r', linestyle = '-')
plt.ylim(0,np.max(y)+0.05)
plt.legend()
plt.show()
