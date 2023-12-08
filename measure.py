import matplotlib.pyplot as plt
import numpy as np
import calendar
import time
import math
from PIL import Image
import melopero_lsm9ds1 as mp
import csv
import display

#sensore
#sensor = mp.LSM9DS1()
#sensor.use_i2c()

def singola(sensor):           
    try:
        A = np.genfromtxt('matrix.txt', delimiter='\t')
        b = np.genfromtxt('bias.txt', delimiter='\t')
        date = np.zeros((0,3))
        mag_measurements = sensor.get_mag()
        mx=mag_measurements[0]
        my=mag_measurements[1]
        mz=mag_measurements[2]
        mx= mx*100
        my= my*100
        mz= mz*100
        c = math.sqrt((mx*mx)+(my*my)+(mz*mz))
        currMeas = np.array([mx,my,mz])
        print(currMeas)
        currMeas = A @ (currMeas - b)
        print('Calibrate: ')
        print(currMeas)
        mx= currMeas[0]
        my= currMeas[1]
        mz= currMeas[2]
        c = math.sqrt((mx*mx)+(my*my)+(mz*mz))
        #np.array(mx, my, mz)
        date=np.append(date, [currMeas], axis=0)
        tx="X: {:.3f} µT ".format(mx)
        ty="Y: {:.3f} µT ".format(my)
        tz="Z: {:.3f} µT ".format(mz)
        tc="CM: {:.3f} µT ".format(c)
        display.scrivi(tx,ty,tz,tc,"")
        return mx, my, mz, c
    except OSError as e:
        print("Dispositivo mai calibrato")
        
        
def multi(sensor, num):           
    try:
        A = np.genfromtxt('matrix.txt', delimiter='\t')
        b = np.genfromtxt('bias.txt', delimiter='\t')
        date = np.zeros((0,3))
        for k in range (num):
            mag_measurements = sensor.get_mag()
            mx=mag_measurements[0]
            my=mag_measurements[1]
            mz=mag_measurements[2]
            mx= mx*100
            my= my*100
            mz= mz*100
            currMeas = np.array([mx,my,mz])
            #print(currMeas)
            currMeas = A @ (currMeas - b)
            #print('Calibrate: ')
            #print(currMeas)
            date=np.append(date, [currMeas], axis=0)
    except OSError as e:
        print("Dispositivo mai calibrato")
    #print(date)
    mdate = np.mean(date, axis=0)
    #print (mdate)
    mx= mdate[0]
    my= mdate[1]
    mz= mdate[2]
    c = math.sqrt((mx*mx)+(my*my)+(mz*mz))
    tx="X: {:.3f} µT ".format(mx)
    ty="Y: {:.3f} µT ".format(my)
    tz="Z: {:.3f} µT ".format(mz)
    tc="CM: {:.3f} µT ".format(c)
    display.scrivi(tx,ty,tz,tc,"")
    return mx, my, mz, c
    