__author__ = "Subhav Pradhan"

from SolverBackend import Serialize
import pymongo
import csv

def main():
    client = pymongo.MongoClient("localhost", 27017)
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

        solutionFindingDuration = solutionFoundTime - detectionTime
        reconfigDuration = reconfigTime - solutionFoundTime

        solutionFoundDurations.append(solutionFindingDuration.total_seconds())
        reconfigDurations.append(reconfigDuration.total_seconds())

    print solutionFoundDurations
    print reconfigDurations

    with open("output.csv", "ab") as f:
        writer = csv.writer(f)
        writer.writerows([solutionFoundDurations, reconfigDurations])
        writer.writerow([])
        f.close()

if __name__ == '__main__':
    main()


