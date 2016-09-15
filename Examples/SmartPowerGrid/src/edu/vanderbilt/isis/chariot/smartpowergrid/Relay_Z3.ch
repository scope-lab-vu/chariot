import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	component Relay_Z3 {
 		provides relay_z3
 		
 		requires 64 MB memory
 		
 		startScript "sh relay.sh"
 	}
}