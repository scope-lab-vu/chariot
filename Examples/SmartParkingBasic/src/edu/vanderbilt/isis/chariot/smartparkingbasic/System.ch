import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	system SmartParkingBasic {
		node beacon1{
			template Edison;
		}
		node beacon2{
			template Edison;
		}
		node beacon3{
			template Edison;
		}
		node beacon4{
			template Edison;
		}
		
		request_handling as objective RequestHandling;

		occupancy_checking as localObjective OccupancyChecking {
			appliesTo EdgeNode nodes;
			keep occupancy_sensor perNode;
		}
		
		replicate parking_manager asVoterCluster with [3,5] instances and ParkingManagerVoter;
	}
}