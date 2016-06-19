import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// This example comprise nodes of two categories.
	// Here we describe node of EdgeNode category.
	nodeCategory EdgeNode;
	
	// Node template for edge nodes.
	nodeTemplate Edison {
		category EdgeNode;
		memory 1024 MB;		// 1 GB
		storage 4096 MB;	// 4 GB
		middleware LCM;
		os Linux;
		device ultrasonic_ranger;
	}
}
