import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	system SmartParkingIoTPaper {
		client_interaction as objective ClientInteraction

		occupancy_checking as objective OccupancyChecking
		
		replicate image_capture asPerNode for category CameraNode
		replicate parking_client asPerNode for category TerminalNode
		replicate occupancy_detector asCluster with [1,4] instances
	}
}