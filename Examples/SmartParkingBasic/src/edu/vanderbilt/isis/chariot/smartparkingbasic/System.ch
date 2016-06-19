import edu.vanderbilt.isis.chariot.smartparkingbasic.*
package edu.vanderbilt.isis.chariot.smartparkingbasic {
	// Defining a simple smart parking system.
	system SmartParkingBasic {
		// Different nodes that are part of the system.
		node edge1{
			template Edison;
			//iface edison_netw address "10.1.0.1";
		}
		node edge2{
			template Edison;
			//iface edison_netw address "10.1.0.2";
		}
		node edge3{
			template Edison;
			//iface edison_netw address "10.1.0.3";
		}
		
		// RequestHandling objective.
		request_handling as objective RequestHandling;

		// OccupancyChecking objective. This is a local objective
		// that applies to all nodes of template EdgeNode. Occupancy
		// sensor functionality of this local objective should be
		// available per node.
		occupancy_checking as localObjective OccupancyChecking {
			appliesTo EdgeNode nodes;
			keep occupancy_sensor perNode;
		}
		
		// Replicating parking manager functionality of RequestHandling
		// objective as a consensus cluster using ParkingManagerConsensus
		// as consensus service. At most three instances of this functionality
		// should be present at any given time in the system, and at least
		// two instances should be present at all time.
		replicate parking_manager asConsensusCluster with [2,3] instances and ParkingManagerConsensus;
	}
}