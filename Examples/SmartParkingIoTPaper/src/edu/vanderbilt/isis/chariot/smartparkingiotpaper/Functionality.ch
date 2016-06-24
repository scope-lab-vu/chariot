package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	// Client functionality with input and output port to interact with 
	// parking manager functionality.
	functionality parking_client {
		input parking_response
		output parking_request
	}
	
	// Parking manager functionality with an input and an output port to 
	// interact with client functionality. Also, another input port to 
	// interact with occupancy detector.
	functionality parking_manager {
		input parking_request, occupancy_status
		output parking_response
	}
	
	// Image capture functionality with an input and an output port to 
	// interact with load balancer functionality. Also, another output port 
	// to interact with occupancy detector.
	functionality image_capture {
		input detector_response
		output detector_request, image
	}
	
	// Load balancer functionality with an input and an output port to 
	// interact with image capture functionality.
	functionality load_balancer {
		input detector_request
		output detector_response
	}
	
	// Occupancy detector with an input port to interact with image capture 
	// functionality and an output port to interact with parking manager 
	// functionality.
	functionality occupancy_detector {
		input image
		output occupancy_status
	}
	
	// A composition that captures interaction between image capture, load 
	// balancer, occupancy detector, and parking manager functionalities.
	composition occupancy_checking {
		image_capture.detector_request to load_balancer.detector_request
		load_balancer.detector_response to image_capture.detector_response
		
		image_capture.image to occupancy_detector.image
		occupancy_detector.occupancy_status to parking_manager.occupancy_status
	}
	
	// A composition that captures interaction between parking client and
	// parking manager functionalities.
	composition client_interaction {
		parking_client.parking_request to parking_manager.parking_request
		parking_manager.parking_response to parking_client.parking_response
	}
}