#! /bin/sh

case "$1" in
    start)
        echo "Adding nodes: 10 edison, 10 wifi_cam, 1 entry_terminal"
        echo "Starting NodeMembership on each node"
        fab -H s22,s23,s24,s25,s26,s27,s28,s29,s30,s31 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=edison,monitoringServer=zk
        fab -H s32,s33,s34,s35,s36,s37,s38,s39,s40,s41 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=wifi_cam,monitoringServer=zk
        fab -H s42 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=entry_terminal,monitoringServer=zk
        
        echo "Starting DeploymentManager on each node"
        fab -H s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42 -f FabFile.py start_deployment_manager:mongoServer=mongo
        
        echo "Starting ResourceMonitoring on each node"
        fab -H s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42 -f FabFile.py start_resource_monitor
        ;;
    stop)
        echo "Tearing down first update"
        fab -H s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42 -f FabFile.py stop_node_membership
        fab -H s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42 -f FabFile.py stop_deployment_manager
        fab -H s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,s42 -f FabFile.py stop_resource_monitor
        ;;
    *)

    echo "Usage: NodeUpdateFirst.sh {start | stop}"
    exit 1
    ;;
esac

exit 0

