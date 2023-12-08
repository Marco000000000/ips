import os

def install_prereqs():
	os.system('sudo apt-get install python3-pip libglib2.0-dev') 
	os.system('apt update')

	os.system('apt install python3 python3-rpi.gpio python3-pip -y')
	print("Installing Flask web server...")
	os.system('sudo .venv/bin/pip install flask ')
	print("Installing library...")
	os.system('sudo apt install gcc  ')
	os.system('sudo .venv/bin/pip install numpy  ')
	os.system('sudo .venv/bin/pip install flask_sslify  ')

	
	os.system('sudo .venv/bin/pip install keyboard  ')
	os.system('sudo .venv/bin/pip install melopero_lsm9ds1  ')
	os.system('sudo .venv/bin/pip install requests  ')
	os.system('sudo .venv/bin/pip install wifi  ')
	os.system('sudo .venv/bin/pip install bluepy  ')
	os.system('sudo .venv/bin/pip install GPIO  ')
	os.system('sudo .venv/bin/pip install RPi.GPIO  ')
	os.system('sudo .venv/bin/pip install pyOpenSSL  ')
	os.system('sudo .venv/bin/pip install pandas  ')
	os.system('sudo .venv/bin/pip install datetime  ')
	os.system('sudo .venv/bin/pip install pillow  ')
	os.system('sudo .venv/bin/pip install scipy  ')
	os.system('sudo .venv/bin/pip install luma.core  ')
	os.system('sudo .venv/bin/pip install luma.oled  ')
	os.system('sudo .venv/bin/pip install matplotlib  ')
	#os.system('clear')
	#testare completezza librerie

def copy_configs():
	os.system('sudo rm -r /lib/ips_project')
	os.system('sudo rm -r /etc/ips_project')
	os.system('sudo mkdir /usr/lib/ips_project')
	os.system('sudo mkdir /etc/ips_project')
	os.system('sudo cp -a * /usr/lib/ips_project/')
	
