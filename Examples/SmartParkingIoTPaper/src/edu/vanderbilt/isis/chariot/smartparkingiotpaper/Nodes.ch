import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	// Declare categories.
	nodeCategory CameraNode {
		// Template for Wi-Fi enabled camera nodes.
		nodeTemplate wifi_cam {
		category CameraNode
		}
	}
	
	nodeCategory EdisonNode {
		// Template for Edison nodes.
		nodeTemplate edison {
			category EdisonNode
			memory 1024 MB		// 1 GB
			storage 4096 MB		// 4 GB
		}
	}
}