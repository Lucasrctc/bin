#!/bin/bash
B=`pacmd list-sinks|grep \*|cut -c 12`
if [ $B == 0 ]; then
	pacmd set-default-sink alsa_output.pci-0000_00_1f.3.analog-stereo
	echo $B
else 
	pacmd set-default-sink alsa_output.usb-Focusrite_Scarlett_2i2_USB-00.analog-stereo
	echo $B
fi
