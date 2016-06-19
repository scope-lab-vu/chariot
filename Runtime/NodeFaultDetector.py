__author__ = 'Garrett Hoffman'

# Watches the oplog of a MongoDB replica set. Once it reads an operation, if the operation is 'insert', the document
# that was inserted is written to an output file. The filename is in the format db.collection

from pymongo import MongoClient
from time import sleep
import pymongo
import json
import time
import os
from pymongo import CursorType

from pymongo.errors import AutoReconnect
heartbeats={}

# Time to wait for data or connection.
_SLEEP = 10
def findDeadNodes(client):
    db = client["ConfigSpace"]
    lsColl = db["LiveSystem"]

    for key in heartbeats.keys():
        if time.time() - heartbeats[key] >10:
            print str(key) +' is dead'

            # Set node state to FAULTY in database.
            result = lsColl.update({"name":str(key)},
                                   {"$set":{"status": "FAULTY"}},
                                   upsert = False)
        else:
            # If heartbeat fine, and status is not ACTIVE (i.e. FAULTY) then set to ACTIVE.
            # NOTE: Currently we do not want to add nodes that are not present in the model.
            #       So if a random new node pops up, we do not include that in our cluster.
            #       This else will only work for node that "went away" and "came back".

            result = lsColl.update({"name":str(key), "status":"FAULTY"},
                                   {"$set":{"status": "ACTIVE"}},
                                   upsert = False)

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    oplog = client.local.oplog.rs
    first = oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
    ts = first['ts']

    while True:
        # query = {'ts': {'$gt': some_timestamp}}  # Replace with your own query.
        cursor = oplog.find({'ts': {'$gt': ts}}, cursor_type=CursorType.TAILABLE_AWAIT)
        print 'created cursor'
        cursor.add_option(8)
        # cursor.add_option(_QUERY_OPTIONS['oplog_replay'])

        try:
            while cursor.alive:
                try:
                    for doc in cursor:
                        if doc['op'] == 'i':
                            print heartbeats
                            findDeadNodes(client)
                            print doc
                            filename = 'nodeMonitoringDocuments/'+doc['ns']
                            if not os.path.exists(os.path.dirname(filename)):
                                os.makedirs(os.path.dirname(filename))
                            with open(filename, "a") as f:
                                fullname = doc['ns'].split('.')
                                if len(fullname) < 2:
                                    print 'invalid db/collection name'
                                    continue
                                db = client[fullname[0]]
                                mcollection = db[fullname[1]]
                                if str(fullname[1]).strip() ==  'Heartbeat':
                                    heartbeats[fullname[0]]=time.time()
                                else:
                                    print(fullname[1])
                                tosave = mcollection.find_one({'_id': doc['o']['_id']})
                                print 'saving document as file: ' + doc['ns']
                                jsonstring = json.dumps(str(tosave))

                                f.write(jsonstring + '\n')

                            # print doc

                except (AutoReconnect, StopIteration):
                    print 'exception triggered'
                    sleep(_SLEEP)

        finally:
            cursor.close()