import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

f = open('BACPY.csv','w')
f.write('time,in_blood_alcohol,input_alcohol\n')

# initial time of simulation
t0=0.
t=t0
# Total number of hours to simulate
hsim = 24
# Final time of simulation
tfinal=3600 * hsim
# Integration time-step
dt = 1.
# Initial BAC
a0 = 0.
# Total number of drinks
N  = 12
# Volumes
shot = 25.
half_glass = 50.
cup = 200.
half=284.
bottle = 330.
pint = 473.2
liter = 1000.
# Alcoholic strenght of popular drinks
beer = 0.05
wine = 0.14
whiskey = 0.4
tequila = 0.5
absenta = 0.71
# Alcohol Absortion rate 
man = 0.10
woman = 0.12
Cabsor = man
# Body mass (kg)
M = 92.
# Density of alcohol (g/mL)
D = 0.789
# Amount of blood per unit mass (L/kg)
Cs=0.067
# Alcohol absorption time (it has a dependence with amount and kind of food in stomach) 
tabs= 20*60

# Drink properties : v (drink volume) , g (strenght) 
# ti ("ith" drink start time since init time, in seconds)
# tf ("ith" drink finish time since init time, in seconds)
# twait (Waiting time after finishing ith drink, in seconds)
# tcons (amount of time required to end "ith" drink, equal to tf - ti, in seconds)
v=[]
g=[]
ti=[]
tf=[]

a=[]
b=[]

tcons = 60 * 60
twait = 60 * 60

for i in range(0,N): 
    v.append(cup)
    g.append(wine)
    ti.append(i*(60+tcons+twait))
    tf.append(i*(60+tcons+twait)+tcons)

# Integration of the proposed model
aux=a0
bux=0

for i in range(0,tfinal-1):
    for j in range(0,N):
        st1=1
        st2=1
        if(t-ti[j]-tabs < 0) : st1 = 0
        if(t-tf[j]-tabs < 0) : st2 = 0
        aux=aux+D*v[j]*g[j]*Cabsor/(Cs*M*(tf[j]-ti[j]))*(st1-st2)*dt

        st1=1
        st2=1
        
        if(t-ti[j] < 0): st1 = 0
        if(t-tf[j] < 0): st2 = 0
        bux=bux+D*v[j]*g[j]*Cabsor*1000/(Cs*M*(tf[j]-ti[j]))*(st1-st2)*dt
        
    t=t+dt

    if(aux < 0):
        aux=0
    else: 
        aux=aux-0.12/3600.*dt

    if(aux < 0): 
        a.append(0)
    else:
        a.append(aux)
        
    b.append(bux)   
    if(np.mod(i,10)  == 0):  f.write(str(np.round(t/60,6))+","+str(np.round(a[i],6))+","+str(np.round(b[i],6))+'\n')
    bux=0

f.close()

# Read Exported data as dataframe
at=pd.read_csv('BACPY.csv')

# Smooth the BAC curve
y=at['in_blood_alcohol']
y_smoothed = gaussian_filter1d(y, sigma=100)

# Graph options
plt.rc('xtick', labelsize=18) 
plt.rc('ytick', labelsize=18)

plt.figure(figsize = (15, 8))
plt.xlabel("Time(min)",fontsize=18)
plt.ylabel("as (g/L)",fontsize=18)
plt.title("Prediction of BAC temporal evolution",fontsize=18)
plt.xlim(0,at.loc[at.index[-1], 'time'])
plt.ylim(0,np.max(y)+0.05)

plt.plot(at['time'], y_smoothed,color='black',label='smoothed solution')
plt.plot(at['time'],at['in_blood_alcohol'], color='black', linestyle = '--', label='solution')
plt.plot(at['time'],at['input_alcohol'], color='grey',label='drink input function')

plt.axhline(y = 0.3, color = 'blue', linestyle = '-',label = "Non-Risk zone")
plt.fill_between(at['time'], 0.3, color='blue', alpha=0.25)
plt.axhline(y = 0.8, color = 'green', linestyle = '-',label = "Happy zone")
plt.fill_between(at['time'], 0.3, 0.8, color='green', alpha=0.25)
plt.axhline(y = 1.5, color = 'yellow', linestyle = '-',label = "The Dot")
plt.fill_between(at['time'], 0.8, 1.5, color='yellow', alpha=0.25)
plt.axhline(y = 3.0, color = 'orange', linestyle = '-',label = "drunkenness")
plt.fill_between(at['time'], 1.5, 3.0, color='orange', alpha=0.25)
plt.axhline(y = 5.0, color = 'red', linestyle = '-',label = "Death zone")
plt.fill_between(at['time'], 3.0, 5.0, color='red', alpha=0.25)

plt.legend(loc='upper right',fontsize=18)
plt.savefig("Cogorza_3b.png",dpi=150)
plt.show()
