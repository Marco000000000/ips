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

@app.route('/update_tables')
def update_tables():
    print("UPDATING TABLES...")
    db = mysql.connector.connect(host='localhost', user='root', password='prova_prova')
    db_cursor = db.cursor()

    token = "ucijk2rvel44_Misura02_20231122"
    
    data_rootpath = os.getcwd()+"\\data\\"+token+"\\"
    uploads_rootpath = os.getcwd()+"\\uploads\\"+token+"\\"
    
    metadata_filepath = uploads_rootpath+"misu.txt"
    
    data_magn_filepath = data_rootpath+"data_magn.txt"
    data_bluetooth_filepath = data_rootpath+"data_ble.txt"
    data_wifi_filepath = data_rootpath+"data_wifi.txt"
    
    with open(metadata_filepath, 'r') as file:
        file.readline()
        for line in file:
            point_metadata = line.split(',')
            
            point_ID = point_metadata[1]
            point_Long = float(point_metadata[2])
            point_Lat = float(point_metadata[3])
            point_CoordX = int(point_metadata[4])
            point_CoordY = int(point_metadata[5])
            
            print(point_Long)
            
            add_measure = ("INSERT INTO my_schema.measure VALUES (%s, %s)")
            data_measure = (token, point_ID)
            
            print(data_measure)
            
            add_punto = ("INSERT INTO my_schema.point VALUES (%s, %s, %s, %s, %s)")            
            data_punto = (point_ID, point_CoordX, point_CoordY, point_Long, point_Lat)
            
            db_cursor.execute(add_measure, data_measure)
            db_cursor.execute(add_punto, data_punto)
            
    db.commit()
    db_cursor.close()
    db.close()
        
    return "HELLO TABLES"

if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        iip=(s.getsockname()[0])
        app.run(debug=True, host=iip, port=80)
    except KeyboardInterrupt:
        pass