import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	component Relay {
 		provides relay
 		
 		startScript "sh relay.sh"
 	}
}