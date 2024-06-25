for i in {0..3}
	do for j in {0..3}
		do xdotool mousemove 3398 493 mousemove_relative $((i*188)) $((j*188)) mousedown 1
	 	sleep .5
		xdotool mousemove 2857 1127 mouseup 1
		sleep .5
	done
 done
 xdotool type "i"
 sleep .5
 xdotool mousemove 2500 1060
