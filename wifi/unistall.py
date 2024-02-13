import os
import shutil
import subprocess

from install import SERVICE_NAME, ETC_APP_DIRECTORY, DEFAULT_HOTSPOT_NAME


def stop_and_disable_service():
    """Stop and disable the hotspot service."""
    subprocess.run(['systemctl', 'stop', SERVICE_NAME], capture_output=True, text=True)
    subprocess.run(['systemctl', 'disable', SERVICE_NAME], capture_output=True, text=True)


def remove_service_file():
    """Remove the service file."""
    service_file = f"/etc/systemd/system/{SERVICE_NAME}"
    if os.path.exists(service_file):
        os.remove(service_file)


def remove_application_folder():
    """Remove the application folder from /etc."""
    if os.path.exists(ETC_APP_DIRECTORY):
        shutil.rmtree(ETC_APP_DIRECTORY)


def remove_hotspot():
    """Remove the created Wi-Fi hotspot."""
    subprocess.run(['nmcli', 'connection', 'delete', DEFAULT_HOTSPOT_NAME], capture_output=True, text=True)


def uninstall():
    """Main uninstall function."""
    stop_and_disable_service()
    remove_service_file()
    remove_application_folder()
    remove_hotspot()
    print("Uninstallation completed successfully!")


if __name__ == '__main__':
    uninstall()
