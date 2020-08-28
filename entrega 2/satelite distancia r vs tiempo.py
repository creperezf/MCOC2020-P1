# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 18:58:55 2020

@author: TOSHIBA 2IN1
"""

import numpy as np
import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt

#datos
G=6.67*(10**(-11))   #Nm^2/Kg^2
mt=5.98*10**24       #Kg
r=7071000            #m
omega = (2*np.pi)/(24*3600)
temp=3.528*3600


#condiciones iniciales
x=r
y=0
z=0

vx=0 # velocidad en m/s
vy=7000 # m/s
vz=0

t = sp.linspace(0,temp,1001)



def satelite(z,t):
    R=sp.array([[sp.cos(omega*t),-sp.sin(omega*t),0],
                [sp.sin(omega*t),sp.cos(omega*t), 0],
                [0.,             0.,              1]])

    dR_dt=sp.array([[-sp.sin(omega*t),-sp.cos(omega*t),0],
                    [sp.cos(omega*t),-sp.sin(omega*t), 0],
                    [0.,            0.,               0.]])*omega

    dR2_dt2=sp.array([[-sp.cos(omega*t),sp.sin(omega*t), 0],
                      [-sp.sin(omega*t),-sp.cos(omega*t),0],
                      [0.,              0.,              0]])*omega**2
    zp = sp.zeros(6)
    zp[0:3] = z[3:6]
    z2p=(-G*mt/(r**3))*z[0:3]-R.T@(dR2_dt2@z[0:3]+2*dR_dt@z[3:6])
    zp[3:6] = z2p
    return zp




z0 = sp.array([x,y,z,vx,vy,vz]) #comienzo
sol = odeint(satelite,z0,t)

x=sol[:,0]
y=sol[:,1]
z=sol[:,2]


plt.plot(t,x)


plt.title("r(t) de 2 orbitas")

rt=6371000
rtn=-6371000
ro=6451000
ron=-6451000
plt.hlines(y=rt,xmin=0,xmax=13000,color="r")
plt.hlines(y=ro,xmin=0,xmax=13000,color="g")
plt.hlines(y=rtn,xmin=0,xmax=13000,color="r")
plt.hlines(y=ron,xmin=0,xmax=13000,color="g")
plt.ylabel("r (t)")
plt.xlabel("tiempo (s)")
plt.legend(["r (t)","radio tierra","radio orbital"]) 
plt.grid(True)
plt.savefig("r (t) para 2 orbitas.png")




plt.show()