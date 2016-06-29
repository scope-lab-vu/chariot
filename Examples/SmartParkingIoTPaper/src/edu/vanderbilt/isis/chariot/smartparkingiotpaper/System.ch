import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	system SmartParkingIoTPaper {
		lifeTime 5 months			// Expected lifetime.
		reliabilityThreshold 0.2	// Required threshold.
		
		node camera1 {
			meanTimeToFailure 3 months
			template CameraNode.wifi_cam
			iface if1 address "127.0.0.1:9000" network smartparking
		}
		/*node camera2 {
			meanTimeToFailure 4 months
			template wifi_cam
			iface if1 address "10.1.1.2" network smartparking
		}
		node camera3 {
			meanTimeToFailure 2 months
			template wifi_cam
			iface if1 address "10.1.1.3" network smartparking
		}
		node camera4 {
			meanTimeToFailure 5 months
			template wifi_cam
			iface if1 address "10.1.1.4" network smartparking
		}*/
		
		node edison1 {
			meanTimeToFailure 2 months
			template EdisonNode.edison
			iface if1 address "127.0.0.1:9001" network smartparking
		}
		node edison2 {
			meanTimeToFailure 4 months
			template EdisonNode.edison
			iface if1 address "127.0.0.1:9002" network smartparking
		}
		/*node edison3 {
			meanTimeToFailure 5 months
			template edison
			iface if1 address "10.1.1.7" network smartparking
		}
		node edison4 {
			meanTimeToFailure 2 months
			template edison
			iface if1 address "10.1.1.8" network smartparking
		}*/
		
		client_interaction as objective ClientInteraction

		occupancy_checking as objective OccupancyChecking
		
		replicate image_capture asPerNode for category CameraNode
		replicate occupancy_detector asCluster with [2,4] instances
	}
}