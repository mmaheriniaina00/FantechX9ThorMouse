# Fantech X9 Thor Mouse LED Controller

A simple command-line utility to control the LED on Fantech X9 Thor gaming mice without requiring a GUI.

## Features

- Turn off mouse LED with a single command
- Lightweight CLI tool (no GUI dependencies)
- Auto-run on system startup support
- Clear error messages and status feedback

## Requirements

- Python 3.x
- PyUSB library
- Linux (tested on Fedora)
- USB access permissions (may require root/sudo)

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:mmaheriniaina00/FantechX9ThorMouse.git
   cd FantechX9ThorMouse
   ```

2. **Install dependencies:**
   ```bash
   pip install pyusb
   ```
   
   Or on Fedora/RHEL:
   ```bash
   sudo dnf install python3-pyusb
   ```

3. **Make the script executable:**
   ```bash
   chmod +x led_off.py
   ```

## Usage

### Basic Usage

Turn off the LED:
```bash
python led_off.py
```

Or if you made it executable:
```bash
./led_off.py
```

### With sudo (if permission denied)

```bash
sudo python led_off.py
```

## Auto-run on Startup

### Method 1: Systemd Service (Recommended)

1. **Copy script to system location:**
   ```bash
   sudo cp led_off.py /usr/local/bin/mouse-led-off.py
   sudo chmod +x /usr/local/bin/mouse-led-off.py
   ```

2. **Create systemd service file:**
   ```bash
   sudo nano /etc/systemd/system/mouse-led-off.service
   ```

3. **Add the following content:**
   ```ini
   [Unit]
   Description=Turn off Fantech X9 Thor Mouse LED
   After=multi-user.target
   Wants=multi-user.target

   [Service]
   Type=oneshot
   ExecStart=/usr/bin/python3 /usr/local/bin/mouse-led-off.py
   RemainAfterExit=yes
   User=root

   [Install]
   WantedBy=multi-user.target
   ```

4. **Enable and start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable mouse-led-off.service
   sudo systemctl start mouse-led-off.service
   ```

5. **Verify it's running:**
   ```bash
   sudo systemctl status mouse-led-off.service
   ```

### Method 2: Udev Rule (Triggers when mouse is plugged in)

1. **Copy script to system location** (if not already done):
   ```bash
   sudo cp led_off.py /usr/local/bin/mouse-led-off.py
   sudo chmod +x /usr/local/bin/mouse-led-off.py
   ```

2. **Create udev rule:**
   ```bash
   sudo nano /etc/udev/rules.d/99-fantech-mouse.rules
   ```

3. **Add the following line:**
   ```
   ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="18f8", ATTR{idProduct}=="0fc0", RUN+="/usr/bin/python3 /usr/local/bin/mouse-led-off.py"
   ```

4. **Reload udev rules:**
   ```bash
   sudo udevadm control --reload-rules
   ```

## Permissions Setup (Optional)

To run without sudo, create a udev rule for USB access:

1. **Create udev rule file:**
   ```bash
   sudo nano /etc/udev/rules.d/50-fantech-mouse.rules
   ```

2. **Add the following line** (replace `username` with your username):
   ```
   SUBSYSTEM=="usb", ATTR{idVendor}=="18f8", ATTR{idProduct}=="0fc0", MODE="0666", GROUP="plugdev"
   ```

3. **Add your user to the plugdev group:**
   ```bash
   sudo usermod -aG plugdev $USER
   ```

4. **Reload udev rules and replug the mouse:**
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

5. **Log out and log back in** for group changes to take effect.

## Troubleshooting

### "Device not found" error
- Ensure the mouse is plugged in
- Verify USB connection is working
- Try replugging the mouse

### "Insufficient permissions" error
- Run with `sudo`
- Or set up udev rules as described above

### Service not starting on boot
- Check service status: `sudo systemctl status mouse-led-off.service`
- View logs: `sudo journalctl -u mouse-led-off.service`
- Ensure the script path in the service file is correct

## Related Projects

This script is based on the [Fantech X9 Thor driver](https://github.com/GuessWhatBBQ/FantechX9ThorDriver) which provides a full GUI for configuring DPI, colors, and LED modes.

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Your Name

## Acknowledgments

- Based on the Fantech X9 Thor Linux driver
- Uses PyUSB for USB communication
