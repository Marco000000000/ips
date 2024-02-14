# Wi-Fi Configuration Page

This project provides a simple web-based interface for configuring and managing Wi-Fi connections on a device. It consists of a Flask web application and supporting scripts to facilitate the setup and management of Wi-Fi networks.

## Project Structure

- `config_wifi_page/`: Directory containing the main application files.
    - `wifi_manager.py`: Flask web application for managing Wi-Fi connections.
- `install.py`: Installation script for setting up the Wi-Fi configuration page and associated services.
- `uninstall.py`: Uninstallation script for removing the Wi-Fi configuration page and associated services.
- `requirements.txt`: List of Python dependencies required for running the application.

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the installation script using Python:

    ```bash
    sudo python install.py
    ```

4. Follow the prompts to set up the Wi-Fi hotspot and configure the auto-run service.

## Usage

1. After installation, access the Wi-Fi configuration page by navigating to the device's IP address in a web browser.
2. The web interface allows you to scan for available Wi-Fi networks, select a network, and enter the password to connect.
3. Once connected, the device should be able to access the internet using the configured Wi-Fi network.

## Uninstallation

To remove the Wi-Fi configuration page and associated services:

1. Run the uninstallation script:

    ```bash
    sudo python uninstall.py
    ```

2. Follow the prompts to stop and disable the hotspot service, remove the service file, delete the application folder, and remove the created Wi-Fi hotspot.
