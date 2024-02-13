#!/bin/bash

# controlli
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo)."
    exit
fi

if ! command -v nmcli &> /dev/null; then
    echo "nmcli not found. Please install NetworkManager."
    exit
fi

# parametri hotspot della raspi
hotspot_name="IPS"
hotspot_password=""

# creazione hotspot
nmcli device wifi hotspot ssid "$hotspot_name" password "$hotspot_password" ifname wlan0

# configurazione hotspot per autorun al boot
hotspot_uuid=$(nmcli connection show | grep "$hotspot_name" | awk '{print $2}')
nmcli connection modify "$hotspot_uuid" connection.autoconnect yes connection.autoconnect-priority 100

# autorun pagina di configurazione wifi al boot
this_directory=$(readlink -f .)
service_file="/etc/systemd/system/hotspot.service"

printf "[Unit]
Description=Hotspot Configuration Service
After=multi-user.target
Requires=network.target
[Service]
Type=idle
ExecStart=/usr/bin/python3 %s/config_wifi_page/app.py
Restart=always
RestartSec=10
User=root
[Install]
WantedBy=multi-user.target" $this_directory > $service_file

chmod 644 $service_file
systemctl daemon-reload
systemctl enable hotspot.service