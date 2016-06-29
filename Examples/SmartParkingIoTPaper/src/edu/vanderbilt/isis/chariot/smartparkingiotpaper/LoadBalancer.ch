import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	hardware externalComponent LoadBalancer {
 		provides load_balancer {
 			detector_request_t as load_balancer.detector_request
 			detector_response_t as load_balancer.detector_response
 		}
 		
 		requires 128 MB memory
 		
 		startScript "sh LoadBalancer.sh"
 	}
}