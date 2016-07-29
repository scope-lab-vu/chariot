#! /bin/sh

case "$1" in
    start)
        echo "Starting CHARIOT on node: $2 with template: $3"
        
        echo "Starting NodeMembership"
        fab -H $2 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=$3,monitoringServer=zk
        
        echo "Starting DeploymentManager"
        fab -H $2 -f FabFile.py start_deployment_manager:mongoServer=mongo
        
        echo "Starting ResourceMonitor"
        fab -H $2 -f FabFile.py start_resource_monitor
        ;;
    stop)
        echo "Tearing down CHARIOT on node: $2"
        fab -H $2 -f FabFile.py stop_node_membership
        fab -H $2 -f FabFile.py stop_deployment_manager
        fab -H $2 -f FabFile.py stop_resource_monitor
        ;;
    *)

    echo "Usage: NodeActivity.sh {start <node name> <node template> | stop <node name>}"
    exit 1
    ;;
esac

exit 0
