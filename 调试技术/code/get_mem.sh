#!/bin/sh


# zhengming@Fiberhome.com
# get mem info from devices


for PID in `ps | grep -v '[[].*[]]$' | awk '!/^PID/ { print $1 }'`
do
	if [ -r /proc/$PID/cmdline ]
	then
		echo "Process: `cat /proc/$PID/cmdline 2>/dev/null`"
		echo "Pid: $PID"
		grep -e 'VmPeak' -e 'VmSize' -e 'VmHWM:' -e 'VmRSS:' /proc/$PID/status
		cat /proc/$PID/smaps
	fi
done > /var/mem.log