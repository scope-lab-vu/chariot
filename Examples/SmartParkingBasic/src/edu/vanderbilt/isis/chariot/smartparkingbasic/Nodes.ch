import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	nodeCategory EdgeNode;
	nodeTemplate Edison {
		category EdgeNode; 
		memory 1024 MB;		// 1 GB
		storage 4096 MB;	// 4 GB
		middleware LCM;
		os Linux;
		device ultrasonic_ranger{
			meanTimeToFailure 3 months
		}
	}
}
