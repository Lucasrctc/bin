
a=1
#for i in {1..3}; do
while true; do
	echo $a
	a=$((a+1))
	xdotool getwindowfocus mousemove 2750 450 click 1 windowfocus --sync %1 mousemove restore
	sleep .3
	xdotool getwindowfocus mousemove 3000 450 click 1 windowfocus --sync %1 mousemove restore
	sleep .3
	xdotool getwindowfocus mousemove 3250 450 click 1 windowfocus --sync %1 mousemove restore
	sleep .3
	xdotool getwindowfocus mousemove 3500 450 click 1 windowfocus --sync %1 mousemove restore
	sleep .3
#	xdotool getwindowfocus mousemove 2900 300 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 3150 300 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 3400 300 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 2900 450 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 3150 450 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 3400 450 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 2900 600 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 3150 600 click 1 windowfocus --sync %1 mousemove restore
#	sleep .3
#	xdotool getwindowfocus mousemove 3400 600 click 1 windowfocus --sync %1 mousemove restore
	sleep 60
done
