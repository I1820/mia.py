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

turn() {
	curl -X PUT -H "Content-Type: application/json" -d "{
		\"type\": \"lamp\",
		\"rpi_id\": \"066156d8-df62-5894-809b-d51ec5a2ff3d\",
		\"device_id\": \"1:$1\",
		\"settings\": {
			\"on\": $2
		}
	}" "192.168.128.90:8080/thing"
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

if [ "$1" = "bandari" ]; then
  echo "Let's do a bandari"
  bandari
elif [ "$1" = "zabdari" ]; then
  echo "Let's do a zabdari"
  zabdari
fi
