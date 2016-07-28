#! /bin/sh

case "$1" in
    start)
        echo "Starting NodeMembership"
        echo "Ensuring we start with clean logs"
        rm -rf /home/ubuntu/tmpNodeMembership
        mkdir -p /home/ubuntu/tmpNodeMembership
        python -u /home/ubuntu/workspace/chariot/Runtime/NodeMembership.py --interface $2 --network $3 --nodeTemplate $4 --monitoringServer $5 >> /home/ubuntu/tmpNodeMembership/Membership.log &
        ;;
    stop)
        echo "Stopping NodeMembership"
        pkill -f "NodeMembership"
        ;;
    *)

    echo "Usage: NodeMembership.sh {start <network interface> <network name> <nodeTemplate> <monitoringServer> | stop}"
    exit 1
    ;;
esac

exit 0
