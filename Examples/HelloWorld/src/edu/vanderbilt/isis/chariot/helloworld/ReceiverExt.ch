import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// An external receiver component.
	component Receiver {
		provides receiver
		
		requires SimpleNodeCategory.SimpleNodeTemplate.camera device
		requires 512 MB memory
		requires 1024 MB storage
	}	
}