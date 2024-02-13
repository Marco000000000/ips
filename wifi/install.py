import os
import shutil
import subprocess
import sys

# Constants
DEFAULT_HOTSPOT_NAME = "IPS"
DEFAULT_HOTSPOT_PASSWORD = "password"
SERVICE_NAME = "hotspot.service"
APP_DIRECTORY = "config_wifi_page"
ETC_APP_DIRECTORY = "/etc/config_wifi_page"
REQUIREMENTS_FILE = "requirements.txt"


def check_root():
    """Check if the script is being run as root."""
    if os.geteuid() != 0:
        print("Please run as root (sudo).")
        exit(1)


def check_nmcli():
    """Check if nmcli is installed."""
    if not shutil.which('nmcli'):
        print("nmcli not found. Please install NetworkManager.")
        exit(1)


def install_requirements():
    """Install Python dependencies from requirements.txt."""
    requirements_path = os.path.join(os.path.dirname(__file__), REQUIREMENTS_FILE)
    if os.path.exists(requirements_path):
        subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
    else:
        print(f"Requirements file '{REQUIREMENTS_FILE}' not found.")
        exit(1)


def setup_hotspot(hotspot_name, hotspot_password):
    """Create the Wi-Fi hotspot and modify the connection to autoconnect."""
    create_hotspot = subprocess.run(
        ['nmcli', 'device', 'wifi', 'hotspot', 'ssid', hotspot_name, 'con-name', hotspot_name, 'password',
         hotspot_password, 'ifname', 'wlan0'], capture_output=True, text=True)
    if create_hotspot.returncode != 0:
        print("Error creating hotspot:", create_hotspot.stderr)
        exit(1)

    modify_connection = subprocess.run(['nmcli', 'connection', 'modify', hotspot_name, 'connection.autoconnect', 'yes'],
                                       capture_output=True, text=True)
    if modify_connection.returncode != 0:
        print("Error modifying connection:", modify_connection.stderr)
        exit(1)

    print(f"Hotspot \"{hotspot_name}\" created successfully")


def setup_autorun():
    """Setup autorun for the Wi-Fi configuration page."""
    # Copy the application folder to /etc
    full_app_dir = os.path.join(os.path.dirname(__file__), APP_DIRECTORY)
    if not os.path.exists(ETC_APP_DIRECTORY):
        shutil.copytree(full_app_dir, ETC_APP_DIRECTORY)
        print("Application folder copied to /etc")
    else:
        print("Application folder already exists in /etc")

    service_file = f"/etc/systemd/system/{SERVICE_NAME}"

    # Stop service if it's already running
    subprocess.run(['systemctl', 'stop', SERVICE_NAME], capture_output=True, text=True)

    with open(service_file, 'w') as f:
        f.write(f"[Unit]\n"
                f"Description=Hotspot Configuration Service\n"
                f"After=multi-user.target\n"
                f"Requires=network.target\n\n"
                f"[Service]\n"
                f"Type=idle\n"
                f"ExecStart=/usr/bin/python3 {ETC_APP_DIRECTORY}/app.py\n"
                f"Restart=always\n"
                f"RestartSec=10\n"
                f"User=root\n\n"
                f"[Install]\n"
                f"WantedBy=multi-user.target\n")

    os.chmod(service_file, 0o644)
    daemon_reload = subprocess.run(['systemctl', 'daemon-reload'], capture_output=True, text=True)
    if daemon_reload.returncode != 0:
        print("Error reloading systemd daemon:", daemon_reload.stderr)
        exit(1)

    enable_service = subprocess.run(['systemctl', 'enable', SERVICE_NAME], capture_output=True, text=True)
    if enable_service.returncode != 0:
        print("Error enabling hotspot service:", enable_service.stderr)
        exit(1)

    start_service = subprocess.run(['systemctl', 'start', SERVICE_NAME], capture_output=True, text=True)
    if start_service.returncode != 0:
        print("Error starting hotspot service:", start_service.stderr)
        exit(1)

    print(f"Setup service \"{SERVICE_NAME}\" completed successfully!")


def setup(hotspot_name=DEFAULT_HOTSPOT_NAME, hotspot_password=DEFAULT_HOTSPOT_PASSWORD):
    """Main setup function."""
    try:
        check_root()
        check_nmcli()
        install_requirements()
        setup_hotspot(hotspot_name, hotspot_password)
        setup_autorun()
        print("Setup completed successfully!")
    except Exception as e:
        print(f"An error occurred during setup: {str(e)}")
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        setup(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        setup()
    else:
        print("Usage: python script.py [hotspot_name hotspot_password]")
        exit(1)
