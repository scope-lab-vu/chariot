import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	hardware component ImageCapture{
 		provides image_capture {
 			detector_response_t as image_capture.detector_response
 			detector_request_t as image_capture.detector_request
 			image_t as image_capture.image
 		}
 		
 		startScript "sh ImageCapture.sh"
 	}
}