import os

import sys

import setup_lib


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
        setup_lib.install_prereqs()
        setup_lib.copy_configs()
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
