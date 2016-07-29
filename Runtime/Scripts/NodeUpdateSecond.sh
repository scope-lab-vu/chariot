#! /bin/sh

case "$1" in
    start)
        echo "Adding nodes: 15 edison, 15 wifi_cam, 1 entry_terminal"
        echo "Starting NodeMembership on each node"
        fab -H s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=edison,monitoringServer=zk
        fab -H s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=wifi_cam,monitoringServer=zk
        fab -H s73 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=entry_terminal,monitoringServer=zk
        
        echo "Starting DeploymentManager on each node"
        fab -H s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73 -f FabFile.py start_deployment_manager:mongoServer=mongo
        
        echo "Starting ResourceMonitoring on each node"
        fab -H s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73 -f FabFile.py start_resource_monitor
        ;;
    stop)
        echo "Tearing down second update"
        fab -H s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73 -f FabFile.py stop_node_membership
        fab -H s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73 -f FabFile.py stop_deployment_manager
        fab -H s43,s44,s45,s46,s47,s48,s49,s50,s51,s52,s53,s54,s55,s56,s57,s58,s59,s60,s61,s62,s63,s64,s65,s66,s67,s68,s69,s70,s71,s72,s73 -f FabFile.py stop_resource_monitor
        ;;
    *)

    echo "Usage: NodeUpdateSecond.sh {start | stop}"
    exit 1
    ;;
esac

exit 0

