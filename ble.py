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
    
    return scanner.scan(tempo)
    

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
    
    
    
    
