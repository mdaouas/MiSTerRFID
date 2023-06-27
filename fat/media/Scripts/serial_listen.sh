#!/bin/bash

ttydev="/dev/ttyACM0"

WAITEND=$((SECONDS+30))
while !  [ -c "${ttydev}" ] && [ ${SECONDS} -lt ${WAITEND} ]; do	
	sleep 0.1
done

if [ -c "${ttydev}" ]; then 	
	export PATH="/media/fat/Scripts:$PATH"
	stty 115200 -F "${ttydev}" raw -echo
	bash <"${ttydev}"
fi
