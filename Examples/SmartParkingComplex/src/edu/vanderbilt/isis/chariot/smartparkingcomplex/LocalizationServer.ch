import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// External application that describes a LocalizationServer.
	external app LocalizationServer{
		// Declaration of functionalities provided.
 		provides localization_server{
 			location_t as localization_server.client_location;
 			location_t as localization_server.localized_location;
 		}
 		
 		// Requirements declaration.
 		requires 1024 MB memory
 		requires Linux;
 		requires LCM;
 		
 		// Location of script that can be used to launch the
 		// associated executable.
 		startScript "sh SmartParkingComplex/LocalizationServer.sh"
 	}
}