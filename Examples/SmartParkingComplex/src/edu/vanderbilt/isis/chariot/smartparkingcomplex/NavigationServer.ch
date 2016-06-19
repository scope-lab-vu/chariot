import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// External application that describes a NavigationServer.
	external app NavigationServer{
		// Declaration of functionalities provided.
 		provides navigation_server{
 			parking_response_t as navigation_server.parking_response;
 			location_t as navigation_server.localized_location;
 			heading_t as navigation_server.heading;
 		}
 		
 		// Requirements declaration.
 		requires 512 MB memory
 		requires Linux;
 		requires LCM;
 		
 		// Location of script that can be used to launch the
 		// associated executable.
 		startScript "sh SmartParkingComplex/NavigationServer.sh"
 	}
}