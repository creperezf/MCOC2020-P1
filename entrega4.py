# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 11:30:26 2020

@author: TOSHIBA 2IN1
"""

from scipy.integrate import odeint
import numpy as np
import scipy as sp
import matplotlib.pylab as plt


#condiciones iniciales
# resolver mx**+cx*+kx=0
x0 = 1
v0 = 1
z0 = [x0,v0]

#datos
m = 1.0 #kg
f = 1.0 #Hz
e = 0.2
w = 2*np.pi*f 
k = m*w**2
c = 2*e*w*m

t = np.linspace(0,4.,100)

def zp(z,t):
    zp = sp.zeros(2)
    zp[0] = z[1]
    z1 = z[0]
    z2 = z[1]
    zp[1]=-(c*z2+k*z1)/m
    return zp


def eulerint(zp,z0,t,Nsub):
    Nt = len(t)
    Ndim = len(np.array(z0))
    
    z = np.zeros((Nt,Ndim))
    z[0,:]=z0
    
    #z(i+1)=zp:i*dt+z_i
    for i in range(1,Nt):
        t_anterior = t[i-1]
        dt = (t[i]-t[i-1])/Nsub
        z_temp = z[i-1,:].copy() #o *1.0
        for k in range(Nsub):
            z_temp+= dt*zp(z_temp,t_anterior+k*dt)
        z[i,:]=z_temp
          
    return z


respuesta_analitica = (np.exp((-c/2)*t))*np.cos(w*t)
plt.plot(t,respuesta_analitica, "k",label="analítica",linewidth=2)

sol = odeint(zp,z0,t)
x=sol[:,0]
plt.plot(t,x,"b",label="odeint")  

sol = eulerint(zp,z0,t,Nsub=1)
z_euler=sol[:,0]
plt.plot(t,z_euler,"g:",label="eulerint subd = 1")

sol = eulerint(zp,z0,t,Nsub=10)
z_euler=sol[:,0]
plt.plot(t,z_euler,"r:",label="eulerint subd = 10")

sol = eulerint(zp,z0,t,Nsub=100)
z_euler=sol[:,0]
plt.plot(t,z_euler,":",color="orange",label="eulerint subd = 100")

plt.legend()
plt.show()
