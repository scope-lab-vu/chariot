import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	hardware externalComponent OccupancyDetector {
 		provides occupancy_detector {
 			image_t as occupancy_detector.image
 			occupancy_status_t as occupancy_detector.occupancy_status
 		}
 		
 		requires 1024 MB memory
 		
 		startScript "sh OccupancyDetector.sh"
 	}
}