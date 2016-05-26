import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	system SmartParkingBasic {
		lifeTime 5 months
		reliabilityThreshold 0.2
		
		node beacon1{
			meanTimeToFailure 2 months
			template Edison
			iface if1 address "10.1.1.1" network smartparking
		}
		node beacon2{
			meanTimeToFailure 3 months
			template Edison
			iface if1 address "10.1.1.2" network smartparking
		}
		node beacon3{
			meanTimeToFailure 4 months
			template Edison
			iface if1 address "10.1.1.3" network smartparking
		}
		
		request_handling as objective RequestHandling;

		occupancy_checking as localObjective OccupancyChecking {
			appliesTo EdgeNode nodes
			keep occupancy_sensor perNode
		}
		
		replicate parking_manager asVoterCluster with [3,5] instances and ParkingManagerVoter
		
		//replicate parking_manager asConsensusCluster with [2, 3] instances and ParkingManagerConsensus
	}
}