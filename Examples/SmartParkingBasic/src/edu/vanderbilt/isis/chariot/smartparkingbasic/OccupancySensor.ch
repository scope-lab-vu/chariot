import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	
	component OccupancySensor {
 		provides occupancy_sensor{
 			occupancy_status_t as occupancy_sensor.occupancy_status
 		}
 		
 		requires 64 MB memory
 		requires Linux
 		requires LCM
 		requires EdgeNode.Edison.ultrasonic_ranger device
 		
 		period 5 seconds
 		deadline 3 seconds
 		
 		startScript "sh OccupancySensor.sh"
 	}
}