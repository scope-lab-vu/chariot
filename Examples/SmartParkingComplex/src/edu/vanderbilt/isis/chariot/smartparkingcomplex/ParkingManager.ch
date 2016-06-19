import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// External application that describes a ParkingManager.
	external app ParkingManager{
		// Declaration of functionalities provided.
 		provides parking_manager{
 			parking_request_t as parking_manager.parking_request;
 			parking_response_t as parking_manager.parking_response;
 			occupancy_status_t as parking_manager.occupancy_status;
 		}
 		
 		// Requirements declaration.
 		requires 256 MB memory
 		requires Linux;
 		requires LCM;
 		
 		// Location of script that can be used to launch the
 		// associated executable.
 		startScript "sh SmartParkingComplex/ParkingManager.sh"
 	}
}