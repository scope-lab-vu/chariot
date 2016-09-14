#! /bin/sh

case "$1" in
    start)
		echo "Starting " "$2" " nodes of template $3"
		for ((i=1; i<=$2; i++))
		do
			NodeName="$3_$i"
			python ../SimulateNodeActivity.py --nodeName $NodeName --nodeTemplate $3 --port 0 --action "start"
		done
		;;
	stop)
		echo "Stopping " "$2" " nodes"
		for ((i=1; i<=$2; i++))
		do
			NodeName="node""$i"
			python ../SimulateNodeActivity.py --nodeName $NodeName --action "stop"
		done
		;;
	*)

    exit 1
    ;;
esac

exit 0