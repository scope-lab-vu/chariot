import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	component Relay_Z3 {
 		provides relay_z3
 		
 		startScript "sh relay.sh"
 	}
}