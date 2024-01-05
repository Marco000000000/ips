from flask import Flask, render_template, request, session, jsonify, send_file
import socket
import os
import requests
import mysql.connector

app = Flask(__name__)

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Cartella creata:", folder_path)
    else:
        print("La cartella esiste già:", folder_path)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/elenco")
def elenco():
    arrayfile = []
    rootdir = os.getcwd()+'\config'
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        sep = rootdir + "\\"
        x = d.split(sep)
        sxl = x[1].split("_conf.txt")
        sx = sxl[0]
        spe = sx.split("_")
        token = spe[0]
        nome = spe[1]
        date = spe[2]
        arrayfile.append({"token":token, "nome":nome, "date": date})

    return(arrayfile)
    

@app.route("/dwc", methods = ['POST'])
def dwc():
    data= (request.form)
    filename = data['filename']
    rootdir = os.getcwd()+"\\config\\"+filename
    return send_file(rootdir, as_attachment=True)

@app.route("/dwdm", methods = ['POST'])
def dwdm():
    data= (request.form)
    filename = data['filename']
    ape = data['ape']
    rootdir = os.getcwd()+"\\data\\"+ape+"\\"+filename
    return send_file(rootdir, as_attachment=True)

@app.route("/dwum", methods = ['POST'])
def dwum():
    data= (request.form)
    filename = data['filename']
    ape = data['ape']
    rootdir = os.getcwd()+"\\uploads\\"+ape+"\\"+filename
    return send_file(rootdir, as_attachment=True)

@app.route("/dwhm", methods = ['POST'])
def dwhm():
    data= (request.form)
    filename = data['filename']
    ape = data['ape']
    rootdir = os.getcwd()+"\\data\\"+ape+"\\"+filename
    return send_file(rootdir, as_attachment=True)

@app.route("/dwpl", methods = ['POST'])
def dwpl():
    data= (request.form)
    filename = data['filename']
    ape = data['ape']
    rootdir = os.getcwd()+"\\uploads\\"+ape+"\\"+filename
    return send_file(rootdir, as_attachment=True)


@app.route('/upconf', methods=['POST'])
def upconf():
    data = (request.form)
    filename = data['filename']
    if 'file' not in request.files:
        return "Nessun file inviato"
    rootdir = os.getcwd()+"\\config\\"+filename
    print(rootdir)
    file = request.files['file']
    file.save(rootdir)  # Salva il file nella directory corrente con il nome "uploaded_file.txt"

    return "File caricato con successo!"


@app.route('/updata', methods=['POST'])
def updata():
    data = (request.form)
    filename = data['filename']
    ape = data['ape']
    
    if 'file' not in request.files:
        return "Nessun file inviato"
    rootdir = os.getcwd()+"\\data\\"+ape+"\\"
    create_folder(rootdir)
    rootdir = rootdir+filename
    
    file = request.files['file']
    file.save(rootdir)
    
    return "File caricato con successo!"

@app.route('/upum', methods=['POST'])
def upum():
    data = (request.form)
    filename = data['filename']
    ape = data['ape']
    
    if 'file' not in request.files:
        return "Nessun file inviato"
    rootdir = os.getcwd()+"\\uploads\\"+ape+"\\"
    create_folder(rootdir)
    rootdir = rootdir+filename
    print(rootdir)
    file = request.files['file']
    file.save(rootdir) 

    return "File caricato con successo!"

@app.route('/update_tables', methods=["GET"])
def update_tables():
    db = mysql.connector.connect(host='localhost', user='root', password='prova_prova')
    db_cursor = db.cursor()

    token = request.args.get('ape')
    
    print("TOKEN IS: ", token)
    
    data_rootpath = os.getcwd()+"\\data\\"+token+"\\"
    uploads_rootpath = os.getcwd()+"\\uploads\\"+token+"\\"
    
    metadata_filepath = uploads_rootpath+"misu.txt"
    
    data_magn_filepath = data_rootpath+"data_magn.txt"
    data_bluetooth_filepath = data_rootpath+"data_ble.txt"
    data_wifi_filepath = data_rootpath+"data_wifi.txt"
    
    db_cursor.execute("DELETE FROM my_schema.point WHERE (Token=%s)", [token])
    db_cursor.execute("DELETE FROM my_schema.magnetic_field WHERE (Token=%s)", [token])
    db_cursor.execute("DELETE FROM my_schema.bluetooth WHERE (Token=%s)", [token])
    db_cursor.execute("DELETE FROM my_schema.wifi WHERE (Token=%s)", [token])
    
    with open(metadata_filepath, 'r') as file:
        file.readline()
        for line in file:
            point_metadata = line.split(',')
            
            point_ID = point_metadata[1]
            point_Long = float(point_metadata[2])
            point_Lat = float(point_metadata[3])
            point_CoordX = int(point_metadata[4])
            point_CoordY = int(point_metadata[5])
            
            # add_measure = ("INSERT INTO my_schema.measure VALUES (%s, %s)")
            # data_measure = (token, point_ID)    
            
            db_query = ("INSERT INTO my_schema.point VALUES (%s, %s, %s, %s, %s, %s)")            
            db_data = (token, point_ID, point_CoordX, point_CoordY, point_Long, point_Lat)
            
            # db_cursor.execute(add_measure, data_measure)
            db_cursor.execute(db_query, db_data)
    
    with open(data_magn_filepath, 'r') as file:
        for line in file:
            point_data = line.split('\t')
            
            point_ID = point_data[1]
            
            point_magX = float(point_data[4])
            point_magY = float(point_data[5])
            point_magZ = float(point_data[6])
            point_magM = float(point_data[7])
    
            db_query = ("INSERT INTO my_schema.magnetic_field VALUES (%s, %s, %s, %s, %s, %s)")
            db_data = (token, point_ID, point_magX, point_magY, point_magZ, point_magM)
            
            db_cursor.execute(db_query, db_data)

    with open(data_bluetooth_filepath, 'r') as file:
        for line in file:
            point_data = line.split('\t')
            
            point_ID = point_data[1]
            
            point_Mac = point_data[4]
            point_Rssi = int(point_data[5])
    
            db_query = ("INSERT INTO my_schema.bluetooth VALUES (%s, %s, %s, %s)")
            db_data = (token, point_ID, point_Mac, point_Rssi)
            
            db_cursor.execute(db_query, db_data)
    
    with open(data_wifi_filepath, 'r') as file:
        for line in file:
            point_data = line.split('\t')
            
            point_ID = point_data[1]
            
            point_SSID = point_data[4]
            point_MAC = point_data[5]
            point_Channel = int(point_data[6])
            point_Frequency = point_data[7]
            point_Quality = point_data[8]
            point_RSSI = int(point_data[9])
    
            db_query = ("INSERT INTO my_schema.wifi VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            db_data = (token, point_ID, point_MAC, point_SSID, point_Channel, point_Frequency, point_Quality, point_RSSI)
            
            db_cursor.execute(db_query, db_data)

    
    db.commit()
    db_cursor.close()
    db.close()
        
    return "Tables updated correctly"

if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        iip=(s.getsockname()[0])
        app.run(debug=True, host=iip, port=80)
    except KeyboardInterrupt:
        pass