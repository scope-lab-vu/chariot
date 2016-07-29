#! /bin/sh

case "$1" in
    start)
        echo "Starting NodeMembershipWatcher"
        echo "Ensuring we start with clean logs"
        rm -rf /home/ubuntu/tmpNodeMembershipWatcher
        mkdir -p /home/ubuntu/tmpNodeMembershipWatcher
        python -u /home/ubuntu/workspace/chariot/Runtime/NodeMembershipWatcher.py --monitoringServer $2 --mongoServer $3 --managementEngine $4 >> /home/ubuntu/tmpNodeMembershipWatcher/MembershipWatcher.log &
        ;;
    stop)
        echo "Stopping NodeMembershipWatcher"
        pkill -f "NodeMembershipWatcher"
        ;;
    *)

    echo "Usage: NodeMembershipWatcher.sh {start <monitoringServer> <mongoServer> <managingEngine> | stop}"
    exit 1
    ;;
esac

exit 0
