# RaspberryPi Hotspot and Wi-Fi Manager

The RaspberryPi Hotspot and Wi-Fi Manager project offers a simple solution for configuring Wi-Fi connections on a
Raspberry Pi. It creates a hotspot to interface with the Raspberry Pi and includes a Flask-based web application (
wifi_manager.py) that interacts with NetworkManager (nmcli) to manage Wi-Fi connections.

## Installation

To set up the project on your Raspberry Pi, follow these steps:

1. Clone or download the project repository to your Raspberry Pi.
2. Navigate to the project directory.
3. Run the installation script using Python. You can specify the hotspot name and password during installation. If no
   arguments are provided, default values will be used (SSID: RaspHotspot, PASS: password).

    ```bash
    sudo python3 -B src/install.py [hotspot_name hotspot_password]
    ```

4. Follow the prompts to set up the Wi-Fi hotspot and configure the auto-run service.

## Usage

Here's how to use the Wi-Fi configuration page:

1. Connect to the hotspot broadcasted from the Raspberry Pi.
2. Open a web browser and navigate to the Raspberry Pi's IP address (typically 10.42.0.1).
3. The web interface will scan for available Wi-Fi networks and display them. Select your desired network from the list.
4. Enter the password for the selected Wi-Fi network.
5. Once connected, the Raspberry Pi should have internet access through the configured Wi-Fi network.
6. If the Wi-Fi connection is lost, the Raspberry Pi will automatically broadcast its hotspot again, allowing for
   reconfiguration.

## Uninstallation

To remove the Wi-Fi configuration page and associated services:

1. Run the uninstallation script:

    ```bash
    sudo python -B src/uninstall.py
    ```

This will remove all configurations and settings made during installation.

Feel free to reach out if you encounter any issues or have any questions!