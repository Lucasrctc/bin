echo "start"
i=1
while true
do
	echo "$i"
	i=$((i+1))
	xdotool getwindowfocus mousemove --sync 200 600 click 1 windowfocus --sync %1 mousemove restore 
	sleep 60
done
