#! /bin/sh

case "$1" in
    start)
        echo "Starting Resource Monitor"

        DM_PID=`ps -x | grep "DeploymentManager.py" | grep -v "grep" | awk '{print $1}'`
        NM_PID=`ps -x | grep "NodeMembership.py" | grep -v "grep" | awk '{print $1}'`
        if [ "$DM_PID" != "" ] && [ "$NM_PID" != "" ]; then
            echo "Ensuring we start with clean logs"
            rm -rf /home/ubuntu/tmpResourceMonitor
            mkdir -p /home/ubuntu/tmpResourceMonitor
            python /home/ubuntu/workspace/chariot/Runtime/ResourceMonitor.py --dmPID $DM_PID --nmPID $NM_PID &
        else
            echo "Invalid DeploymentManager or NodeMembership PID."
        fi
        ;;
    stop)
        echo "Stopping ResourceMonitor"
        pkill -f "ResourceMonitor"
        ;;
    *)

    echo "Usage: ResourceMonitor.sh {start | stop}"
    exit 1
    ;;
esac

exit 0
