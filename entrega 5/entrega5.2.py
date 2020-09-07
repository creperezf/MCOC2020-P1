# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:08:21 2020

@author: TOSHIBA 2IN1
"""

import xml
import xml.etree.ElementTree as ET
from numpy import zeros
import datetime as dt
from matplotlib.pylab import *
from scipy.integrate import odeint
import numpy as sp
from time import perf_counter



#leer en consola
#from sys import argv
#eofname = argv(1)
#t, x, y, z, vx, vy, vz = leer_eof(eofname)
def utc2time(utc, ut1, EOF_datetime_format = "%Y-%m-%dT%H:%M:%S.%f"):
    t1 = dt.datetime.strptime(ut1,EOF_datetime_format)
    t2 = dt.datetime.strptime(utc,EOF_datetime_format)
    return (t2 - t1).total_seconds()

def leer_eof(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    
    Data_Block = root.find("Data_Block")
    List_of_OSVs = Data_Block.find("List_of_OSVs")
    
    count = int(List_of_OSVs.attrib["count"])
    
    t = zeros(count)
    x = zeros(count)
    y = zeros(count)
    z = zeros(count)
    vx = zeros(count)
    vy = zeros(count)
    vz = zeros(count)
    
    set_ut1 = False
    for i,osv in enumerate(List_of_OSVs):
        UTC = osv.find("UTC").text[4:]
        x[i] = osv.find("X").text
        y[i] = osv.find("Y").text
        z[i] = osv.find("Z").text
        vx[i] = osv.find("VX").text
        vy[i] = osv.find("VY").text
        vz[i] = osv.find("VZ").text
        
        if not set_ut1:
            ut1 = UTC
            set_ut1= True
        
        t[i] = utc2time(UTC, ut1)
    
    return t, x, y, z, vx, vy, vz
    
t, x, y, z, vx, vy, vz = leer_eof("S1A_OPER_AUX_POEORB_OPOD_20200816T120754_V20200726T225942_20200728T005942.EOF")

#vector de condición inicial
z0 = sp.array([x[0], y[0], z[0], vx[0], vy[0], vz[0]])

#vector de condición inicial
zf = sp.array([x[-1], y[-1], z[-1], vx[-1], vy[-1], vz[-1]])


#datos
G=6.67*(10**(-11))   #Nm^2/Kg^2
mt=5.98*10**24       #Kg
omega = (2*sp.pi)/(24*3600)

def satelite(z,t):
    zp = sp.zeros(6)
    z1 = z[0:3]
    r2 = sp.dot(z1,z1)
    r = sp.sqrt(r2)
    R=sp.array([[sp.cos(omega*t),-sp.sin(omega*t),0],
                [sp.sin(omega*t),sp.cos(omega*t), 0],
                [0.,             0.,              1]])

    dR_dt=sp.array([[-sp.sin(omega*t),-sp.cos(omega*t),0],
                    [sp.cos(omega*t),-sp.sin(omega*t), 0],
                    [0.,            0.,               0.]])*omega

    dR2_dt2=sp.array([[-sp.cos(omega*t),sp.sin(omega*t), 0],
                      [-sp.sin(omega*t),-sp.cos(omega*t),0],
                      [0.,              0.,              0]])*omega**2
    
    
    
    zp[0:3] = z[3:6]
    z2p=(-G*mt/(r**3))*z[0:3]-R.T@(dR2_dt2@z[0:3]+2*dR_dt@z[3:6])
    zp[3:6] = z2p
    return zp

def eulerint(zp,z0,t,Nsub):
    Nt = len(t)
    Ndim = len(z0)
    
    z = sp.zeros((Nt,Ndim))
    z[0,:]=z0[:]
    
    for i in range(1,Nt):
        t_anterior = t[i-1]
        dt = (t[i]-t[i-1])/Nsub
        z_temp = z[i-1,:].copy() #o *1.0
        for k in range(Nsub):
            z_temp+= dt*satelite(z_temp,t_anterior+k*dt)
        z[i,:]=z_temp
          
    return z

z0 = sp.array([x[0], y[0], z[0], vx[0], vy[0], vz[0]])
sol=odeint(satelite,z0,t)
x1=sol[:,0]
y1=sol[:,1]
z1=sol[:,2]

zp=sol[:,:]
t_1=perf_counter()
sol2 = eulerint(zp,z0,t,Nsub=180)
t_2=perf_counter()

tiempo= t_2-t_1

z_euler=sol2[:,0]

x_sol=sol2[:,0]
y_sol=sol2[:,1]
z_sol=sol2[:,2]



difeuler = sp.sqrt((x_sol-x)**2+(y_sol-y)**2+(z_sol-z)**2)
difodeint = sp.sqrt((x1-x)**2+(y1-y)**2+(z1-z)**2)

plot(t/3600,difodeint/1000)
plot(t/3600,difeuler/1000)
print (tiempo)
xlabel("Tiempo, t (horas)")
title("Distancia entre odeint y eulerint subdivisiones = 180")
ylabel("Deriva en Km")
savefig("Gráfica_3_comparación_subdivision=180.png")
