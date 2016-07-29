#! /bin/sh

case "$1" in
    start)
        echo "Starting mongo server"
        echo "Ensuring we start from a clean database"
        rm -rf /home/ubuntu/tmpMongo/db
        mkdir -p /home/ubuntu/tmpMongo/db
        mongod --pidfilepath /home/ubuntu/tmpMongo/current.pid --fork --logpath /home/ubuntu/tmpMongo/log --dbpath /home/ubuntu/tmpMongo/db/ 
        ;;
    stop)
        echo "Stopping mongo server"
        pkill -f "mongod"
        ;;
    *)

    echo "Usage: MongoServer {start | stop}"
    exit 1
    ;;
esac

exit 0
