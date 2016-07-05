import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	externalComponent Client{
 		provides parking_client{
 			parking_response_t as parking_client.parking_response
 			parking_request_t as parking_client.parking_request
 		}
 		
 		requires 256 MB memory
 		
 		startScript "sh Client.sh"
 	}
}


