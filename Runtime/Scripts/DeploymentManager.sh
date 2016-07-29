#! /bin/sh

case "$1" in
    start)
        echo "Starting Deployment Manager"
        echo "Ensuring we start with clean logs"
        rm -rf /home/ubuntu/tmpDeploymentManager
        mkdir -p /home/ubuntu/tmpDeploymentManager
        python -u /home/ubuntu/workspace/chariot/Runtime/DeploymentManager.py --mongoServer $2 --simulateDM >> /home/ubuntu/tmpDeploymentManager/DeploymentManager.log &
        ;;
    stop)
        echo "Stopping Deployment Manager"
        pkill -f "DeploymentManager"
        ;;
    *)

    echo "Usage: DeploymentManager.sh {start <mongoServer> | stop}"
    exit 1
    ;;
esac

exit 0
