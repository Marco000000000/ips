from flask import Flask, render_template, request, session, jsonify, send_file
import socket
import os
import requests

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
    print(rootdir)
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

if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        iip=(s.getsockname()[0])
        app.run(debug=True, host=iip, port=80)
    except KeyboardInterrupt:
        pass