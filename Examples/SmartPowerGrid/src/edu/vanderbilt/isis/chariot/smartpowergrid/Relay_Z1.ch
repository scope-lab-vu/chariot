import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	component Relay_Z1 {
 		provides relay_z1
 		
 		requires 64 MB memory
 		
 		startScript "sh relay.sh"
 	}
}