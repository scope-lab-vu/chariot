package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// Client functionality with input to receive parking
	// response and send parking request.
	functionality parking_client {
		input parking_response, heading;
		output parking_request;
	}
	
	// Decawave functionality to send a client's location.
	functionality decawave {
		output client_location;
	}
	
	// ParkingManager functionality with inputs to receive
	// parking request and occupancy status, and output
	// to send parking response.
	functionality parking_manager {
		input parking_request, occupancy_status;
		output parking_response;
	}
	
	// OccupancySensor functionality to send occupancy
	// status.
	functionality occupancy_sensor {
		output occupancy_status;
	}
	
	// LocalizationServer functionality to receive client
	// location, localize that information, and output
	// localized location.
	functionality localization_server {
		input client_location;
		output localized_location;
	}
	
	// NavigationServer functionality to receive parking
	// response to keep track of clients to navigate. This
	// functionality also takes as input localized location
	// information from LocalizationServer. Finally, as 
	// output, this functionality produces target heading 
	// that should be followed by a client.
	functionality navigation_server {
		input parking_response, localized_location;
		output heading;
	}
	
	// A composition to capture interaction between a client
	// and a ParkingManager.
	composition request_handling {
		parking_client.parking_request to parking_manager.parking_request;
		parking_manager.parking_response to parking_client.parking_response;
	}
	
	// A composition to capture interaction between an
	// OccupancySensor and a ParkingManager.
	composition occupancy_checking {
		occupancy_sensor.occupancy_status to parking_manager.occupancy_status;
	}
	
	// A composition to capture interaction between decawave
	// (client location source) and a LocalizationServer. This
	// also captures interaction between the LocalizationServer
	// and a NavigationServer.
	composition localization {
		decawave.client_location to localization_server.client_location;
		localization_server.localized_location to navigation_server.localized_location;
	}
	
	// A composition to capture interaction between a
	// NavigationServer and a client.
	composition navigation {
		parking_manager.parking_response to navigation_server.parking_response;
		navigation_server.heading to parking_client.heading;
	}
}