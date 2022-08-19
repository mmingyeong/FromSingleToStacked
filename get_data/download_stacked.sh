#!/bin/bash

wave_list="g r i"
num_list="1 2 3 4 5 6"

for wave in $wave_list
do
   for num in $num_list
   do 
      cd /home/mingyeong/workflow/data/stacked/106/$wave/cc$num
      chmod +x get_${wave}106_cc${num}_axel.sh
      ./get_${wave}106_cc${num}_axel.sh
    done
done

for wave in $wave_list
do
   for num in $num_list
   do 
      cd /home/mingyeong/workflow/data/stacked/206/$wave/cc$num
      chmod +x get_${wave}206_cc${num}_axel.sh
      ./get_${wave}206_cc${num}_axel.sh
    done
done