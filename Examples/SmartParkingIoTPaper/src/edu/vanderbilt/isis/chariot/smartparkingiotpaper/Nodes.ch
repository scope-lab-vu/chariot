import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	nodeCategory CameraNode
	nodeCategory EdisonNode
	
	nodeTemplate wifi_cam {
		category CameraNode
	}
	
	nodeTemplate edison {
		category EdisonNode
		memory 1024 MB		// 1 GB
		storage 4096 MB		// 4 GB
	}
}