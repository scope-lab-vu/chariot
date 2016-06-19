package edu.vanderbilt.isis.chariot.smartparkingbasic {
	// Client functionality with input to receive parking
	// response and send parking request.
	functionality parking_client {
		input parking_response;
		output parking_request;
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
}