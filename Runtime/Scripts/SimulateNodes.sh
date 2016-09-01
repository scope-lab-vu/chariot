#! /bin/sh

case "$1" in
    start)
		echo "Starting " "$2" " nodes"
		for ((i=1; i<=$2; i++))
		do
			NodeName="node""$i"
			PortNumber=$((7000+$i))
			python ../SimulateNodeActivity.py --nodeName $NodeName --nodeTemplate "SimpleNodeTemplate" --port $PortNumber --action "start" &
		done
		;;
	stop)
		echo "Stopping " "$2" " nodes"
		for ((i=1; i<=$2; i++))
		do
			NodeName="node""$i"
			PortNumber=$((7000+$i))
			python ../SimulateNodeActivity.py --nodeName $NodeName --nodeTemplate "SimpleNodeTemplate" --port $PortNumber --action "stop" &
		done
		;;
	*)

    exit 1
    ;;
esac

exit 0