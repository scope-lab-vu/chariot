import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	goalDescription SmartPowerGrid {
		// Objectives.
		protection_z1 as objective Protection_Zone1
		protection_z2 as objective Protection_Zone2
		protection_z3 as objective Protection_Zone3

		
		// Replication constraints.
		replicate pmu_z1 asPerNode for category PMU_Z1
		replicate pmu_z2 asPerNode for category PMU_Z2
		replicate pmu_z3 asPerNode for category PMU_Z3
		
		replicate breaker_z1 asPerNode for category Breaker_Z1
		replicate breaker_z2 asPerNode for category Breaker_Z2
		replicate breaker_z3 asPerNode for category Breaker_Z3
	}
}
