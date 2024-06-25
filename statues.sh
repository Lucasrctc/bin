xdotool mousemove 2713 880 click 1 type "5000"
for i in {0..3}
	do for j in {0..3}
		do xdotool mousemove 3021 611 mousedown 1
	 	sleep .5
		xdotool mousemove 3398 493 mousemove_relative $((i*188)) $((j*188)) mouseup 1
		sleep .5
	done
 done
 xdotool type "i"
sleep .5
xdotool mousemove 2105 271
