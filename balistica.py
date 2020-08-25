# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 09:53:19 2020

@author: TOSHIBA 2IN1
"""

import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt

def bala(z,t):
    zp = sp.zeros(4)
    zp[0] = z[2]
    zp[1] = z[3]
    v = z[2:4]
    v[0]=v[0]-V
    v2 = sp.dot(v,v)
    vnorm = sp.sqrt(v2)
    FD = -CD * v2 *(v/vnorm)
    zp[2] = FD[0]/m
    zp[3] = FD[1]/m-g
    
    return zp


cm=0.01
inch=2.54*cm
g=9.81     #m/s^2

#coeficiente de arrastre
ro=1.225      #kg
cd=0.47
D=8.5*inch
r=D/2
A=sp.pi*r**2
CD=0.5*ro*cd*A

#masa
m=15 #kg
#viento

V1= [0.,10.,20.]  #m/s
for V in V1:
    t = sp.linspace(0,30,1001)
    #Parte en el origen

    vi=100*1000./3600. #600 km/h
    z0 = sp.array([0,0,vi,vi,])

    sol = odeint(bala,z0,t)

#funcion a integrar
# z = [x, y, vx, vy]
# dz/dt = bala (z,t)
#        [z2
# dz/dt =[
#        [FD/m  -g

#vector de estado
#z[0]  -> x
#z[1]  -> y
#z[2]  -> vx
#z[3]  -> vy


    x=sol[:,0]
    y=sol[:,1]
    
    plt.ylim(0,50)
    plt.xlim(0,150)
    plt.plot(x,y)

plt.title("Trayectoria para distintos vientos")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.grid(True)
plt.legend(["V = 0 m/s", "V = 10 m/s", "V = 20 m/s"])  
#crea archivo png en carpeta de tu archivo .py
plt.savefig("grafica_bala") #plt.figure() si se quiere tener la gráfica en python
plt.show()
          

    
    
    
    
    
    
    
    
