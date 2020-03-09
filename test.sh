#!/bin/bash
#RPiIP=$(hostname -I) || true
#if [ "$RPiIP" ]; then
#  printf "$RPiIPd\n"
#fi

## This should grab the IP address of the RPi and display - Heath
RPiIP=$(hostname -I) || true
if [ "$RPiIP" ]; then
  #printf "My IP address is %s\n" "$RPiIP"
echo "Calling python scrip from shell"
python test.py "$RPiIP"

fi
