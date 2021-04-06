kivybooth
=========

A fotobooth application based on Kivy.


## Getting started
 * The application's dependencies can be installed on a Raspberry Pi in a venv using the `res/app-setup.sh` script.
 * After installation, try the Kivy demo from `venv/share/kivy-examples/demo/showcase`.
 * I had to change my `~/.kivy/config.ini` for the touchscreen to work, see `res/kivy/config.ini`.
 * To start the application as a service, a systemd config file is available at `res/kivybooth.service`.


## Printer Configuration
`raspbian-setup.sh` should have installed the `cups` package on your RPi. This allows you to use the CUPS web interface to configure and, more important, troubleshoot your driver. By default, the web UI will be accessible from localhost (that is, the RPi itself) only. You probably want to access it from your development PC. The easiest and most secure way to achieve that is to set up a SSH port forwarding with a command like `ssh root@photobooth -L 631:localhost:631`. Then, you can access the web UI via http://localhost:631/ (tested on my Windows 10 PC).

What is needed to configure a printer correctly is hard to tell. To get a HP DeskJet 3760 to work, I additionally installed the `hplip` package and then cofigured the printer using `hp-setup -i`. I nevertheless had to restart the RPi before the printer would work correctly. You should probably try that before randomly installing things. I was however more successful with installing an Epson ET-2710, wich did not require any additional drivers.


## References
 * [Kivy installation on RPi](https://kivy.org/doc/stable/installation/installation-rpi.html)
 * [Touchscreen Documentation](https://wiki.52pi.com/index.php/7-Inch-1024x600_Capacitive_Touch_Screen_DIY_Kit_SKU:_EP-0084) (I used a [7'' screen from Pollin](https://www.pollin.de/p/7-17-78-cm-display-set-mit-touchscreen-hdmi-vga-video-810841))
 * [Systemd Service Tutorial (DE)](https://wiki.ubuntuusers.de/Howto/systemd_Service_Unit_Beispiel/)
