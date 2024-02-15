import subprocess


def install_prereqs():
    """
    Install necessary packages and libraries.
    """
    subprocess.run(['sudo', 'apt-get', 'install', 'python3-pip', 'libglib2.0-dev'])
    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'python3', 'python3-rpi.gpio', 'python3-pip', '-y'])

    print("Installing Flask web server...")
    subprocess.run(['sudo', '.venv/bin/pip', 'install', 'flask'])
    print("Installing library...")
    subprocess.run(['sudo', 'apt', 'install', 'gcc'])
    subprocess.run(['sudo', '.venv/bin/pip', 'install', 'numpy'])
    subprocess.run(['sudo', '.venv/bin/pip', 'install', 'flask_sslify'])
    subprocess.run(
        ['sudo', '.venv/bin/pip', 'install', 'keyboard', 'melopero_lsm9ds1', 'requests', 'wifi', 'bluepy', 'GPIO',
         'RPi.GPIO', 'pyOpenSSL', 'pandas', 'datetime', 'pillow', 'scipy', 'luma.core', 'luma.oled', 'matplotlib'])


def copy_configs():
    """
    Copy configuration files to appropriate directories.
    """
    subprocess.run(['sudo', 'rm', '-r', '/lib/ips_project'])
    subprocess.run(['sudo', 'rm', '-r', '/etc/ips_project'])
    subprocess.run(['sudo', 'mkdir', '/usr/lib/ips_project'])
    subprocess.run(['sudo', 'mkdir', '/etc/ips_project'])
    subprocess.run(['sudo', 'cp', '-a', '*', '/usr/lib/ips_project/'])
