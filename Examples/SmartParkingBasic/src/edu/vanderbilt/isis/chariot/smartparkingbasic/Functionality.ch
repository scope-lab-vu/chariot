package edu.vanderbilt.isis.chariot.smartparkingbasic {
	functionality parking_client {
		input parking_response;
		output parking_request;
	}
	
	functionality parking_manager {
		input parking_request, occupancy_status;
		output parking_response;
	}
	
	functionality occupancy_sensor {
		output occupancy_status;
	}
	
	composition request_handling {
		parking_client.parking_request to parking_manager.parking_request;
		parking_manager.parking_response to parking_client.parking_response;
	}
	
	composition occupancy_checking {
		occupancy_sensor.occupancy_status to parking_manager.occupancy_status;
	}
}