# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 20:00:51 2020

@author: TOSHIBA 2IN1
"""

import xml
import xml.etree.ElementTree as ET
from numpy import zeros
import datetime as dt
from matplotlib.pylab import *
from scipy.integrate import odeint
import numpy as np
import scipy as sp



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
z0 = array([x[0], y[0], z[0], vx[0], vy[0], vz[0]])

#vector de condición inicial
zf = array([x[-1], y[-1], z[-1], vx[-1], vy[-1], vz[-1]])


#datos
G=6.67*(10**(-11))   #Nm^2/Kg^2
mt=5.98*10**24       #Kg
omega = (2*np.pi)/(24*3600)
J2 = 1.75553*(10**10)*1000**5
J3 = -2.61913*(10**11)*1000**6

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
    
    
    
    FxJ2 = J2*(z[0]/r**7)* (6*z[2]**2-3/2*(z[0]**2+z[1]**2))
    FyJ2 = J2*(z[1]/r**7)* (6*z[2]**2-3/2*(z[0]**2+z[1]**2))
    FzJ2 = J2*(z[2]/r**7)* (3*z[2]**2-9/2*(z[0]**2+z[1]**2))
    FJ2 = sp.array([FxJ2,FyJ2,FzJ2])
    
    FxJ3 = J3*z[0]*z[2]/r**9* (10*z[2]**2-15/2*(z[0]**2+z[1]**2))
    FyJ3 = J3*z[1]*z[2]/r**9* (10*z[2]**2-15/2*(z[0]**2+z[1]**2))
    FzJ3 = J3/r**9* (4*z[2]**2*(z[2]**2-3*(z[0]**2+z[1]**2))+3/2*(z[0]**2+z[1]**2)**2)
    FJ3 = sp.array([FxJ3,FyJ3,FzJ3])  
                
    
    zp[0:3] = z[3:6]
    z2p=(-G*mt/(r**3))*z[0:3]-R.T@(dR2_dt2@z[0:3]+2*dR_dt@z[3:6])+FJ2[0:3]+FJ3[0:3]
    zp[3:6] = z2p
    return zp

sol=odeint(satelite,z0,t)

x_sol=sol[:,0]
y_sol=sol[:,1]
z_sol=sol[:,2]

y1=[-5e6,0,5e6]
ejey=["-5000","0","5000"]
x1=[0,18000,36000,54000,72000,90000]
ejex=["0","5","10","15","20","25"]


figure()
subplot(3,1,1)
yticks(y1,ejey)
xticks(x1,ejex)
title("Posición")
ylabel("X (Km)")
plot(t,x)
plot(t,x_sol)
subplot(3,1,2)
yticks(y1,ejey)
xticks(x1,ejex)
ylabel("Y (Km)")
plot(t,y)
plot(t,y_sol)
subplot(3,1,3)
yticks(y1,ejey)
xticks(x1,ejex)
ylabel("Z (Km)")
xlabel("Tiempo, t (horas)")
plot(t,z)
plot(t,z_sol)
tight_layout()
savefig("Gráfica_2_con_perfeccionar.png")