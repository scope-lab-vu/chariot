import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	system SmartParkingBasic {
		reliabilityThreshold 0.42
		
		node beacon1{
			reliability 0.8
			template Edison;
			iface if1 address "10.1.1.1" network smartparking
		}
		node beacon2{
			reliability 0.9
			template Edison;
			iface if1 address "10.1.1.2" network smartparking
		}
		node beacon3{
			reliability 0.7
			template Edison;
			iface if1 address "10.1.1.3" network smartparking
		}
		
		request_handling as objective RequestHandling;

		occupancy_checking as localObjective OccupancyChecking {
			appliesTo EdgeNode nodes;
			keep occupancy_sensor perNode;
		}
		
		//replicate parking_manager asVoterCluster with [3,5] instances and ParkingManagerVoter;
	}
}