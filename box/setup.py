import os
import subprocess

import sys


def install_prereqs():
    """
    Install necessary packages and libraries.
    """
    subprocess.run(['sudo', 'apt-get', 'install', 'python3-pip', 'libglib2.0-dev'])
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'python3', 'python3-rpi.gpio', 'python3-pip', '-y'])

    print("Installing Flask web server...")
    subprocess.run(['sudo', 'venv/bin/pip', 'install', 'flask'])
    print("Installing library...")
    subprocess.run(['sudo', 'apt', 'install', 'gcc'])
    subprocess.run(['sudo', 'venv/bin/pip', 'install', 'numpy'])
    subprocess.run(['sudo', 'venv/bin/pip', 'install', 'flask_sslify'])
    subprocess.run(
        ['sudo', 'venv/bin/pip', 'install', 'keyboard', 'melopero_lsm9ds1', 'requests', 'wifi', 'bluepy', 'GPIO',
         'RPi.GPIO', 'pyOpenSSL', 'pandas', 'datetime', 'pillow', 'scipy', 'luma.core', 'luma.oled', 'matplotlib'])


def copy_configs():
    """
    Copy configuration files to appropriate directories.
    """
    subprocess.run(['sudo', 'rm', '-r', '/lib/ips_project'])
    subprocess.run(['sudo', 'rm', '-r', '/etc/ips_project'])
    subprocess.run(['sudo', 'mkdir', '/usr/lib/ips_project'])
    subprocess.run(['sudo', 'mkdir', '/etc/ips_project'])
    subprocess.run(['sudo', 'cp', '-a','*', '/usr/lib/ips_project/'])


def main():
    if os.getuid():
        sys.exit('You need root access to install!')

    print("\n" * 2 + "#" * 35)
    print("###  Indoor Positioning System  ###")
    print("###   Indoor Navigation System  ###")
    print("### Based on Geomagnetic Field  ###")
    print("###    Box di Acquisizione      ###")
    print("#" * 35 + "\n")

    install_ans = input("Sei pronto per eseguire il commit delle modifiche al sistema? [y/N]: ")

    if install_ans.lower() == 'y':
        install_prereqs()
        copy_configs()
    else:
        print("\n" * 2 + "=" * 51)
        print("-" * 51)
        print("\nIPS Installazione Annullata. Nothing changed...\n")
        print("-" * 51)
        print("=" * 51 + "\n" * 2)
        sys.exit()

    print("\n" * 2 + "#" * 41)
    print("##### Indoor Positioning System Installazione Completata  #####")
    print("#" * 41 + "\n")

    # TODO: replace with new wifi_manager_installer

    # print("Installare plugin WiFi per la configurazione della rete")
    # wifi_ans = input("Vuoi farlo adesso? [y/N]: ")
    # print("\n" * 2)

    # if wifi_ans.lower() == 'y':
    #     os.chdir('wifi')
    #     os.system('sudo python3 initial_setup.py')

    print("\n" * 2)


if __name__ == '__main__':
    main()
