__author__ = "Subhav Pradhan"

from chariot_runtime_libs import Serialize
import pymongo
import csv

def main():
    client = pymongo.MongoClient("mongo", 27017)
    db = client["ConfigSpace"]
    reColl = db["ReconfigurationEvents"]
    findResult = reColl.find()
    solutionFoundDurations = list()
    solutionFoundDurations.append("Solution Finding")
    reconfigDurations = list()
    reconfigDurations.append("Reconfiguration")

    for re in findResult:
        reconfigEvent = Serialize(**re)
        detectionTime = reconfigEvent.detectionTime
        solutionFoundTime = reconfigEvent.solutionFoundTime
        reconfigTime = reconfigEvent.reconfiguredTime

        if solutionFoundTime != 0:
            solutionFindingDuration = solutionFoundTime - detectionTime
            solutionFoundDurations.append(solutionFindingDuration.total_seconds())
        else:
            solutionFoundDurations.append(0)
        
        if reconfigTime != 0:
            reconfigDuration = reconfigTime - solutionFoundTime
            reconfigDurations.append(reconfigDuration.total_seconds())
        else:
            reconfigDurations.append(0)
            

    print solutionFoundDurations
    print reconfigDurations

    with open("output.csv", "ab") as f:
        writer = csv.writer(f)
        writer.writerows([solutionFoundDurations, reconfigDurations])
        writer.writerow([])
        f.close()

if __name__ == '__main__':
    main()
