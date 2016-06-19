import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	// Defining a complex smart parking system that
	// performs localization and navigation.
	system SmartParkingComplex {
		// Different nodes that are part of the system.
		node edge1{
			template Edison;
			//iface smart_parking_ntw address "10.1.0.1";
		}
		node edge2{
			template Edison;
			//iface smart_parking_ntw address "10.1.0.2";
		}
		node edge3{
			template Edison;
			//iface smart_parking_ntw address "10.1.0.3";
		}
		node server1{
			template Server;
			//iface smart_parking_ntw address "10.1.0.4"; 
		}
		node server2{
			template Server;
			//iface smart_parking_ntw address "10.1.0.5";
		}
		node server3{
			template Server;
			//iface smart_parking_ntw address "10.1.0.6";
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
		
		// Localization objective.
		localization as objective Localization;
		
		// Navigation objective.
		navigation as objective Navigation;
	}
}