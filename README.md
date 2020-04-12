# dzen2-bar
Basic bar generator for dzen2.

For those who struggle to find some simple examples of dzen2 bar/panel setup.

This is a pretty basic setup, written in Python, could be called a fork of the script published here:
https://www.linuxquestions.org/questions/linux-general-1/dzen2-status-bar-script-837042/
That was a page where I finally found a super usefull and clear example of how to deal with dzen2.

What's there:

* Time/date;
* RAM monitoring (as a horizontal bar);
* Volume indicator;
* Battery with percents and status (Charging/discharging);
* WiFi (shows SSID and connection quality).

Installation:
- Clone or download this repository;
- Put 'dzen2' folder in yout $HOME/.config directory;
- Give all files execution permissions;
- Run 'dzen2-startup.sh' script.

Requirements:
- Python (probably version 3+);
- amixer - for volume indicator;
- acpi - for battery indicator (I think it's installed by default on every distribution);
- for WiFi check out your interface names. By default 'wifi.py' script uses "wlp2s0" name for WiFi adapter.
On some distros you'll need to change it to "wlan0" (see 'wifi.py' file).
