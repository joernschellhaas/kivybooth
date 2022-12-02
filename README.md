kivybooth
=========

A fotobooth application based on Kivy, intended to run on a Raspberry Pi with a touchscreen (obviously) and a CUPS enabled printer.


## Getting started
 * The application's dependencies can be installed on a Raspberry Pi in a venv using the `res/app-setup.sh` script.
 * After installation, try the Kivy demo from `venv/share/kivy-examples/demo/showcase`.
 * I had to change my `~/.kivy/config.ini` for the touchscreen to work, see `res/kivy/config.ini`.
 * To start the application as a service, a systemd config file is available at `res/kivybooth.service`.
 * You should be able to also debug the application using a Visual Studio Code run configuration.


## Running on Windows
For development puposes, the application is intended to also be run on Windows computers. Since a few things will not be available on Windows (CUPS, GPIO, gphoto2(?)), the application will ignore these if the `KBOOTH_EMULATE` environment variable is set. When using `res/app-setup.bat` to create the virtual environment on Windows, it should be set automagically.


## Printer Configuration
`raspbian-setup.sh` should have installed the `cups` package on your RPi. This allows you to use the CUPS web interface to configure and, more important, troubleshoot your driver. By default, the web UI will be accessible from localhost (that is, the RPi itself) only. You probably want to access it from your development PC. The easiest and most secure way to achieve that is to set up a SSH port forwarding with a command like `ssh root@photobooth -L 6310:localhost:631`. Then, you can access the web UI via http://localhost:6310/ (tested on my Windows 10 PC).

What is needed to configure a printer correctly is hard to tell. To get a HP DeskJet 3760 to work, I additionally installed the `hplip` package and then cofigured the printer using `hp-setup -i`. I nevertheless had to restart the RPi before the printer would work correctly. You should probably try that before randomly installing things. I was however more successful with installing an Epson ET-2710, wich did not require any additional drivers. Although, what must be noted is that in this case installing the manufacturer's driver move than doubled the print speed (to 50 sec in "high" quality and 3 min in "photo" quality).


## References
 * [Kivy installation on RPi](https://kivy.org/doc/stable/installation/installation-rpi.html)
 * [Touchscreen Documentation](https://wiki.52pi.com/index.php/7-Inch-1024x600_Capacitive_Touch_Screen_DIY_Kit_SKU:_EP-0084) (I used a [7'' screen from Pollin](https://www.pollin.de/p/7-17-78-cm-display-set-mit-touchscreen-hdmi-vga-video-810841))
 * [Systemd Service Tutorial (DE)](https://wiki.ubuntuusers.de/Howto/systemd_Service_Unit_Beispiel/)
