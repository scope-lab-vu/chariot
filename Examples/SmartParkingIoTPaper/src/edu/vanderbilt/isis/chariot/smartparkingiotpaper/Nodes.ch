import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	nodeCategory CameraNode {
		// Template for Wi-Fi enabled (wireless IP) 
		// camera nodes.
		nodeTemplate wifi_cam {
			memory 32 MB
			storage 1024 MB 	// 1 GB external
		}
	}
	
	nodeCategory ProcessingNode {
		// Template for Edison nodes.
		nodeTemplate edison {
			memory 1024 MB		// 1 GB
			storage 4096 MB		// 4 GB
		}
	}
	
	nodeCategory TerminalNode {	
		// Template for entry termial nodes.
		nodeTemplate entry_terminal {
			memory 1024 MB		// 1 GB
			storage 8192 MB		// 8 GB
		}
	}
}