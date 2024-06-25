echo "start"
sleep 3
for i in {1..50}; do
	echo $i
	xdotool key c
	sleep .5
	xdotool mousemove 3100 500 click 1 mousemove restore
	sleep .5
	xdotool mousemove 1800 500 click 1 mousemove restore
	sleep .5
	xdotool key c
	sleep .5
	xdotool key c
	xdotool mousedown 1
	sleep .5
	xdotool mouseup 1
done
