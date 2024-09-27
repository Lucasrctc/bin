while true; do for i in {1..3}; do sleep 1500; xdotool mousemove 370 330 click 1 mousemove restore; echo "d"; done; sleep 1; xdotool mousemove 160 250 click 1 mousemove restore; echo "Done"; done

