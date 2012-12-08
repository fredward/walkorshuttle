#!/bin/bash
MY_PATH="`dirname \"$0\"`"
TIME=`date +%s`
CMD="python "$MY_PATH"/s_r_request.py"
echo `$CMD`
wait
while [ 'true' ]
do
	if [ $((`date +%s` - $TIME)) -ge 1 ]
	then
		if [ $((`date +%s` % 30)) -eq 0 ]
		then
			CMD="python "$MY_PATH"/s_r_request.py"
			echo `$CMD`
			wait
			TIME=`date +%s`
			echo $TIME
		fi
		CMD="python "$MY_PATH"/v_request.py"
		echo `$CMD`
		wait
		TIME=`date +%s`
		echo $TIME
	fi
	
done