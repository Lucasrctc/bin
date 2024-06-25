echo "start"
for i in {1..10000000}; do
	echo $i
	xdotool getwindowfocus mousemove 220 1675 click 1 windowfocus --sync %1 mousemove restore 
	sleep 300
done
