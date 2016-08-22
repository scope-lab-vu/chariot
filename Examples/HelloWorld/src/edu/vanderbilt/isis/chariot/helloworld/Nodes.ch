import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// A simple node category and template.
	nodeCategory SimpleNodeCategory {
		nodeTemplate SimpleNodeTemplate {
			memory 1024 MB		// 1 GB
			storage 4096 MB		// 4 GB
			device camera
		}
	}
}
