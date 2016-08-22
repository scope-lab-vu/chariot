import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// An external sender component.
	component Sender {
		provides sender
		
		requires 512 MB memory
	}
}