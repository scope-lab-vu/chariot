import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	component Relay_Z2 {
 		provides relay_z2
 		
 		requires 64 MB memory
 		
 		startScript "sh relay.sh"
 	}
}