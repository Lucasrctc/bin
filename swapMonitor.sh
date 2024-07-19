#!/bin/bash
a=`xrandr --listactivemonitors | grep DP-0`
if [ -z "$a" ]; then
	xrandr --output DP-2 --primary --right-of HDMI-0 --mode 2560x1440 --rate 120.00; xrandr --output DP-0 --auto --right-of DP-2
else
	xrandr --output HDMI-0 --primary --auto; xrandr --output DP-0 --off; xrandr --output DP-2 --off
fi
