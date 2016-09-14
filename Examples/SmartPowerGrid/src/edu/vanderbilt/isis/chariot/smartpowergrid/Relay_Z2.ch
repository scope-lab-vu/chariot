import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	component Relay_Z2 {
 		provides relay_z2
 		
 		startScript "sh relay.sh"
 	}
}