# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:18:41 2020

@author: TOSHIBA 2IN1
"""
import numpy as np
import scipy as sp
from scipy.integrate import odeint


#datos
G=6.67*(10**(-11))   #Nm^2/Kg^2
mt=5.98*10**24       #Kg
r=7071000            #m
omega = (2*np.pi)/(24*3600)




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

from datetime import datetime

ti = "2020-07-26T22:59:42.000000"
ti = ti.split("T")
ti = "{} {}".format(ti[0], ti[1])
ti = datetime.strptime(ti,"%Y-%m-%d %H:%M:%S.%f")
tf = "2020-07-28T00:59:42.000000"
tf = tf.split("T")
tf = "{} {}".format(tf[0], tf[1])
tf = datetime.strptime(tf,"%Y-%m-%d %H:%M:%S.%f")

deltaT = (tf - ti).total_seconds()


x_i = -1301280.082165
y_i = 1004010.737057
z_i = 6871909.837597
Vx_i = -1690.883903
Vy_i = 7262.526664
Vz_i = -1378.428879

x_f = -2034924.039156
y_f = -5918644.611771
z_f = 3293131.005464
Vx_f = -447.774853
Vy_f = 3813.444330
Vz_f = 6554.348888

t = sp.linspace(0,deltaT,9361)

z0 = sp.array([x_i,y_i,z_i,Vx_i,Vy_i,Vz_i]) #comienzo
sol = odeint(satelite,z0,t)

x=sol[:,0:3]

pos_final = sp.array([x_f,y_f,z_f,Vx_f,Vy_f,Vz_f])- sol[-1]

print ("Intervalo = 1 dia y 2 horas")
print(f"Intervalo en segundos = {deltaT} s")
for el in pos_final:
    print(el, "m")

print ("Según x, y, z, Vx, Vy, Vz respectivamente")


norma = (x_f**2+y_f**2+z_f**2)**(1/2)
norma2 = (sol[-1,0]**2+sol[-1,1]**2+sol[-1,2]**2)**(1/2)
dif = norma-norma2

print (f"La norma es: {dif}, m")



