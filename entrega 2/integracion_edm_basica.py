# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:18:41 2020

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
temp=24*3600


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

ratm=6451000  #m    radio de la atmosfera



theta = np.linspace(0, 2*np.pi, 100) #dibujo el circulo de la atmosfera


a = ratm*np.cos(theta)
b = ratm*np.sin(theta)

figure, axes = plt.subplots(1)

axes.plot(a, b)
axes.set_aspect(1)

plt.plot(x,y)



plt.title("Trayectoria de satelites")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.grid(True)
plt.legend(["atmosfera","V = 7000 m/s"])    

plt.savefig("grafica_satelite")



plt.show()