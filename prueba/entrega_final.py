# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 21:48:25 2020

@author: TOSHIBA 2IN1
"""

import xml
import xml.etree.ElementTree as ET
import datetime as dt
from scipy.integrate import odeint
import numpy as np
from sys import argv

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
    
    t = np.zeros(count)
    x = np.zeros(count)
    y = np.zeros(count)
    z = np.zeros(count)
    vx = np.zeros(count)
    vy = np.zeros(count)
    vz = np.zeros(count)
    
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
    

# Leer en consola
eofname=argv[1]

var_t,var_x,var_y,var_z,var_vx,var_vy,var_vz=leer_eof(eofname)

eof_out=eofname.replace('.EOF','.PRED')
print(f'Archivo de entrada: {eofname}')
print(f'Archivo de salida: {eof_out}')

#Condición Inicial
z0=np.array([var_x[0],var_y[0],var_z[0],var_vx[0],var_vy[0],var_vz[0]])

#Condición Final
zf=np.array([var_x[-1],var_y[-1],var_z[-1],var_vx[-1],var_vy[-1],var_vz[-1]])


Mt= 5.98*10**24       #Kg
G= 6.67*(10**(-11))   #Nm^2/Kg^2
omega= (2*np.pi)/(24*3600)


J2=1.75553e25 #m5 s-2
J3=-2.61913e29 #m6 s-2

def satelite(z,t):
    zp = np.zeros(6)
    z1 = z[0:3]
    r2 = np.dot(z1,z1)
    r = np.sqrt(r2)
    R=np.array([[np.cos(omega*t),-np.sin(omega*t),0],
                [np.sin(omega*t),np.cos(omega*t), 0],
                [0.,             0.,              1]])

    dR_dt=np.array([[-np.sin(omega*t),-np.cos(omega*t),0],
                    [np.cos(omega*t),-np.sin(omega*t), 0],
                    [0.,            0.,               0.]])*omega

    dR2_dt2=np.array([[-np.cos(omega*t),np.sin(omega*t), 0],
                      [-np.sin(omega*t),-np.cos(omega*t),0],
                      [0.,              0.,              0]])*omega**2
    
    
    
    FxJ2 = J2*(z[0]/r**7)* (6*z[2]**2-3/2*(z[0]**2+z[1]**2))
    FyJ2 = J2*(z[1]/r**7)* (6*z[2]**2-3/2*(z[0]**2+z[1]**2))
    FzJ2 = J2*(z[2]/r**7)* (3*z[2]**2-9/2*(z[0]**2+z[1]**2))
    FJ2 = np.array([FxJ2,FyJ2,FzJ2])
    
    FxJ3 = J3*z[0]*z[2]/r**9* (10*z[2]**2-15/2*(z[0]**2+z[1]**2))
    FyJ3 = J3*z[1]*z[2]/r**9* (10*z[2]**2-15/2*(z[0]**2+z[1]**2))
    FzJ3 = J3/r**9* (4*z[2]**2*(z[2]**2-3*(z[0]**2+z[1]**2))+3/2*(z[0]**2+z[1]**2)**2)
    FJ3 = np.array([FxJ3,FyJ3,FzJ3])  
                
    
    zp[0:3] = z[3:6]
    z2p=(-G*Mt/(r**3))*z[0:3]-R.T@(dR2_dt2@z[0:3]+2*dR_dt@z[3:6])+FJ2+FJ3
    zp[3:6] = z2p
    return zp

sol=odeint(satelite,z0,var_t) 
sol_ode=sol[:,:]
t=var_t
x=sol_ode[:,0]
y=sol_ode[:,1]
z=sol_ode[:,2]
vx=sol_ode[:,3]
vy=sol_ode[:,4]
vz=sol_ode[:,5]


with open(eof_out,'w') as fout:
    fout.write('<?xml version="1.0" ?>\n'
'<Earth_Explorer_File>\n'
'  <Earth_Explorer_Header>\n'
'    <Fixed_Header>\n'
'      <File_Name>S1A_OPER_AUX_POEORB_OPOD_20200816T120754_V20200726T225942_20200728T005942</File_Name>\n'
'      <File_Description>Precise Orbit Ephemerides (POE) Orbit File</File_Description>\n'
'      <Notes></Notes>\n'
'      <Mission>Sentinel-1A</Mission>\n'
'      <File_Class>OPER</File_Class>\n'
'      <File_Type>AUX_POEORB</File_Type>\n'
'      <Validity_Period>\n'
'        <Validity_Start>UTC=2020-07-26T22:59:42</Validity_Start>\n'
'        <Validity_Stop>UTC=2020-07-28T00:59:42</Validity_Stop>\n'
'      </Validity_Period>\n'
'      <File_Version>0001</File_Version>\n'
'      <Source>\n'
'        <System>OPOD</System>\n'
'        <Creator>OPOD</Creator>\n'
'        <Creator_Version>0.0</Creator_Version>\n'
'        <Creation_Date>UTC=2020-08-16T12:07:54</Creation_Date>\n'
'      </Source>\n'
'    </Fixed_Header>\n'
'    <Variable_Header>\n'
'      <Ref_Frame>EARTH_FIXED</Ref_Frame>\n'
'      <Time_Reference>UTC</Time_Reference>\n'
'    </Variable_Header>\n'
'  </Earth_Explorer_Header>\n'
'<Data_Block type="xml">\n'
'  <List_of_OSVs count="9361">\n')
    Nt=len(t) 
    for i in range(Nt):
        Dia1 = dt.datetime(2020,7,26,23,00,19,000000)
        Dia2 = dt.datetime(2020,7,26,22,59,42,000000)
        Dia3 = dt.datetime(2020,7,26,22,59,41,787522)
        dias1 = (Dia1 + dt.timedelta(seconds=t[i])).strftime('%Y-%m-%dT%H:%M:%S.%f')
        dias2 = (Dia2 + dt.timedelta(seconds=t[i])).strftime('%Y-%m-%dT%H:%M:%S.%f')
        dias3 = (Dia3 + dt.timedelta(seconds=t[i])).strftime('%Y-%m-%dT%H:%M:%S.%f')
        fout.write('    <OSV>\n'
f'      <TAI>TAI={dias1}</TAI>\n'
f'      <UTC>UTC={dias2}</UTC>\n'
f'      <UT1>UT1={dias3}</UT1>\n'
f'      <Absolute_Orbit>+226632</Absolute_Orbit>\n'
f'      <X unit="m">{x[i]}</X>\n'
f'      <Y unit="m">{y[i]}</Y>\n'
f'      <Z unit="m">{z[i]}</Z>\n'
f'      <VX unit="m/s">{vx[i]}</VX>\n'
f'      <VY unit="m/s">{vy[i]}</VY>\n'
f'      <VZ unit="m/s">{vz[i]}</VZ>\n'
'      <Quality>NOMINAL</Quality>\n'
'    </OSV>\n')

    fout.write('  </List_of_OSVs>\n'
    '</Data_Block>\n'
    '</Earth_Explorer_File>\n')
