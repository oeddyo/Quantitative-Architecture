#!/bin/bash
source /Users/eddiexie/Software/vpython/bin/activate
source /Users/eddiexie/.bash_profile
date
echo 'Launch venue statistics monitor'
nohup python /Users/eddiexie/work/Quantitative-Architecture/venue_stats_monitor.py 1>> /Users/eddiexie/work/Quantitative-Architecture/runtines/log.txt &

