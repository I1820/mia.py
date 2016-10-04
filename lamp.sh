#!/bin/bash
# In The Name Of God
# ========================================
# [] File Name : lamp.sh
#
# [] Creation Date : 21-09-2016
#
# [] Improved By : Iman Tabrizian (tabrizian@outlook.com)
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================

i1820_address=${1:-"192.168.128.90"}
node_id=${2:-"066156d8-df62-5894-809b-d51ec5a2ff3d"}

echo "[I1820] using $i1820_address as I1820 server"
echo "[I1820] using $node_id as your target RPi ID."

# Trun
# parameter 1: lamp node - string
# parameter 2: lamp identification - string
# parameter 3: true -> on | false -> off - bool
turn() {
	curl -X PUT -H "Content-Type: application/json" -d "{
		\"type\": \"lamp\",
		\"rpi_id\": \"$node_id\",
		\"device_id\": \"$1:$2\",
		\"settings\": {
			\"on\": $3
		}
	}" "$i1820_address:8080/thing"
	echo ""
	echo "=============================================================================="
	sleep 2
}

bandari() {
  for i in `seq 1 9`; do
    turn 1 $i true
    turn 2 $i true
  done
  for i in `seq 1 9`; do
    turn 1 $i false
    turn 2 $i false
  done
}

zabdari() {
  turn 1 1 true
  turn 2 1 true
  turn 1 5 true
  turn 2 5 true
  turn 1 9 true
  turn 2 9 true
  turn 1 7 true
  turn 2 7 true
  turn 1 3 true
  turn 2 3 true
  turn 1 1 false
  turn 2 1 false
  turn 1 5 false
  turn 2 5 false
  turn 1 9 false
  turn 2 9 false
  turn 1 7 false
  turn 2 7 false
  turn 1 3 false
  turn 2 3 false
}

osPS3=$PS3
PS3="[I1820] Please choose your way [ENTER to list options]:"
select t in "Let's do a bandari" "Let's do a zabdari" "Quit"; do
	if [ ! -z "$t" ]; then
		case $REPLY in
			1)
				bandari
				break
				;;
			2)
				zabdari
				break
				;;
			3)
				exit
				;;
		esac
	else
		echo "$REPLY in not a valid option"
	fi
done
PS3=$oPS3
