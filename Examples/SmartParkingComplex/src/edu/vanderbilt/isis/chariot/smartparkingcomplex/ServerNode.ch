import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// This example comprise nodes of two categories.
	// Here we describe node of ServerNode category.
	nodeCategory ServerNode;
	
	// Node template for server nodes.
	nodeTemplate Server {
		category ServerNode;
    	memory 2048 MB;		// 2 GB
    	storage 10240 MB;	// 10 GB
    	middleware LCM;
    	os Linux;
	}
}
