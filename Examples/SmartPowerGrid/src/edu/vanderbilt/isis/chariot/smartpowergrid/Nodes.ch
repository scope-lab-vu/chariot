import edu.vanderbilt.isis.chariot.smartpowergrid.*
package edu.vanderbilt.isis.chariot.smartpowergrid {
	// Node categories for different PMUs.
	nodeCategory PMU_Z1 {
		nodeTemplate default_pmu_z1{}
	}
	
	nodeCategory PMU_Z2 {
		nodeTemplate default_pmu_z2{}
	}
	
	nodeCategory PMU_Z3 {
		nodeTemplate default_pmu_z3{}
	}
	
	// Node categories for different breakers.
	nodeCategory Breaker_Z1 {
		nodeTemplate default_breaker_z1{}
	}
	
	nodeCategory Breaker_Z2 {
		nodeTemplate default_breaker_z2{}
	}
	
	nodeCategory Breaker_Z3 {
		nodeTemplate default_breaker_z3{}
	}
	
	// Node categories for different IEDs.
	nodeCategory IED_Z1 {
		nodeTemplate default_ied_z1{}
	}
	
	nodeCategory IED_Z2 {
		nodeTemplate default_ied_z2{}
	}
	
	nodeCategory IED_Z3 {
		nodeTemplate default_ied_z3{}
	}
}