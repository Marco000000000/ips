import os
import shutil
import subprocess


def setup():
    # Check if the user is root
    if os.geteuid() != 0:
        print("Please run as root (sudo).")
        exit()

    # Check if nmcli exists
    if not shutil.which('nmcli'):
        print("nmcli not found. Please install NetworkManager.")
        exit()

    # Parameters for the Raspberry Pi hotspot
    hotspot_name = "IPS"
    hotspot_password = "password"

    # Create hotspot
    create_hotspot = subprocess.run(
        ['nmcli', 'device', 'wifi', 'hotspot', 'ssid', hotspot_name, 'con-name', hotspot_name, 'password',
         hotspot_password,
         'ifname', 'wlan0'],
        capture_output=True,
        text=True
    )
    if create_hotspot.returncode != 0:
        print("Error creating hotspot:", create_hotspot.stderr)
        exit()

    # Configure hotspot to autorun at boot

    modify_connection = subprocess.run(
        ['nmcli', 'connection', 'modify', hotspot_name, 'connection.autoconnect', 'yes'],
        capture_output=True,
        text=True
    )
    if modify_connection.returncode != 0:
        print("Error modifying connection:", modify_connection.stderr)
        exit()

    # Autorun wifi configuration page at boot
    this_directory = os.path.dirname(os.path.realpath(__file__))
    service_file = "/etc/systemd/system/hotspot.service"

    with open(service_file, 'w') as f:
        f.write(f"[Unit]\n"
                f"Description=Hotspot Configuration Service\n"
                f"After=multi-user.target\n"
                f"Requires=network.target\n\n"
                f"[Service]\n"
                f"Type=idle\n"
                f"ExecStart=/usr/bin/python3 {this_directory}/config_wifi_page/app.py\n"
                f"Restart=always\n"
                f"RestartSec=10\n"
                f"User=root\n\n"
                f"[Install]\n"
                f"WantedBy=multi-user.target\n")

    os.chmod(service_file, 0o644)
    daemon_reload = subprocess.run(['systemctl', 'daemon-reload'], capture_output=True, text=True)
    if daemon_reload.returncode != 0:
        print("Error reloading systemd daemon:", daemon_reload.stderr)
        exit()

    enable_service = subprocess.run(['systemctl', 'enable', 'hotspot.service'], capture_output=True, text=True)
    if enable_service.returncode != 0:
        print("Error enabling hotspot service:", enable_service.stderr)
        exit()
    start_service = subprocess.run(['systemctl', 'start', 'hotspot.service'], capture_output=True, text=True)
    if start_service.returncode != 0:
        print("Error starting hotspot service:", start_service.stderr)
        exit()

    print("Setup completed successfully!")


if __name__ == '__main__':
    setup()
