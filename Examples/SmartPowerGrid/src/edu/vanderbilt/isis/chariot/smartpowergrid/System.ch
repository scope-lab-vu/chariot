import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	goalDescription SmartPowerGrid {
		// Objectives.
		sensing as objective Sensing
		actuating as objective Actuating
		
		// Replication constraints.
		replicate pmu asPerNode 
			for category PMU
		replicate breaker asPerNode 
			for category Breaker
		replicate relay asCluster 
			with [5,10] instances
	}
}