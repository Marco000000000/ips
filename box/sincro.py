import requests
import pandas as pd
import os
from json import loads, dumps

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Cartella creata:", folder_path)
    else:
        print("La cartella esiste già:", folder_path)


def upload(server, porta, t):
    print("connesione al server:",server," : ",porta)
    arrayr = []
    url = server+":"+ str(porta)

    #conf
    req = "/upconf"
    endpoint = url+req
    rootdir = os.getcwd()+'/static/config/'
    filename= t + '_conf.txt'
    file_path = rootdir + filename
    files = {'file': open(file_path, 'rb')}
    response = requests.post(endpoint, data = {'filename':filename}, files=files)
    print(response.text)
    if response.ok:
        print("Status Code: ", response.status_code)
        conf_file = file_path
        conf_read = open(conf_file, "r").readlines()
        config = {conf_read[0].split('\t')[0]: (conf_read[0].split('\t')[1]).split('\n')[0],
                  conf_read[1].split('\t')[0]: (conf_read[1].split('\t')[1]).split('\n')[0],
                  conf_read[2].split('\t')[0]: (conf_read[2].split('\t')[1]).split('\n')[0],
                  conf_read[3].split('\t')[0]: (conf_read[3].split('\t')[1]).split('\n')[0]}
        ble_s = int(config['ble'])
        wifi_s = int(config['wifi'])
        arrayr.append({"config":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"config":"ko"})
        
    #data
    req = "/updata"
    endpoint = url+req
    rootdir = os.getcwd()+'/static/data/'+t+'/'
    #data_magn
    filename = 'data_magn.txt'
    file_path = rootdir + filename
    files = {'file': open(file_path, 'rb')}
    response = requests.post(endpoint, data = {'filename':filename, 'ape':t}, files=files)
    print(response.text)
    if response.ok:
        print("Status Code: ", response.status_code)
        arrayr.append({"data_magn":"ok"})    
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"data_magn":"ko"})
    #data_wifi.txt
    if wifi_s == 1:
        filename =  "data_wifi.txt"
        file_path = rootdir + filename
        files = {'file': open(file_path, 'rb')}
        response = requests.post(endpoint, data = {'filename':filename, 'ape':t}, files=files)
        print(response.text)    
        if response.ok:
            print("Status Code: ", response.status_code)
            arrayr.append({"data_wifi":"ok"})
        else:
            print("Status Code: ", response.status_code)
            print("Response Content: ", response.content)
            arrayr.append({"data_wifi":"ko"})
    #data_ble.txt
    if ble_s == 1:
        filename =  "data_ble.txt"
        file_path = rootdir + filename
        files = {'file': open(file_path, 'rb')}
        response = requests.post(endpoint, data = {'filename':filename, 'ape':t}, files=files)
        print(response.text)    
        if response.ok:
            print("Status Code: ", response.status_code)
            arrayr.append({"data_ble":"ok"})
        else:
            print("Status Code: ", response.status_code)
            print("Response Content: ", response.content)
            arrayr.append({"data_ble":"ko"})
    #hm
    req = "/updata"
    endpoint = url+req
    filename =  'hm.png'
    file_path = rootdir + filename
    files = {'file': open(file_path, 'rb')}
    response = requests.post(endpoint, data = {'filename':filename, 'ape':t}, files=files)
    print(response.text)    
    if response.ok:
        print("Status Code: ", response.status_code)
        arrayr.append({"hm":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"hm":"ko"})
    #origin
    req = "/updata"
    endpoint = url+req
    filename =  'origin.png'
    file_path = rootdir + filename
    files = {'file': open(file_path, 'rb')}
    response = requests.post(endpoint, data = {'filename':filename, 'ape':t}, files=files)
    print(response.text)    
    if response.ok:
        print("Status Code: ", response.status_code)
        arrayr.append({"origin":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"origin":"ko"})
    #uploads
    req = "/upum"
    endpoint = url+req
    rootdir = os.getcwd()+'/static/uploads/'+t+'/'
    #data_magn
    filename = 'misu.txt'
    file_path = rootdir + filename
    files = {'file': open(file_path, 'rb')}
    response = requests.post(endpoint, data = {'filename':filename, 'ape':t}, files=files)
    print(response.text)
    if response.ok:
        print("Status Code: ", response.status_code)
        arrayr.append({"misu":"ok"})    
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"misu":"ko"})
    #planimetria
    filename = 'planimetria.png'
    file_path = rootdir + filename
    files = {'file': open(file_path, 'rb')}
    response = requests.post(endpoint, data = {'filename':filename, 'ape':t}, files=files)
    print(response.text)
    if response.ok:
        print("Status Code: ", response.status_code)
        arrayr.append({"plani":"ok"})    
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"plani":"ko"})
    print(arrayr)
    
    return(arrayr)


def download(server, porta, t, n, d):
    print("connesione al server:",server," : ",porta)
    arrayr = []
    
    url = server+":"+ str(porta)
    
    #confing
    print("download file config")
    req = "/dwc"
    endpoint = url+req
    filename = t + "_" + n + "_" + d + "_conf.txt"
    rootdir = os.getcwd()+'/static/config/'
    response = requests.post(endpoint, data = {'filename':filename})
    if response.ok:
        print("Status Code: ", response.status_code)
        with open(rootdir+filename, "w") as f:
            f.write(response.text)
        
        conf_file = os.getcwd() + "/static/config/" + filename
        conf_read = open(conf_file, "r").readlines()
        config = {conf_read[0].split('\t')[0]: (conf_read[0].split('\t')[1]).split('\n')[0],
                  conf_read[1].split('\t')[0]: (conf_read[1].split('\t')[1]).split('\n')[0],
                  conf_read[2].split('\t')[0]: (conf_read[2].split('\t')[1]).split('\n')[0],
                  conf_read[3].split('\t')[0]: (conf_read[3].split('\t')[1]).split('\n')[0]}
        ble_s = int(config['ble'])
        wifi_s = int(config['wifi'])
        arrayr.append({"config":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"config":"ko"})
    
    #data
    name_folder=os.getcwd() + "/static/data/" + t + "_" + n + "_" + d + "/"
    create_folder(name_folder)
    
    #data_magn.txt
    req = "/dwdm"
    endpoint = url+req
    ape = t + "_" + n + "_" + d
    filename =  "data_magn.txt"
    response = requests.post(endpoint, data = {'filename':filename, 'ape':ape})
    if response.ok:
        print("Status Code: ", response.status_code)
        with open(name_folder+filename, "w") as f:
            f.write(response.text)
        arrayr.append({"data_magn":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"data_magn":"ko"})
    
    #data_wifi.txt
    if wifi_s == 1:
        filename =  "data_wifi.txt"
        response = requests.post(endpoint, data = {'filename':filename, 'ape':ape})
        if response.ok:
            print("Status Code: ", response.status_code)
            with open(name_folder+filename, "w") as f:
                f.write(response.text)
            arrayr.append({"data_wifi":"ok"})
        else:
            print("Status Code: ", response.status_code)
            print("Response Content: ", response.content)
            arrayr.append({"data_wifi":"ko"})
        
    #data_ble.txt
    if ble_s == 1:
        filename =  "data_ble.txt"
        response = requests.post(endpoint, data = {'filename':filename, 'ape':ape})
        if response.ok:
            print("Status Code: ", response.status_code)
            with open(name_folder+filename, "w") as f:
                f.write(response.text)
            arrayr.append({"data_ble":"ok"})
        else:
            print("Status Code: ", response.status_code)
            print("Response Content: ", response.content)
            arrayr.append({"data_ble":"ko"})

    #hm
    req = "/dwhm"
    endpoint = url+req
    ape = t + "_" + n + "_" + d
    filename =  "hm.png"
    response = requests.post(endpoint, data = {'filename':filename, 'ape':ape})
    if response.ok:
        print("Status Code: ", response.status_code)
        with open(name_folder+filename, "wb") as f:
            f.write(response.content)
        arrayr.append({"heatmap":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"heatmap":"ko"})
    
    #origin
    filename = "origin.jpg"
    response = requests.post(endpoint, data = {'filename':filename, 'ape':ape})
    if response.ok:
        print("Status Code: ", response.status_code)
        with open(name_folder+filename, "wb") as f:
            f.write(response.content)
        arrayr.append({"origin":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"origin":"ko"})
    
    #uploads
    name_folder=os.getcwd() + "/static/uploads/" + t + "_" + n + "_" + d + "/"
    create_folder(name_folder)
    #misu.txt
    req = "/dwum"
    endpoint = url+req
    ape = t + "_" + n + "_" + d
    filename =  "misu.txt"
    response = requests.post(endpoint, data = {'filename':filename, 'ape':ape})
    if response.ok:
        print("Status Code: ", response.status_code)
        with open(name_folder+filename, "w") as f:
            f.write(response.text)
        arrayr.append({"misu":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"misu":"ko"})

    #planimetria
    req = "/dwpl"
    endpoint = url+req
    ape = t + "_" + n + "_" + d
    filename = "planimetria.jpg"
    response = requests.post(endpoint, data = {'filename':filename, 'ape':ape})

    if response.ok:
        print("Status Code: ", response.status_code)
        with open(name_folder+filename, "wb") as f:
            f.write(response.content)
        arrayr.append({"plani":"ok"})
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        arrayr.append({"plani":"ko"})
        
    print(arrayr)
    #parsed = loads(arrayr)
    #vett = dumps(parsed, indent=4)
    #print(vett)
    return arrayr
