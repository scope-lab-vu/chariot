import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	// A consensus service, which will be used for consensus 
	// replication. The idea here is that each member of a 
	// consensus group (ring) will have associated consensus 
	// service that will take care of running a consensus 
	// algorithm (raft/paxos) to maintain consistency of
	// state variables between different members.
	consensus service ParkingManagerConsensus{
		
		// Location of script that can be used to launch the
 		// associated executable.
 		startScript "sh SmartParkingBasic/ParkingManagerConsensus.sh"
 	}
}