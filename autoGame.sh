#!/bin/bash

MOUSE_ID=$(xinput --list | grep -i -m 1 'mouse' | grep -o 'id=[0-9]\+' | grep -o '[0-9]\+')

STATE1=$(xinput --query-state $MOUSE_ID | grep 'button\[1')
STATE8=$(xinput --query-state $MOUSE_ID | grep 'button\[8')
STATE9=$(xinput --query-state $MOUSE_ID | grep 'button\[9')
LOCK9=0

COORD="730 955"
DCOORD="$COORD $COORD"
TIME="1000"
RESPAWN="input touchscreen swipe $DCOORD $TIME"
CLICK="input touchscreen swipe $DCOORD 1"

while [[ $STATE8 == *up* ]]; do
	STATE1=$(xinput --query-state $MOUSE_ID | grep 'button\[1')
	STATE8=$(xinput --query-state $MOUSE_ID | grep 'button\[8')
	STATE9=$(xinput --query-state $MOUSE_ID | grep 'button\[9')
	if [[ $STATE9 == *down* ]] && [[ $STATE1 == *down* ]]
	then
		LOCK9="$((1-$LOCK9))"
		echo "locking is $LOCK9"
		while [[ $STATE1 == *down* ]]; do
			STATE1=$(xinput --query-state $MOUSE_ID | grep 'button\[1')
			sleep 0.1
		done
	elif ((LOCK9))
	then 
		echo "RESPAWN"
		adb shell "$RESPAWN"
		sleep 3
		echo "START BATTLE"
		adb shell "$CLICK"
		sleep 13
		echo "END BATTLE"
		adb shell "$CLICK"
		sleep 1
	fi
done

