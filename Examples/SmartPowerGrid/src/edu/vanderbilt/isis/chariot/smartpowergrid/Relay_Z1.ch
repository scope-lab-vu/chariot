import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	component Relay_Z1 {
 		provides relay_z1
 		
 		startScript "sh relay.sh"
 	}
}