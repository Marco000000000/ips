import csv
import ctypes
import math
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import requests

import display

o_filename = 'config/mag.txt'


def req(lat, long):
    url = "https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfwmm"
    params = dict(lat1=lat, lon1=long, key='EAU2y', resultFormat='json')
    resp = requests.get(url=url, params=params)
    data = resp.json()
    total_in = data['result']
    ti = (total_in[0]['totalintensity'])
    ti = ti / 1000
    return ti


def calibra(sensor):
    measure_matrix = np.zeros((1, 3), dtype="float")

    # Inserisci nella riga i valori x, y e z letti dal sensore magnetico.
    mag_measurements = sensor.get_mag()
    mx = mag_measurements[0] * 100
    my = mag_measurements[1] * 100
    mz = mag_measurements[2] * 100
    measure_matrix[0][0] = mx
    measure_matrix[0][1] = my
    measure_matrix[0][2] = mz

    return measure_matrix


def asse(nume, a, sensor):
    mm = np.zeros((nume, 3), dtype='float')
    display.scrivi("", "Ruota il sensore", "Lungo l'asse", a, "")
    print("Ruota il sensore lungo l'asse ", a)
    time.sleep(1)

    for i in range(nume):
        mag_measurements = sensor.get_mag()
        mx = mag_measurements[0]
        my = mag_measurements[1]
        mz = mag_measurements[2]
        mx = mx * 100
        my = my * 100
        mz = mz * 100
        c = math.sqrt((mx * mx) + (my * my) + (mz * mz))
        mm[i][0] = mx
        mm[i][1] = my
        mm[i][2] = mz
        # mm[i][3] = c
        tx = "X: {:.3f} µT ".format(mx)
        ty = "Y: {:.3f} µT ".format(my)
        tz = "Z: {:.3f} µT ".format(mz)
        tc = "CM: {:.3f} µT ".format(c)
        display.scrivi(tx, ty, tz, tc, "")
        print(i)
        print(tx)
        print(ty)
        print(tz)
        print(tc)

    return mm


def save(rawData, nume, asse):
    if asse == 'X':
        with open(o_filename, mode='w') as f:
            writer = csv.writer(f, delimiter='\t')
            for i in range(nume):
                writer.writerow([rawData[i][0], rawData[i][1], rawData[i][2]])
        f.close()
    if asse == 'Y' or asse == 'Z':
        with open(o_filename, mode='a') as f:
            writer = csv.writer(f, delimiter='\t')
            for i in range(nume):
                writer.writerow([rawData[i][0], rawData[i][1], rawData[i][2]])
        f.close()
    if asse == 'Z':
        calibrate(nume)


def calibrate(nume):
    # Leggiamo dati prima della calibrazione
    rawData = np.genfromtxt(o_filename, delimiter='\t')
    print(rawData)
    print(type(rawData))
    print(rawData.size)
    with open('config/ti.txt', mode='r') as f:
        ti = float(f.read())
    f.close()
    print(ti)
    func = ctypes.CDLL(os.getcwd() + '/fun.so')
    print(type(func))
    print(func.main(ctypes.c_float(ti)))
    A = np.genfromtxt('config/matrix.txt', delimiter='\t')
    b = np.genfromtxt('config/bias.txt', delimiter='\t')
    N = len(rawData)
    calibData = np.zeros((N, 3), dtype='float')
    for i in range(N):
        currMeas = np.array([rawData[i, 0], rawData[i, 1], rawData[i, 2]])
        calibData[i, :] = A @ (currMeas - b)

    with open("config/cod.txt", mode='w') as f:
        f.write(str('33'))
    f.close()

    p = os.getcwd() + '/static/cali/xy.png'
    try:
        os.remove(p)
    except:
        print('Path is not a file')

    p = os.getcwd() + '/static/cali/xz.png'
    try:
        os.remove(p)
    except:
        print('Path is not a file')

    p = os.getcwd() + '/static/cali/yz.png'
    try:
        os.remove(p)
    except:
        print('Path is not a file')

    p = os.getcwd() + '/static/cali/3d.png'
    try:
        os.remove(p)
    except:
        print('Path is not a file')

    # Plot XY data
    plt.figure()
    plt.plot(rawData[:, 0], rawData[:, 1], 'b*', label='Raw Meas')
    plt.plot(calibData[:, 0], calibData[:, 1], 'r*', label='Calibrated Meas')
    plt.title('XY Magnetometer Data')
    plt.xlabel('X [µT]')
    plt.ylabel('Y [µT]')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    # namefig="xy.png"
    # plt.savefig(namefig)
    namepath = "static/cali/xy.png"
    plt.savefig(namepath)

    # Plot YZ data
    plt.figure()
    plt.plot(rawData[:, 1], rawData[:, 2], 'b*', label='Raw Meas')
    plt.plot(calibData[:, 1], calibData[:, 2], 'r*', label='Calibrated Meas')
    plt.title('YZ Magnetometer Data')
    plt.xlabel('Y [µT]')
    plt.ylabel('Z [µT]')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    # namefig="yz.png"
    # plt.savefig(namefig)
    namepath = "static/cali/yz.png"
    plt.savefig(namepath)

    # Plot XZ data
    plt.figure()
    plt.plot(rawData[:, 0], rawData[:, 2], 'b*', label='Raw Meas')
    plt.plot(calibData[:, 0], calibData[:, 2], 'r*', label='Calibrated Meas')
    plt.title('XZ Magnetometer Data')
    plt.xlabel('X [µT]')
    plt.ylabel('Z [µT]')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    # namefig="xz.png"
    # plt.savefig(namefig)
    namepath = "static/cali/xz.png"
    plt.savefig(namepath)

    # plot 3D
    plt.figure(figsize=(8, 8))
    ax = plt.axes(projection='3d')
    ax.grid
    for i in range(N):
        xs = rawData[i][0]
        ys = rawData[i][1]
        zs = rawData[i][2]
        ax.scatter(xs, ys, zs, marker='o', c='blue', label='Raw Meas')
        xs = calibData[i][0]
        ys = calibData[i][1]
        zs = calibData[i][2]
        ax.scatter(xs, ys, zs, marker='o', c='red', label='Calibrated Meas')
    ax.set_xlabel('X [µT]')
    ax.set_ylabel('Y [µT]')
    ax.set_zlabel('Z [µT]')
    # namefig="3d.png"
    # plt.savefig(namefig)
    namepath = "static/cali/3d.png"
    plt.savefig(namepath)
    # plt.show()
    return 1
