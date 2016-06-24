import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	externalComponent ParkingManager{
 		provides parking_manager{
 			parking_request_t as parking_manager.parking_request
 			parking_response_t as parking_manager.parking_response
 			occupancy_status_t as parking_manager.occupancy_status
 		}
 		
 		requires 1024 MB memory
 		
 		startScript "sh ParkingManager.sh"
 	}
}