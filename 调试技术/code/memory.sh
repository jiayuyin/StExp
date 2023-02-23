#!/bin/sh

intel=$1
count=$2
LOG_PATH=/var
if [[ -z "$intel"  ]]
then
        echo "no input param,using default 10 minutes as interval"
        intel=600
		count=200
fi
echo 'start test '  
echo "interval time = $intel  "
echo "count = $count "  
echo ========please wait=======  
i=1  
#rtl need mempool info, need to enbale this
mempoolenable=1
if [[ "$mempoolenable" == "1" ]]
then
        echo "start mount debug fs"
        mount -t debugfs nodev /sys/kernel/debug/
fi

rm ${LOG_PATH}/*.txt

while [[ $i -le $count ]]  
do  
	echo current running: $i
	time=`date "+%Y-%m-%d %H:%M:%S"`
	echo "$time" >> ${LOG_PATH}/meminfolog.txt
	cat /proc/meminfo |awk '{print $2}' >> ${LOG_PATH}/meminfolog.txt

	if [[ "$mempoolenable" == "1" ]];then
		echo scan > /sys/kernel/debug/kmemleak
		sleep 3
		echo "$time" >> ${LOG_PATH}/memleaklog.txt
		cat /sys/kernel/debug/kmemleak >> ${LOG_PATH}/memleaklog.txt
	fi
  let i++  
  echo 'Waiting for 10 min'
  sleep $intel  
done  
echo =========all done success==============