#!/bin/bash

for w in $(xdotool search xpdf); do
	xdotool key --window "$w" "$1"
done
