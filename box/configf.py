import melopero_lsm9ds1 as mp
import csv
import os

class BoxConfig:
    def __init__(self):
        # Output data rate del sensore magnetico, in Hz
        self.output_data_rate = 80
        
        # Tempo di scansionamento della ricerca bluetooth, in secondi
        self.bluetooth_scan_time = 1.5
        
        # Tipo di interpolazione da usare nella generazione della mappa magnetica.
        # Valori possibili sono: nearest, linear, cubic
        self.magnetic_map_interpolation = "cubic"
        
        # Colorazione della mappa magnetica.
        # Valori possibili sono: jet, ocean, gnu
        self.magnetic_map_color = "jet"
        
        # Indirizzo ip del server a cui collegarsi per fare upload/download delle misurazioni
        self.server_ip = "http://192.168.1.0"
        
        # Numero di porta del server a cui collegarsi per fare upload/download delle misurazioni
        self.server_port = 80

    def save(self):
        config_file_path = os.getcwd() + "/static/config_box/config.csv"
        with open(config_file_path, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=" ")
            
            writer.writerow(["output_data_rate", "bluetooth_scan_time", "magnetic_map_interpolation", "magnetic_map_color", "server_ip", "server_port"])
            writer.writerow([self.output_data_rate, self.bluetooth_scan_time, self.magnetic_map_interpolation, self.magnetic_map_color, self.server_ip, self.server_port])
    
    def load(self):
        saved_config_file_path = os.getcwd() + "/static/config_box/config.csv"
        basic_config_file_path = os.getcwd() + "/static/config_box/basic_config.csv"
        
        config_file_path = basic_config_file_path
        
        if os.path.exists(saved_config_file_path):
            config_file_path = saved_config_file_path
        
        with open(config_file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=" ")
            config_data = list(reader)[0]
            
            self.set_output_data_rate(config_data["output_data_rate"])
            self.set_bluetooth_scan_time(config_data["bluetooth_scan_time"])
            self.set_magnetic_map_interpolation(config_data["magnetic_map_interpolation"])
            self.set_magnetic_map_color(config_data["magnetic_map_color"])
            self.set_server_ip(config_data["server_ip"])
            self.set_server_port(config_data["server_port"])
            
            
    def set_server_ip(self, ip):
        self.server_ip = ip
    
    def set_server_port(self, port):
        self.server_port = port
        
    def set_bluetooth_scan_time(self, time):
        accettable_values = [0.4, 1.3, 2.0, 3.0, 5.0]
        
        if time in accettable_values:
            self.bluetooth_scan_time = time
        else:
            self.bluetooth_scan_time = 1.3
    
    def set_magnetic_map_color(self, color):
        accettable_values = ["gnu", "ocean", "jet"]
        
        if color in accettable_values:
            self.magnetic_map_color = color
        else:
            self.magnetic_map_color = "jet"
    
    def set_magnetic_map_interpolation(self, interpolation):
        accettable_values = ["linear", "nearest", "cubic"]
        
        if interpolation in accettable_values:
            self.magnetic_map_interpolation = interpolation
        else:
            self.magnetic_map_interpolation = "cubic"
            
    def set_output_data_rate(self, odr):
        accettable_values = [0.625, 1.25, 2.5, 5.0, 10.0, 20.0, 40.0, 80.0]
        
        if odr in accettable_values:
            self.output_data_rate = odr
        else:
            self.output_data_rate = 40
                
        

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
