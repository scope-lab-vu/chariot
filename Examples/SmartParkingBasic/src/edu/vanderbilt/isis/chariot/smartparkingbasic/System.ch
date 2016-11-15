import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	goalDescription SmartParkingBasic {
		request_handling as objective RequestHandling
		
		occupancy_checking as objective OccupancyChecking
		
		replicate occupancy_sensor asPerNode for category EdgeNode		
		replicate parking_manager asVoterCluster with [3,5] instances and ParkingManagerVoter
	}
}