import edu.vanderbilt.isis.chariot.simpledemo.*
package edu.vanderbilt.isis.chariot.simpledemo {
	nodeCategory EdgeNode;
	nodeTemplate BaseEdison {
		category EdgeNode; 
		memory 1024 MB;		// 1 GB
		storage 4096 MB;	// 4 GB
	}
	
	nodeTemplate LCDEdison {
		category EdgeNode;
		memory 1024 MB;		// 1 GB
		storage 4096 MB;	// 4 GB
		device lcd;
	}
}
