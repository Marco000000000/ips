from bluepy.btle import Scanner


def scan(tempo):
    matrix = []
    scanner = Scanner()
    print(tempo)
    devices = scanner.scan(tempo)
 
    for device in devices:
        #print("DEV = {} RSSI = {}".format(device.addr, device.rssi))
        matrix.append([device.addr, device.rssi])
        
    return matrix

def get_available_devices(tempo):
    scanner = Scanner()
    
    scan_entries = scanner.scan(tempo, passive=True)
    
    for entry in scan_entries:
        print("SCAN ENTRY: " + str(entry.getScanData()), flush=True)
    
    return scan_entries
    

def scan_filter(tempo, device_addresses_list):
    matrix = []
    scanner = Scanner()
    print(tempo)
    devices = scanner.scan(tempo)
    
    for address in device_addresses_list:
        for device in devices:
            if address == device.addr:
                matrix.append([device.addr, device.rssi])
        
    return matrix
    
    
    
    
