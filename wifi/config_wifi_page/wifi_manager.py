import subprocess

from flask import Flask, request

WIFI_DEVICE = "wlan0"


def scan_wifi_networks():
    """Scan for available Wi-Fi networks."""
    try:
        result = subprocess.check_output(
            ["nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname",
             WIFI_DEVICE])
        ssids_list = result.decode().split('\n')
        return [ssid.removeprefix("SSID:") for ssid in ssids_list if ssid.startswith("SSID:")]
    except subprocess.CalledProcessError as e:
        print(f"Error scanning Wi-Fi networks: {e}")
        return []


def render_wifi_form(ssids):
    """Render the Wi-Fi network selection form."""
    options = ''.join([f'<option value="{ssid}">{ssid}</option>' for ssid in ssids])
    form = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wi-Fi Control</title>
        </head>
        <body>
            <h1>Wi-Fi Control</h1>
            <form action="/submit" method="post">
                <label for="ssid">Choose a Wi-Fi network:</label>
                <select name="ssid" id="ssid">
                    {options}
                </select>
                <p/>
                <label for="password">Password: <input type="password" name="password"/></label>
                <p/>
                <input type="submit" value="Connect">
            </form>
        </body>
        </html>
    """
    return form


def connect_to_wifi(ssid, password):
    """Connect to the specified Wi-Fi network."""
    try:
        connection_command = ["nmcli", "--colors", "no", "device", "wifi", "connect", ssid, "ifname", WIFI_DEVICE]
        if password:
            connection_command.extend(["password", password])
        result = subprocess.run(connection_command, capture_output=True, text=True, check=True)
        # Modify the connection to auto-connect and increase priority
        modify_command = ["nmcli", "connection", "modify", ssid, "connection.autoconnect", "yes",
                          "connection.autoconnect-priority", "100"]
        subprocess.run(modify_command, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error connecting to Wi-Fi network: {e}"


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """Render the Wi-Fi network selection form."""
    ssids = scan_wifi_networks()
    return render_wifi_form(ssids)


@app.route("/submit", methods=['POST'])
def submit():
    """Handle form submission and connect to the selected Wi-Fi network."""
    ssid = request.form.get('ssid')
    password = request.form.get('password')
    if ssid:
        result_message = connect_to_wifi(ssid, password)
        return f"<p>{result_message}</p>"
    else:
        return "<p>Error: Please select a Wi-Fi network.</p>"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
