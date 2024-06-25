#!/bin/bash

MOUSE_ID=$(xinput --list | grep -i -m 1 'mouse' | grep -o 'id=[0-9]\+' | grep -o '[0-9]\+')

STATE8=$(xinput --query-state $MOUSE_ID | grep 'button\[8')

echo $STATE8

while [[ $STATE8 == *up* ]]; do
	STATE8=$(xinput --query-state $MOUSE_ID | grep 'button\[8')
	xdotool click 1
	sleep 2
	./statues.sh
	sleep .5
	xdotool click 1
	sleep 2
	./delstatues.sh
done
