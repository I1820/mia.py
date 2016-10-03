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
node_id="6c6319f9-bbc3-5fe0-9475-c12695250865"
echo "[I1820] using $i1820_address as I1820 server"

# Trun
# parameter 1: lamp identification - string
# parameter 2: true -> on | false -> off - bool
turn() {
	curl -X PUT -H "Content-Type: application/json" -d "{
		\"type\": \"lamp\",
		\"rpi_id\": \"$node_id\",
		\"device_id\": \"1:$1\",
		\"settings\": {
			\"on\": $2
		}
	}" "$i1820_address:8080/thing"
	sleep 1
}

bandari() {
  status=true
  for i in `seq 1 9`; do
    turn $i true
  done
  for i in `seq 1 9`; do
    turn $i false
  done
}

zabdari() {
  turn 1 true
  turn 5 true
  turn 9 true
  turn 7 true
  turn 1 false
  turn 5 false
  turn 9 false
  turn 7 false
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
