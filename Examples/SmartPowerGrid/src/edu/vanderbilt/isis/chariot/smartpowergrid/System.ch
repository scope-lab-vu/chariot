import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	goalDescription SmartPowerGrid {
		// Objectives.
		node PMU pmu1
		node PMU pmu2
		node PMU pmu3
		
		protection_area1 as objective z1
		protection_area2 as objective z2
		protection_area3 as objective z3
		
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
