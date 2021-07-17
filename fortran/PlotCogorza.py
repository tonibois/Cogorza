import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

at=pd.read_csv('BAC.csv')

y=at['in_blood_alcohol']
y_smoothed = gaussian_filter1d(y, sigma=50)

plt.figure(figsize = (15, 8))
plt.xlabel("Tiempo (min)")
plt.ylabel("alcohol en sangre (g/L)")
plt.title("Simulacion del alcohol en sangre (g/L)")

plt.plot(at['time'], y_smoothed,color='black',label='simulacion suavizada')
plt.plot(at['time'],at['in_blood_alcohol'], color='black', linestyle = '--', label='simulacion original')
plt.plot(at['time'],at['input_alcohol'], color='grey',label='consumiciones')
plt.xlim(0,at.loc[at.index[-1], 'time'])
plt.axhline(y = 0.3, color = 'blue', linestyle = '-',label = "Zona sin riesgo")
plt.fill_between(at['time'], 0.3, color='blue', alpha=0.25)

plt.axhline(y = 0.8, color = 'green', linestyle = '-',label = "Zona alegre")
plt.fill_between(at['time'], 0.3, 0.8, color='green', alpha=0.25)

plt.axhline(y = 1.5, color = 'yellow', linestyle = '-',label = "El puntillo")
plt.fill_between(at['time'], 0.8, 1.5, color='yellow', alpha=0.25)

plt.axhline(y = 3.0, color = 'orange', linestyle = '-',label = "Cogorza del copon")
plt.fill_between(at['time'], 1.5, 3.0, color='orange', alpha=0.25)

plt.axhline(y = 5.0, color = 'red', linestyle = '-',label = "Riesgo de Muerte")
plt.fill_between(at['time'], 3.0, 5.0, color='red', alpha=0.25)

plt.ylim(0,np.max(y)+0.05)
plt.legend()
plt.savefig("Cogorza_12cons.png",dpi=200)
plt.show()
