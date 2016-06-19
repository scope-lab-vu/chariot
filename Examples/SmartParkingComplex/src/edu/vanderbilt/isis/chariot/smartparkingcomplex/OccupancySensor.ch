import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// External application that describes an OccupancySensor.
	// We consider OccupancySensor to be a periodic application
	// for this example.
	external app OccupancySensor {
		// Declaration of functionality provided.
 		provides occupancy_sensor{
 			occupancy_status_t as occupancy_sensor.occupancy_status;
 		}
 		
 		// Requirements declaration.
 		requires 64 MB memory;
 		requires Linux;
 		requires LCM;
 		requires Edison.ultrasonic_ranger device;
 		
 		// Parameters associated with periodicty.
 		period 5 seconds;
 		deadline 3 seconds;
 		
 		// Location of script that can be used to launch the
 		// associated executable.
 		startScript "sh SmartParkingComplex/OccupancySensor.sh"
 	}
}