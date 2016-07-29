#! /bin/sh

case "$1" in
    start)
        echo "Adding nodes: 13 edison, 13 wifi_cam, 1 entry_terminal"
        fab -H s74,s75,s76,s77,s78,s79,s80,s81,s82,s83,s84,s85,s86 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=edison,monitoringServer=zk
        fab -H s87,s88,s89,s90,s91,s92,s93,s94,s95,s96,s97,s98,s99 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=wifi_cam,monitoringServer=zk
        fab -H s100 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=entry_terminal,monitoringServer=zk
        ;;
    stop)
        echo "Tearing down first update"
        fab -H s74,s75,s76,s77,s78,s79,s80,s81,s82,s83,s84,s85,s86,s87,s88,s89,s90,s91,s92,s93,s94,s95,s96,s97,s98,s99,s100 -f FabFile.py stop_node_membership
        ;;
    *)

    echo "Usage: NodeUpdateThird.sh {start | stop}"
    exit 1
    ;;
esac

exit 0

