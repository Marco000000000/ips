import numpy as np
import csv
import os
import keyboard
import pandas as pd
from json import loads, dumps
import requests


def recd():
    a = []
    rootdir = os.getcwd()+'/static/config'
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isfile(d):
            z=(d.split(rootdir+'/'))
            z=(z[1].split('_conf.txt'))
            tokenz = (z[0].split('_'))[0]
            a.append(tokenz)
    return a


def load_dati():    
    a = []
    col = ['Token', 'Nome', 'Data', 'Num', 'Ble', 'WiFi']
    rootdir = os.getcwd()+'/static/config'
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isfile(d):
            conf_read = open(d, "r").readlines()
            config = {conf_read[0].split('\t')[0]: (conf_read[0].split('\t')[1]).split('\n')[0],
                      conf_read[1].split('\t')[0]: (conf_read[1].split('\t')[1]).split('\n')[0],
                      conf_read[2].split('\t')[0]: (conf_read[2].split('\t')[1]).split('\n')[0],
                      conf_read[3].split('\t')[0]: (conf_read[3].split('\t')[1]).split('\n')[0]}
            num = int(config['numero'])
            ble_s = int(config['ble'])
            wifi_s = int(config['wifi'])        
            z=(d.split(rootdir+'/'))
            z=(z[1].split('_conf.txt'))
            tokenz = (z[0].split('_'))[0]
            nomez = (z[0].split('_'))[1]
            dataz = (z[0].split('_'))[2]
            new_row = {'Token': tokenz , 'Nome': nomez, 'Data': dataz, 'Num': num, 'Ble': ble_s, 'WiFi': wifi_s}
            a.append(new_row)
    df = pd.DataFrame(a,columns=col)
    
    result = df.to_json(orient="index")
    parsed = loads(result)
    vett = dumps(parsed, indent=4)
    
    return vett

def load_remot(server, porta):
    print("connesione al server:",server," : ",porta)
    

    url = server+":"+ str(porta)
    req = "/elenco"
    endpoint = url+req
    response = requests.get(endpoint)
    print(response)

    if response.ok:
        json_data = response.json()
        df = pd.DataFrame(json_data)
        df["local"]=0
        print(df)
        lista_token=recd()
        print(lista_token)
        
        for index, row in df.iterrows():
            aa = row['token']
            if aa in lista_token:
                df.at[index, "local"]=1
            else:
                df.at[index, "local"]=0
        
        result = df.to_json(orient="index")
        parsed = loads(result)
        vett = dumps(parsed, indent=4)
        print(vett)
        
    else:
        print("Status Code: ", response.status_code)
        print("Response Content: ", response.content)
        vett = {"error: ", response.status_code}
        
    return vett
