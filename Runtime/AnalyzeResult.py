__author__ = "Subhav Pradhan"

import pymongo
import csv

if __name__ == '__main__':
    client = pymongo.MongoClient("192.168.1.6", 27017)
    db = client["ConfigSpace"]
    failureColl = db["Failures"]

    from SolverBackend import Serialize
    for failureEntry in failureColl.find():
        failure = Serialize(**failureEntry)
        failedEntity = failure.failedEntity
        detectionTime = failure.detectionTime
        solutionFoundTime = failure.solutionFoundTime
        reconfigTime = failure.reconfiguredTime

        solutionFindingDuration = solutionFoundTime - detectionTime
        actualReconfigDuration = reconfigTime - solutionFoundTime
        totalReconfigDuration = reconfigTime - detectionTime

        print "Entity: ", failedEntity
        print "D Time: ", detectionTime, type(detectionTime)
        print "S Time: ", solutionFoundTime
        print "R Time: ", reconfigTime

        print "Solution Finding Time: ", solutionFindingDuration.total_seconds()
        print "Reconfiguration Time: ", actualReconfigDuration.total_seconds()
        print "Total Reconfiguration Time: ", totalReconfigDuration.total_seconds()


