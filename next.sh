#!/bin/bash
# In The Name Of God
# ========================================
# [] File Name : next.sh
#
# [] Creation Date : 04-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
for w in `xdotool search LibreOffice`; do
	xdotool key --window $w Page_Down
done
