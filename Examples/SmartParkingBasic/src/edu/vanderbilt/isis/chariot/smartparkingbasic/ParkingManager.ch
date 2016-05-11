import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	external app ParkingManager{
 		provides parking_manager{
 			parking_request_t as parking_manager.parking_request;
 			parking_response_t as parking_manager.parking_response;
 			occupancy_status_t as parking_manager.occupancy_status;
 		}
 		
 		requires 256 MB memory
 		requires Linux;
 		requires LCM;
 		
 		startScript "sh ParkingManager.sh"
 	}
}