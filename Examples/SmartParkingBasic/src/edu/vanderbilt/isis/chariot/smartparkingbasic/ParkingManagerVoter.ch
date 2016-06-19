import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	// A voter service, which will be used for voter replication. 
	// The idea here is that each member of a voter group will
	// send their output(s) to this service, which in turn uses
	// implemented voter logic to determine "voted" outputs.
	voter service ParkingManagerVoter{
		
		// Location of script that can be used to launch the
 		// associated executable.
 		startScript "sh SmartParkingBasic/ParkingManagerVoter.sh"
 	}
}