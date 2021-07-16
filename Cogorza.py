import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

f = open('BACPY.csv','w')
f.write('time,in_blood_alcohol,input_alcohol\n')

# tiempo inicial
t0=0.
# horas de simulacion
hsim = 24

# tiempo final de simulacion
tfinal=3600 * hsim
#paso de tiempo
dt = 1.
#alcohol inicial en sangre
a0 = 0.
# Numero de consumiciones
N  = 12

lata = 330.
copa = 200.
botella = 750.
botellin = 200.
medio_vaso = 50.
litro = 1000.

cerveza = 0.05
vino = 0.14
whisky = 0.4
hierbas = 0.3
martini = 0.2
absenta = 0.71

# Constante de absorcion de alcohol en funcion del genero del sujeto
hombre = 0.10
mujer = 0.12

Cabsor = hombre
# Masa del sujeto
M = 92
# Densidad del alcohol (g/mL)
D = 0.789
# Cs (Litros de sangre por unidad de masa del sujeto, L/kg)
Cs=0.067

# Tiempo de absorcion del alcohol (entre que se ingiere y que llega a la sangre) --> entre 15 min y 1 hora. Ponemos 20 minutos
tabs= 20*60

# Caracteristicas de las consumiciones : v (volumen bebida) , g (graduacion) 
# ti (tiempo de toma desde inicio simulacion), tf (tiempo en que el sujeto termina de beber)
# tesp (tiempo de espera despues de la bebida i), tconsum (tiempo de consumo, igual a tf - ti)

#for i in range(1,N):
v=[]
g=[]
ti=[]
tf=[]
tesp=[]
a=[]
t=[]
b=[]


v.append(lata)
g.append(cerveza)
ti.append(0*60)
tf.append(30*60)

v.append(lata)
g.append(cerveza)
ti.append(60*60)
tf.append(80*60)

v.append(lata)
g.append(cerveza)
ti.append(120*60)
tf.append(140*60)

v.append(lata)
g.append(cerveza)
ti.append(160*60)
tf.append(200*60)

v.append(lata)
g.append(cerveza)
ti.append(210*60)
tf.append(225*60)

v.append(lata)
g.append(cerveza)
ti.append(260*60)
tf.append(280*60)

v.append(lata)
g.append(cerveza)
ti.append(300*60)
tf.append(330*60)

v.append(lata)
g.append(cerveza)
ti.append(335*60)
tf.append(380*60)

v.append(lata)
g.append(cerveza)
ti.append(440*60)
tf.append(500*60)

v.append(lata)
g.append(cerveza)
ti.append(510*60)
tf.append(520*60)

v.append(lata)
g.append(cerveza)
ti.append(540*60)
tf.append(560*60)

v.append(lata)
g.append(cerveza)
ti.append(570*60)
tf.append(600*60)
#    tesp.append(5.*60)

a.append(a0)
t=t0
b.append(0)
aux=a0
bux=0

for i in range(0,tfinal-1):
    for j in range(0,N-1):
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
#    if(np.mod(i,1000)== 0):  print(t,a[i],b[i])
    if(np.mod(i,10)  == 0):  f.write(str(np.round(t/60,6))+","+str(np.round(a[i],6))+","+str(np.round(b[i],6))+'\n')
    bux=0

f.close()


at=pd.read_csv('BACPY.csv')

y=at['in_blood_alcohol']
y_smoothed = gaussian_filter1d(y, sigma=100)

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

plt.axhline(y = 3.0, color = 'orange', linestyle = '-',label = "Cogorza")
plt.fill_between(at['time'], 1.5, 3.0, color='orange', alpha=0.25)

plt.axhline(y = 5.0, color = 'red', linestyle = '-',label = "Riesgo de Muerte")
plt.fill_between(at['time'], 3.0, 5.0, color='red', alpha=0.25)

plt.ylim(0,np.max(y)+0.05)
plt.legend()
plt.savefig("Cogorza_12cons_py.png",dpi=200)
plt.show()
