#!/bin/bash
# In The Name Of God
# ========================================
# [] File Name : lamp.sh
#
# [] Creation Date : 21-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================

for i in `seq 1 8`; do
	curl -X PUT -H "Content-Type: application/json" -d "{
		\"type\": \"lamp\",
		\"rpi_id\": \"b07882d6-5c28-597b-89f9-d250f74b0bad\",
	      	\"device_id\": \"1:5\",
	      	\"settings\": {
			\"on\": true
		}
	}" "iot.ceit.aut.ac.ir:58902/thing"
	curl -X PUT -H "Content-Type: application/json" -d "{
		\"type\": \"lamp\",
		\"rpi_id\": \"b07882d6-5c28-597b-89f9-d250f74b0bad\",
	      	\"device_id\": \"1:5\",
	      	\"settings\": {
			\"on\": false
		}
	}" "iot.ceit.aut.ac.ir:58902/thing"
done
