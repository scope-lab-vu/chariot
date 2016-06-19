import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	// This example comprise nodes of single category.
	nodeCategory EdgeNode;
	
	// This example comprise nodes of single template.
	nodeTemplate Edison {
		category EdgeNode;
		memory 1024 MB;		// 1 GB
		storage 4096 MB;	// 4 GB
		middleware LCM;
		os Linux;
		device ultrasonic_ranger;
	}
}
