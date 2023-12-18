import wifi
import time


def Scan():
    wifilist = []
    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        item = {
            "ssid": cell.ssid,
            "address": cell.address,
            "channel": cell.channel,
            "frequency": cell.frequency,
            "quality": cell.quality,
            "signal": cell.signal,
            "noise": cell.noise
        }
        wifilist.append(item)
    return wifilist

def scan_filter(addresses):
    all_list = Scan()
    filtered_list = []
    
    for wifi in all_list:
        for addr in addresses:
            if addr == wifi['address']:
                filtered_list.append(wifi)
    
    return filtered_list
