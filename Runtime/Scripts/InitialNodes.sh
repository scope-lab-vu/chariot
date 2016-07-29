#! /bin/sh

case "$1" in
    start)
        echo "Starting CHARIOT on: 10 edison, 10 wifi_cam, 1 entry_terminal"
        echo "Starting NodeMembership on each node"
        fab -H s1,s2,s3,s4,s5,s6,s7,s8,s9,s10 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=edison,monitoringServer=zk
        fab -H s11,s12,s13,s14,s15,s16,s17,s18,s19,s20 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=wifi_cam,monitoringServer=zk
        fab -H s21 -f FabFile.py start_node_membership:interface=eth0,network=iot,nodeTemplate=entry_terminal,monitoringServer=zk
        
        echo "Starting DeploymentManager on each node"
        fab -H s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21 -f FabFile.py start_deployment_manager:mongoServer=mongo

        echo "Starting ResourceMonitoring on each node"
        fab -H s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21 -f FabFile.py start_resource_monitor
        ;;
    stop)
        echo "Tearing down CHARIOT"
        fab -H s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21 -f FabFile.py stop_node_membership
        fab -H s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21 -f FabFile.py stop_deployment_manager
        fab -H s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21 -f FabFile.py stop_resource_monitor
        ;;
    *)

    echo "Usage: InitialNodes.sh {start | stop}"
    exit 1
    ;;
esac

exit 0
