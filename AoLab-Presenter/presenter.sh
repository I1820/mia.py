#!/bin/bash
# In The Name Of God
# ========================================
# [] File Name : presenter.sh
#
# [] Creation Date : 04-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================

for w in `xdotool search xpdf`; do
	xdotool key --window $w $1
done
