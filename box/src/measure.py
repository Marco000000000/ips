import math

import melopero_lsm9ds1 as mp
import numpy as np

import display


# sensore
# sensor = mp.LSM9DS1()
# sensor.use_i2c()

def set_sensor_odr(sensor, odr):
    if odr == 0.625:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_0_625Hz)
    elif odr == 1.25:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_1_25Hz)
    elif odr == 2.5:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_2_5Hz)
    elif odr == 5:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_5Hz)
    elif odr == 10:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_10Hz)
    elif odr == 20:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_20Hz)
    elif odr == 40:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_40Hz)
    else:
        sensor.set_mag_odr(mp.LSM9DS1.MAG_ODR_80Hz)


def singola(sensor):
    try:
        A = np.genfromtxt('confimatrix.txt', delimiter='\t')
        b = np.genfromtxt('config/bias.txt', delimiter='\t')
        date = np.zeros((0, 3))
        mag_measurements = sensor.get_mag()
        mx = mag_measurements[0]
        my = mag_measurements[1]
        mz = mag_measurements[2]
        mx = mx * 100
        my = my * 100
        mz = mz * 100
        c = math.sqrt((mx * mx) + (my * my) + (mz * mz))
        currMeas = np.array([mx, my, mz])
        print(currMeas)
        currMeas = A @ (currMeas - b)
        print('Calibrate: ')
        print(currMeas)
        mx = currMeas[0]
        my = currMeas[1]
        mz = currMeas[2]
        c = math.sqrt((mx * mx) + (my * my) + (mz * mz))
        # np.array(mx, my, mz)
        date = np.append(date, [currMeas], axis=0)
        tx = "X: {:.3f} µT ".format(mx)
        ty = "Y: {:.3f} µT ".format(my)
        tz = "Z: {:.3f} µT ".format(mz)
        tc = "CM: {:.3f} µT ".format(c)
        display.scrivi(tx, ty, tz, tc, "")
        return mx, my, mz, c
    except OSError as e:
        print("Dispositivo mai calibrato")


def multi(sensor, num):
    try:
        A = np.genfromtxt('config/matrix.txt', delimiter='\t')
        b = np.genfromtxt('config/bias.txt', delimiter='\t')
        date = np.zeros((0, 3))
        for k in range(num):
            mag_measurements = sensor.get_mag()
            mx = mag_measurements[0]
            my = mag_measurements[1]
            mz = mag_measurements[2]
            mx = mx * 100
            my = my * 100
            mz = mz * 100
            currMeas = np.array([mx, my, mz])
            # print(currMeas)
            currMeas = A @ (currMeas - b)
            # print('Calibrate: ')
            # print(currMeas)
            date = np.append(date, [currMeas], axis=0)
    except OSError as e:
        print("Dispositivo mai calibrato")
    # print(date)
    mdate = np.mean(date, axis=0)
    # print (mdate)
    mx = mdate[0]
    my = mdate[1]
    mz = mdate[2]
    c = math.sqrt((mx * mx) + (my * my) + (mz * mz))
    tx = "X: {:.3f} µT ".format(mx)
    ty = "Y: {:.3f} µT ".format(my)
    tz = "Z: {:.3f} µT ".format(mz)
    tc = "CM: {:.3f} µT ".format(c)
    display.scrivi(tx, ty, tz, tc, "")
    return mx, my, mz, c
