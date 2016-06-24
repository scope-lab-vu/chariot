import edu.vanderbilt.isis.chariot.smartparkingiotpaper.*
package edu.vanderbilt.isis.chariot.smartparkingiotpaper {
	system SmartParkingIoTPaper {
		lifeTime 5 months
		reliabilityThreshold 0.2
		
		node Camera1 {
			meanTimeToFailure 3 months
			template wifi_cam
			iface if1 address "10.1.1.1" network smartparking
		}
		node Camera2 {
			meanTimeToFailure 4 months
			template wifi_cam
			iface if1 address "10.1.1.2" network smartparking
		}
		node Camera3 {
			meanTimeToFailure 2 months
			template wifi_cam
			iface if1 address "10.1.1.3" network smartparking
		}
		node Camera4 {
			meanTimeToFailure 5 months
			template wifi_cam
			iface if1 address "10.1.1.4" network smartparking
		}
		
		node edison1 {
			meanTimeToFailure 2 months
			template edison
			iface if1 address "10.1.1.5" network smartparking
		}
		node edison2 {
			meanTimeToFailure 4 months
			template edison
			iface if1 address "10.1.1.6" network smartparking
		}
		node edison3 {
			meanTimeToFailure 5 months
			template edison
			iface if1 address "10.1.1.7" network smartparking
		}
		node edison4 {
			meanTimeToFailure 2 months
			template edison
			iface if1 address "10.1.1.8" network smartparking
		}
		
		client_interaction as objective ClientInteraction;

		occupancy_checking as objective OccupancyChecking {
			keep image_capture perNode for category CameraNode
		}
		
		replicate occupancy_detector asCluster with [2,4] instances
	}
}