import os
import sys

import setup_lib

if os.getuid():
    sys.exit('You need root access to install!')

print()
print()
print("###################################")
print("###  Indoor Positioning System  ###")
print("###   Indoor Navigation System  ###")
print("### Based on Geomagnetic Field  ###")
print("###    Box di Acquisizione      ###")
print("###################################")
print()
install_ans = input("Sei pronto per eseguire il commit delle modifiche al sistema? [y/N]: ")

if (install_ans.lower() == 'y'):
    setup_lib.install_prereqs()
    setup_lib.copy_configs()
else:
    print()
    print()
    print("===================================================")
    print("---------------------------------------------------")
    print()
    print("IPS Installazione Annullata. Nothing changed...")
    print()
    print("---------------------------------------------------")
    print("===================================================")
    print()
    print()
    sys.exit()

print()
print()
print("#####################################")
print("##### Indoor Positioning System Installazione Completata  #####")
print("#####################################")
print()
print()
# print("Installare plugin WiFi per la configurazione della rete")
# wifi_ans = input("Vuoi farlo adesso? [y/N]: ")
# print()
# print()

# if wifi_ans.lower() == 'y':
#    os.system('cd wifi')
#    os.system('sudo python3 wifi/initial_setup.py')


print()
print()
