#!/bin/bash
# In The Name Of God
# ========================================
# [] File Name : lamp.sh
#
# [] Creation Date : 21-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
for i in `seq 1 9`; do
	curl -X PUT -H "Content-Type: application/json" -d "{
		\"type\": \"lamp\",
		\"rpi_id\": \"066156d8-df62-5894-809b-d51ec5a2ff3d\",
		\"device_id\": \"1:$i\",
		\"settings\": {
			\"on\": true
		}
	}" "192.168.128.90:8080/thing"	
done
