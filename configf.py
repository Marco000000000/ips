import melopero_lsm9ds1 as mp
import csv
import os

def load_conf():
    config_file = os.getcwd() + "/static/config_box/config.txt"
    basic_file = os.getcwd() + "/static/config_box/basic.txt"
    try:
        conf_read = open(config_file, "r").readlines()
    except:
        conf_read = open(basic_file, "r").readlines()
    config = {conf_read[0].split('\t')[0]: (conf_read[0].split('\t')[1]).split('\n')[0],
              conf_read[1].split('\t')[0]: (conf_read[1].split('\t')[1]).split('\n')[0],
              conf_read[2].split('\t')[0]: (conf_read[2].split('\t')[1]).split('\n')[0],
              conf_read[3].split('\t')[0]: (conf_read[3].split('\t')[1]).split('\n')[0],
              conf_read[4].split('\t')[0]: (conf_read[4].split('\t')[1]).split('\n')[0],
              conf_read[5].split('\t')[0]: (conf_read[5].split('\t')[1]).split('\n')[0],
              conf_read[6].split('\t')[0]: (conf_read[6].split('\t')[1]).split('\n')[0]}
    odr = int(config['odr'])
    nume = int(config['cali'])
    inter = (config['inter'])
    colormap = (config['colormap'])
    server = (config['server'])
    port = int(config['port'])
    t1 = float(config['ble'])
    
    if t1 == 4:
        tempo = 0.4
    elif t1 == 13:
        tempo = 1.3
    elif t1 == 2:
        tempo = 2
    elif t1 == 3:
        tempo = 3
    elif t1 == 5:
        tempo = 5
    
    return({'odr':odr,'cali':nume,'inter':inter,'colormap':colormap,'server':server,'port':port,'tempo':tempo})


def save_conf(a, b, c, d, e, f, g):
        config_file = 'static/config_box/config.txt'
        with open(config_file, mode='w') as ff:
            writer = csv.writer(ff, delimiter='\t')
            writer.writerow(['odr', a])
            writer.writerow(['cali', b])
            writer.writerow(['inter', c])
            writer.writerow(['colormap', d])
            writer.writerow(['ble', e])
            writer.writerow(['server', f])
            writer.writerow(['port', g])
        ff.close()
        odr = int(a)
        nume = int(b)
        inter = c
        colormap = d
        t1 = float(e)
        server = f
        port = int(g)
        if t1 == 4:
            tempo = 0.4
        elif t1 == 13:
            tempo = 1.3
        elif t1 == 2:
            tempo = 2
        elif t1 == 3:
            tempo = 3
        elif t1 == 5:
            tempo = 5
        
        return({'odr':odr,'cali':nume,'inter':inter,'colormap':colormap,'server':server,'port':port,'tempo':tempo})