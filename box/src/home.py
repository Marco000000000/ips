import ast
import calendar
import csv
import ctypes
import os
import random
import shutil
import socket
import string
import threading
import time
import uuid
from datetime import datetime
from os.path import join, dirname, realpath

import matplotlib
import matplotlib.pyplot as plt
import melopero_lsm9ds1 as mp
import numpy as np
import pandas as pd
from PIL import Image
from flask import Flask, render_template, request, session, jsonify, send_file
from flask_sslify import SSLify
from werkzeug.utils import secure_filename

import ble
import cal
import configf
import dati
import display
import heatmap
import measure
import sincro
import wifis

matplotlib.use("Agg")


def randStr(chars=string.ascii_uppercase + string.digits, N=12):
    return ''.join(random.choice(chars) for _ in range(N))


iip = "0.0.0.0"

# sensore
sensor = mp.LSM9DS1()
sensor.use_i2c()

# Upload Mappe
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
upl_dir = "/static/uploads/"
data_dir = "/static/data/"
# UPLOAD_FOLDER = os.path.join('/static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SSL_CONTEXT'] = ('cert.pem', 'priv_key.pem')
sslify = SSLify(app)

# Calibrazione
nume = 0

# Define secret key to enable session
app.secret_key = randStr(chars='abcdefghijklmnopqrstuvwyxz123456789')

g_stop_calibration_requested = None

calibration_raw_data_output_filename = "mag.txt"
calibration_calibrated_data_output_filename = "calibration_calibrated_data.txt"


@app.route("/")
@app.route("/index")
def index():
    prnt()
    return render_template('/index.html')


@app.route("/config")
def configtemp():
    prnt()
    return render_template('/config.html')


@app.route("/live")
def live():
    return render_template('/live.html')


@app.route("/daticonfig")
def daticoonfig():
    global g_box_config

    config_data = {"colormap": g_box_config.magnetic_map_color, "inter": g_box_config.magnetic_map_interpolation,
                   "odr": g_box_config.output_data_rate, "ble": g_box_config.bluetooth_scan_time,
                   "server": g_box_config.server_ip, "port": g_box_config.server_port, "cali": 20}

    return jsonify(config_data)

    # jc = configf.load_conf()  # return jsonify(jc)


@app.route("/config", methods=("POST", "GET"))
def config():
    prnt()
    if request.method == 'POST':
        config_data = request.json

        global g_box_config

        g_box_config.set_output_data_rate(float(config_data["odr"]))
        g_box_config.set_bluetooth_scan_time(float(config_data["ble"]))
        g_box_config.set_magnetic_map_interpolation(config_data["inter"])
        g_box_config.set_magnetic_map_color(config_data["colormap"])
        g_box_config.set_server_ip(config_data["server"])
        g_box_config.set_server_port(int(config_data["port"]))

        g_box_config.save()

        measure.set_sensor_odr(sensor, g_box_config.output_data_rate)

    return ("ok")


@app.route("/sm")
def sm():
    if request.method == 'GET':
        k = request.args.get('k')
    x, y, z, c = measure.singola(sensor)
    if k == 'b':
        return render_template('/sm.html', x="{:.3f}".format(x), y="{:.3f}".format(y), z="{:.3f}".format(z),
                               c="{:.3f}".format(c))
    else:
        return jsonify(
            {"x": "{:.3f}".format(x), "y": "{:.3f}".format(y), "z": "{:.3f}".format(z), "c": "{:.3f}".format(c)})


@app.route("/termina_calibrazione")
def termina_calibrazione():
    global g_stop_calibration_requested
    g_stop_calibration_requested = True
    prnt()

    return "Calibrazione terminata"


@app.route("/nuova_calibrazione")
def show_nuova_calibrazione():
    prnt()
    return render_template('/nuova_calibrazione.html')


@app.route("/nuova_calibrazione", methods=["POST"])
def nuova_calibrazione():
    global g_stop_calibration_requested
    if g_stop_calibration_requested is None:
        g_stop_calibration_requested = True

    if not g_stop_calibration_requested:
        return "Calibrazione già avviata: continuare a ruotare il dispositivo..."
    prnt()
    # Dati in formato json mandati dal client. Contengono:
    #   - ti:   total intensity, acquisita grazie alla richiesta effettuata dal client al sito governativo subito
    #           prima di richiedere "/nuova_calibrazione". Verrà usata per il calcolo di A e b ai fini della calibrazione.
    #
    #   - sample_frequency: Frequenza con cui il sensore magnetico deve campionare durante l'acquisizone dei dati.
    request_data = request.json

    total_intensity = float(request_data['ti'])
    sample_frequency = float(request_data["sample-frequency"])

    g_stop_calibration_requested = False

    calibration_thread = threading.Thread(target=nuova_calibrazione_thread_func,
                                          args=(total_intensity, sample_frequency,))
    calibration_thread.start()

    return "Calibrazione avviata: ruotare il dispositivo..."


def nuova_calibrazione_thread_func(total_intensity, sample_frequency):
    global g_stop_calibration_requested

    # Matrice fatta da N righe e 3 colonne. N rappresenta il numero di campioni presi dall'utente
    # durante il processo di acquisizone. Le tre colonne rappresentano le tre componenti del campo magnetico letto
    # dal sensore.
    raw_data = np.zeros((0, 3), dtype="float")

    # Limita il valore di frequenza ricevuto dal client tra 1 e 50.
    sample_frequency = np.clip(sample_frequency, 1, 50)

    # Ogni quanti secondi campionare dal sensore
    periodo = 1.0 / sample_frequency

    while not g_stop_calibration_requested:
        single_measure = np.zeros((1, 3), dtype="float")

        # Inserisci nella riga i valori x, y e z letti dal sensore magnetico.
        mag_measurements = sensor.get_mag()
        mx = mag_measurements[0] * 100
        my = mag_measurements[1] * 100
        mz = mag_measurements[2] * 100
        single_measure[0][0] = mx
        single_measure[0][1] = my
        single_measure[0][2] = mz

        raw_data = np.append(raw_data, single_measure, axis=0)

        time.sleep(periodo)

    # N è il numero di campioni letti durante l'acquisizione
    N = len(raw_data)

    # Scrivi raw_data dentro il file 'mag.txt'. Verrà usato per il calcolo della matrice A e del bias.
    with open(calibration_raw_data_output_filename, mode='w') as f:
        writer = csv.writer(f, delimiter='\t')
        for i in range(N):
            writer.writerow([raw_data[i][0], raw_data[i][1], raw_data[i][2]])

    # Invoca la funzione 'main' dentro la libreria fun.so per il calcolo di A e b, passandogli
    # la total intensity acquisita precedentemnte dal client.
    # Inoltre, la funzione leggerà il file mag.txt contenente le misure contenute in raw_data.
    # Con queste informazioni, la funzione 'main' calcolerà A e b e le scriverà, rispettivamente,
    # nei file 'matrix.txt' e 'bias.txt'.
    func = ctypes.CDLL(os.getcwd() + '/fun.so')
    func.main(ctypes.c_float(total_intensity))

    # Leggi A e b dai rispettivi file
    A = np.genfromtxt('matrix.txt', delimiter='\t')
    b = np.genfromtxt('bias.txt', delimiter='\t')

    # Dopo aver acquisito i dati grezzi in 'raw_data', usa A e b per calibrare
    calibrated_data = np.zeros((N, 3), dtype='float')
    for i in range(N):
        curr_meas = np.array([raw_data[i, 0], raw_data[i, 1], raw_data[i, 2]])
        calibrated_data[i, :] = A @ (curr_meas - b)

    with open(calibration_calibrated_data_output_filename, mode='w') as f:
        writer = csv.writer(f, delimiter='\t')
        for i in range(N):
            writer.writerow([calibrated_data[i][0], calibrated_data[i][1], calibrated_data[i][2]])


@app.route("/view_calibration_plot", methods=["POST"])
def view_calibration_plot():
    request_data = request.json

    plot_type = request_data["plot_type"]

    raw_data = np.genfromtxt(calibration_raw_data_output_filename, delimiter='\t')
    calibrated_data = np.genfromtxt(calibration_calibrated_data_output_filename, delimiter='\t')

    # Root directory in cui salvare i plot della calibrazione
    plot_root_dir = os.getcwd() + "/static/calibration"
    xy_plane_filepath = plot_root_dir + "/xy.png"
    yz_plane_filepath = plot_root_dir + "/yz.png"
    xz_plane_filepath = plot_root_dir + "/xz.png"
    three_dim_plot_filepath = plot_root_dir + "/3d.png"

    N = len(raw_data)

    if not os.path.exists(plot_root_dir):
        os.makedirs(plot_root_dir)

    if plot_type == "3d":
        # Plot 3D Data
        plt.figure(figsize=(8, 8))
        ax = plt.axes(projection='3d')
        ax.grid
        for i in range(N):
            xs = raw_data[i][0]
            ys = raw_data[i][1]
            zs = raw_data[i][2]
            ax.scatter(xs, ys, zs, marker='o', c='blue', label='Raw Measurments')
            xs = calibrated_data[i][0]
            ys = calibrated_data[i][1]
            zs = calibrated_data[i][2]
            ax.scatter(xs, ys, zs, marker='o', c='red', label='Calibrated Measurments')
        ax.set_xlabel('X [µT]')
        ax.set_ylabel('Y [µT]')
        ax.set_zlabel('Z [µT]')
        plt.savefig(three_dim_plot_filepath)

        return send_file(three_dim_plot_filepath)

    elif plot_type == "xy":
        # Plot XY data
        plt.figure()
        plt.plot(raw_data[:, 0], raw_data[:, 1], 'b*', label='Raw Measurments')
        plt.plot(calibrated_data[:, 0], calibrated_data[:, 1], 'r*', label='Calibrated Measurments')
        plt.title('XY Magnetometer Data')
        plt.xlabel('X [µT]')
        plt.ylabel('Y [µT]')
        plt.legend()
        plt.grid()
        plt.axis('equal')
        plt.savefig(xy_plane_filepath)

        return send_file(xy_plane_filepath)

    elif plot_type == "yz":
        # Plot YZ data
        plt.figure()
        plt.plot(raw_data[:, 1], raw_data[:, 2], 'b*', label='Raw Measurments')
        plt.plot(calibrated_data[:, 1], calibrated_data[:, 2], 'r*', label='Calibrated Measurments')
        plt.title('YZ Magnetometer Data')
        plt.xlabel('Y [µT]')
        plt.ylabel('Z [µT]')
        plt.legend()
        plt.grid()
        plt.axis('equal')
        plt.savefig(yz_plane_filepath)

        return send_file(yz_plane_filepath)

    elif plot_type == "xz":
        # Plot XZ data
        plt.figure()
        plt.plot(raw_data[:, 0], raw_data[:, 2], 'b*', label='Raw Measurments')
        plt.plot(calibrated_data[:, 0], calibrated_data[:, 2], 'r*', label='Calibrated Measurments')
        plt.title('XZ Magnetometer Data')
        plt.xlabel('X [µT]')
        plt.ylabel('Z [µT]')
        plt.legend()
        plt.grid()
        plt.axis('equal')
        plt.savefig(xz_plane_filepath)

        return send_file(xz_plane_filepath)

    return ""


@app.route("/cali")
def cali():
    prnt()
    return render_template('/cali.html')


@app.route("/cali", methods=("POST", "GET"))
def calibra():
    if request.method == 'POST':
        datare = request.json
        k = datare['k']
        cod = int(datare['cod'])
        ti = float(datare['ti'])
        # if(k=='b'):
        if (cod == 0):
            with open('cod.txt', mode='r') as f:
                codn = int(f.read())
            f.close()
            if codn != 0:
                print("Calibrazione già in corso")
                return jsonify({"codi": -22, "mess": "Calibrazione già in corso"})
            if (ti != -9):
                with open("ti.txt", mode='w') as f:
                    f.write(str(ti))
                f.close()
            with open("cod.txt", mode='w') as f:
                f.write(str('1'))
            f.close()
            x = threading.Thread(target=ta, args=(nume,))
            x.start()
            return jsonify({"codi": 1})
        elif (cod == 33):
            with open("cod.txt", mode='w') as f:
                f.write(str('0'))
            f.close()
            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)
            nf = str(time_stamp)
            prnt()
            finalresponse = {"codi": -14, "s": nf, "statuscalibration": "ok"}
            return jsonify(finalresponse)
        elif (cod == -11):
            with open("cod.txt", mode='w') as f:
                f.write(str('0'))
            f.close()
            try:
                x.terminate()
            except:
                print("Thread non trovato!")
            return jsonify({"codi": 0})
        else:
            with open('cod.txt', mode='r') as f:
                codn = int(f.read())
            f.close()
            return jsonify({"codi": codn})


def ta(nume):
    rawData = np.zeros((0, 3), dtype='float')
    print(rawData)
    # if asse == 'X':
    rawData = np.append(rawData, cal.asse(nume, '1', sensor), axis=0)
    with open('cod.txt', mode='r') as f:
        codn = int(f.read())
    f.close()
    print(codn)
    if codn != 1:
        print("Annulla........")
        # time.sleep(1.5)
        return -1
    cal.save(rawData, nume, 'X')
    with open("cod.txt", mode='w') as f:
        f.write(str('10'))
    f.close()
    time.sleep(1)
    with open("cod.txt", mode='w') as f:
        f.write(str('2'))
    f.close()
    rawData = np.append(rawData, cal.asse(nume, '2', sensor), axis=0)
    with open('cod.txt', mode='r') as f:
        codn = int(f.read())
    f.close()
    print(codn)
    if codn != 2:
        print("Annulla........")
        # time.sleep(1.5)
        return -1
    cal.save(rawData, nume, 'Y')
    with open("cod.txt", mode='w') as f:
        f.write(str('20'))
    f.close()
    time.sleep(1)
    with open("cod.txt", mode='w') as f:
        f.write(str('3'))
    f.close()
    rawData = np.append(rawData, cal.asse(nume, '3', sensor), axis=0)
    with open('cod.txt', mode='r') as f:
        codn = int(f.read())
    f.close()
    print(codn)
    if codn != 3:
        print("Annulla........")
        # time.sleep(1.5)
        return -1
    with open("cod.txt", mode='w') as f:
        f.write(str('30'))
    f.close()
    cal.save(rawData, nume,
             'Z')  # with open("cod.txt", mode='w') as f:  #    f.write(str('33'))  # f.close()  # time.sleep(1)


def vta(nume, asse):
    rawData = np.zeros((0, 3), dtype='float')
    print(rawData)
    if asse == 'X':
        rawData = np.append(rawData, cal.asse(nume, '1', sensor), axis=0)
        with open("cod.txt", mode='w') as f:
            f.write(str('10'))
        f.close()
        cal.save(rawData, nume, asse)

    if asse == 'Y':
        rawData = np.append(rawData, cal.asse(nume, '2', sensor), axis=0)
        with open("cod.txt", mode='w') as f:
            f.write(str('20'))
        f.close()
        cal.save(rawData, nume, asse)

    if asse == 'Z':
        rawData = np.append(rawData, cal.asse(nume, '3', sensor), axis=0)

        with open("cod.txt", mode='w') as f:
            f.write(str('30'))
        f.close()
        cal.save(rawData, nume, asse)


@app.route("/meas")
def meas():
    global g_box_config

    prnt()
    bluetooth_scan_entries = ble.get_available_devices(g_box_config.bluetooth_scan_time)
    wifi_scan_entries = wifis.Scan()

    return render_template('/meas.html', bluetooth_devices=bluetooth_scan_entries, wifi_devices=wifi_scan_entries)


@app.route("/misu")
def misu():
    global g_box_config

    prnt()
    stato = "ok"
    if request.method == 'GET':
        token = request.args.get('token')
        punto = request.args.get('punto')
    temp1 = recup(token, punto)
    long = temp1[0]
    lat = temp1[1]
    cx = temp1[2]
    cy = temp1[3]
    conf_file = os.getcwd() + "/static/config/" + token + "_conf.txt"
    conf_read = open(conf_file, "r").readlines()
    config = {conf_read[0].split('\t')[0]: (conf_read[0].split('\t')[1]).split('\n')[0],
              conf_read[1].split('\t')[0]: (conf_read[1].split('\t')[1]).split('\n')[0],
              conf_read[2].split('\t')[0]: (conf_read[2].split('\t')[1]).split('\n')[0],
              conf_read[3].split('\t')[0]: (conf_read[3].split('\t')[1]).split('\n')[0],
              conf_read[4].split('\t')[0]: (conf_read[4].split('\t')[1]).split('\n')[0],
              conf_read[5].split('\t')[0]: (conf_read[5].split('\t')[1]).split('\n')[0]}

    num = int(config['numero'])
    ble_s = int(config['ble'])
    wifi_s = int(config['wifi'])

    bluetooth_macs = ast.literal_eval(config['ble-macs'])
    wifi_macs = ast.literal_eval(config['wifi-macs'])

    try:
        x, y, z, cm = measure.multi(sensor, num)
        data_file = os.getcwd() + "/static/data/" + token + "/data_magn.txt"
        with open(data_file, mode='a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow([time.time(), punto, cx, cy, x, y, z, cm, long, lat])
    except:
        stato = "ko"

    print("ble: ", ble_s)
    if (ble_s == 1):
        try:
            data_file = os.getcwd() + "/static/data/" + token + "/data_ble.txt"

            dble = []
            if len(bluetooth_macs) == 0:
                dble = ble.scan(g_box_config.bluetooth_scan_time)
            else:
                dble = ble.scan_filter(g_box_config.bluetooth_scan_time, bluetooth_macs)

            with open(data_file, mode='a') as f:
                writer = csv.writer(f, delimiter='\t')
                for i in range(len(dble)):
                    writer.writerow([time.time(), punto, cx, cy, dble[i][0], dble[i][1], long, lat])
        except:
            stato = "bko"

    print("wifi: ", wifi_s)
    if (wifi_s == 1):
        try:
            data_file = os.getcwd() + "/static/data/" + token + "/data_wifi.txt"

            dwifi = []
            if len(wifi_macs) == 0:
                dwifi = wifis.Scan()
            else:
                dwifi = wifis.scan_filter(wifi_macs)

            with open(data_file, mode='a') as f:
                writer = csv.writer(f, delimiter='\t')
                for cell in dwifi:
                    writer.writerow(
                        [time.time(), punto, cx, cy, cell['ssid'], cell['address'], cell['channel'], cell['frequency'],
                         cell['quality'], cell['signal'], long, lat])
        except:
            stato = "wko"

    if stato != "ko":
        good(token, punto)

    return (stato)


@app.route("/end")
def end():
    global g_box_config

    if request.method == 'GET':
        token = request.args.get('token')

    img_format = request.args.get('img-format')

    data_file = os.getcwd() + "/static/data/" + token + "/data_magn.txt"
    data = np.genfromtxt(data_file, delimiter='\t')
    url_img = heatmap.magnmap(data, token, g_box_config.magnetic_map_interpolation, g_box_config.magnetic_map_color)
    return "ok"


@app.route("/down_pac")
def down_pac():
    global g_box_config

    tt = request.args.get('t')
    nn = request.args.get('n')
    dd = request.args.get('d')
    resusincro = sincro.download(g_box_config.server_ip, g_box_config.server_port, tt, nn, dd)
    return jsonify(resusincro)


@app.route("/up")
def up():
    global g_box_config

    tt = request.args.get('t')
    resusincro = sincro.upload(g_box_config.server_ip, g_box_config.server_port, tt)
    return jsonify(resusincro)


@app.route("/pagend")
def pagend():
    prnt()
    if request.method == 'GET':
        token = request.args.get('token')
    conf_file = os.getcwd() + "/static/config/" + token + "_conf.txt"
    conf_read = open(conf_file, "r").readlines()
    config = {conf_read[0].split('\t')[0]: (conf_read[0].split('\t')[1]).split('\n')[0],
              conf_read[1].split('\t')[0]: (conf_read[1].split('\t')[1]).split('\n')[0],
              conf_read[2].split('\t')[0]: (conf_read[2].split('\t')[1]).split('\n')[0],
              conf_read[3].split('\t')[0]: (conf_read[3].split('\t')[1]).split('\n')[0]}
    ble_s = str(int(config['ble']))
    wifi_s = str(int(config['wifi']))
    ability = '1' + ble_s + wifi_s
    return render_template('meas3.html', token=token, ability=ability)


@app.route('/remove_measure', methods=(["GET"]))
def remove_measure():
    token = request.args.get('token')

    conf_file_path = os.getcwd() + "/static/config/" + token + "_conf.txt"

    if os.path.exists(conf_file_path):
        os.remove(conf_file_path)

    data_directory_path = os.getcwd() + "/static/data/" + token

    if os.path.exists(data_directory_path):
        shutil.rmtree(data_directory_path)

    upload_directory_path = os.getcwd() + "/static/uploads/" + token

    if os.path.exists(upload_directory_path):
        shutil.rmtree(upload_directory_path)

    return render_template("datx.html")


@app.route("/dati")
def datas():
    v = dati.load_dati()
    return (v)


@app.route("/datiremoto")
def elencodatiremoto():
    global g_box_config

    v = dati.load_remot(g_box_config.server_ip, g_box_config.server_port)
    return (v)


@app.route("/datx")
def datx():
    prnt()
    return render_template('datx.html')


@app.route("/dwmisu")
def dwmisu():
    prnt()
    return render_template('dwmisu.html')


@app.route('/meas', methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask

        uploaded_img = request.files['mappa']
        punti = request.files['punti']

        nome = (request.form['nome'])
        numero = (request.form['numero'])

        chosen_bluetooth_macs = request.form.getlist('macs')
        chosen_wifi_macs = request.form.getlist('wifis')

        wifi = 0
        if (request.form['wifi']) == 'ON':
            wifi = 1
        else:
            wifi = 0
        ble = 0
        if (request.form['ble']) == 'ON':
            ble = 1
        else:
            ble = 0
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        s = uuid.uuid4().hex + '_' + nome + '_' + year + month + day

        formatimg = (secure_filename(uploaded_img.filename).split('.')[1])
        img_filename = s + '.' + formatimg
        os.makedirs(os.getcwd() + upl_dir + s, exist_ok=True)
        os.makedirs(os.getcwd() + data_dir + s, exist_ok=True)
        img_filename = s + '/planimetria.' + formatimg
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))

        formatimgt = (secure_filename(punti.filename).split('.')[1])
        punti_filename = s + '_punti.' + formatimgt
        punti.save(os.path.join(app.config['UPLOAD_FOLDER'], punti_filename))
        gest_file(punti_filename, s)

        imr = Image.open(os.getcwd() + upl_dir + img_filename)
        widimr, heiimr = imr.size
        if widimr >= heiimr:
            heiimr = int((heiimr / widimr) * 2000)
            widimr = 2000
        else:
            widimr = int((widimr / heiimr) * 2000)
            heiimr = 2000
        resizedImage = imr.resize((widimr, heiimr), Image.Resampling.LANCZOS)
        # resizedImage.save(os.getcwd() +"/static/uploads/"+img_filename)
        img_filename = s + '/origin.' + formatimg
        resizedImage.save(os.getcwd() + data_dir + img_filename)
        config_file = 'static/config/' + s + '_conf.txt'
        with open(config_file, mode='w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(['nome', nome])
            writer.writerow(['numero', numero])
            writer.writerow(['wifi', wifi])
            writer.writerow(['ble', ble])

            writer.writerow(['ble-macs', chosen_bluetooth_macs])
            writer.writerow(['wifi-macs', chosen_wifi_macs])

        f.close()
        img_file_path = session.get('uploaded_img_file_path', None)
        return render_template('meas2.html', mappa=img_filename, token=s, wimg=widimr, himg=heiimr)


def gest_file(bn, s):
    bn = os.getcwd() + upl_dir + bn
    b = pd.read_csv(bn, header=None, names=("idp", "long", "lat", "x", "y"))
    b['misu'] = 0
    print(b)
    b.to_csv(os.getcwd() + upl_dir + s + '/misu.txt')
    os.remove(bn)


def recup(token, punto):
    bn = os.getcwd() + upl_dir + token + '/misu.txt'
    b = pd.read_csv(bn, header=0, names=("a", "idp", "long", "lat", "x", "y", "misu"))
    b = b.drop(['a'], axis=1)
    print(b)
    print(b.loc[b['idp'] == punto])
    c = b.loc[b['idp'] == punto]
    return [c["long"].values[0], c["lat"].values[0], c["x"].values[0], c["y"].values[0]]


def good(token, punto):
    bn = os.getcwd() + upl_dir + token + '/misu.txt'
    b = pd.read_csv(bn, header=0, names=("a", "idp", "long", "lat", "x", "y", "misu"))
    c = b.loc[b['idp'] == punto]
    ind = c['a'].values[0]
    print(ind)
    b = b.drop(['a'], axis=1)
    print(b)
    b['misu'][ind] = 1
    print(b)
    b.to_csv(os.getcwd() + upl_dir + token + '/misu.txt')


@app.route("/markers")
def get_markers():
    token = request.args.get('token')
    bn = os.getcwd() + upl_dir + token + '/misu.txt'
    b = pd.read_csv(bn)
    finalresponse = [{"idp": ii, "lat": aa, "long": bb, "x": cc, "y": dd, "misu": ee} for ii, aa, bb, cc, dd, ee in
                     zip(b['idp'], b['lat'], b['long'], b['x'], b['y'], b['misu'])]
    print(finalresponse)
    return jsonify(finalresponse)


@app.route("/restart")
def restart():
    os.system('sudo reboot')
    return ("ok")


@app.route("/edit")
def edit():
    if request.method == 'GET':
        token = request.args.get('token')
    img_filename = token + '/origin.png'
    imr = Image.open(os.getcwd() + data_dir + img_filename)
    widimr, heiimr = imr.size
    if widimr >= heiimr:
        heiimr = int((heiimr / widimr) * 2000)
        widimr = 2000
    else:
        widimr = int((widimr / heiimr) * 2000)
        heiimr = 2000
    return render_template('meas2.html', mappa=img_filename, token=token, wimg=widimr, himg=heiimr)


def prnt():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    (s.connect(("8.8.8.8", 443)))
    iip = (s.getsockname()[0])
    nssid = os.popen("sudo iwgetid -r").read()
    display.scrivi("    IPS", "", "Dispostivo Pronto", "WiFi: " + nssid, iip + ":443")


@app.route("/points")
def points():
    prnt()
    return render_template('points/index.html')


@app.route("/addpoints")
def addpoints():
    prnt()
    return render_template('points/addpoints.html')


@app.route("/map")
def map():
    prnt()
    return render_template('points/map.html')


if __name__ == "__main__":
    try:
        o = -1
        display.scrivi("Loading...", "", "", "", "")
        time.sleep(10.5)
        a = 0
        while o == -1:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                (s.connect(("8.8.8.8", 443)))
                iip = (s.getsockname()[0])
                o = 1
            except:
                display.scrivi("Loading...", "", "Connesione", "in corso....", "")
                time.sleep(100)
                a = a + 1
                if a > 4:
                    display.scrivi("Attendere...", "", "Riavvio", "in corso....", "")
                    time.sleep(2)  # os.system('sudo reboot')
        display.scrivi("    IPS", "", "   Dispostivo in ", "   caricamento", iip + ":443")
        time.sleep(0.4)

        global g_box_config
        g_box_config = configf.BoxConfig()
        g_box_config.load()

        measure.set_sensor_odr(sensor, g_box_config.output_data_rate)

        cert = os.getcwd() + '/cert.pem'
        key = os.getcwd() + '/priv_key.pem'
        nssid = os.popen("sudo iwgetid -r").read()
        display.scrivi("    IPS", "", "Dispostivo Pronto", "WiFi: " + nssid, iip + ":443")
        app.run(debug=True, host=iip, port=int(443), ssl_context=('cert.pem', 'priv_key.pem'))
    except KeyboardInterrupt:
        pass
