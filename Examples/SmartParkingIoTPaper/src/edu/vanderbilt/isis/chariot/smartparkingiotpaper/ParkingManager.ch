import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	externalComponent ParkingManager {
		// Provided functionality and declaration of
		// datatypes associated with different ports of the
		// functionality.
 		provides parking_manager{
 			parking_request_t as 
 				parking_manager.parking_request
 			parking_response_t as 
 				parking_manager.parking_response
 			occupancy_status_t as 
 				parking_manager.occupancy_status
 		}
 		
 		requires 1024 MB memory // Minimum memory required.
 		
 		startScript "sh ParkingManager.sh" // Launch script.
 	}
}

