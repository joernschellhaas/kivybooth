kivybooth
=========

A fotobooth application based on Kivy.


# Getting started
 * The application's dependencies can be installed on a Raspberry Pi in a venv using the `res/app-setup.sh` script.
 * After installation, try the Kivy demo from `venv/share/kivy-examples/demo/showcase`.
 * I had to change my `~/.kivy/config.ini` for the touchscreen to work, see `res/kivy/config.ini`.
 * To start the application as a service, a systemd config file is available at `res/kivybooth.service`.


# References
 * [Kivy installation on RPi](https://kivy.org/doc/stable/installation/installation-rpi.html)
 * [Touchscreen Documentation](https://wiki.52pi.com/index.php/7-Inch-1024x600_Capacitive_Touch_Screen_DIY_Kit_SKU:_EP-0084) (I used a [7'' screen from Pollin](https://www.pollin.de/p/7-17-78-cm-display-set-mit-touchscreen-hdmi-vga-video-810841))
 * [Systemd Service Tutorial (DE)](https://wiki.ubuntuusers.de/Howto/systemd_Service_Unit_Beispiel/)
