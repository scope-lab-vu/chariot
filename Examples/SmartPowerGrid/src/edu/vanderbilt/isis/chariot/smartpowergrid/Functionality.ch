package edu.vanderbilt.isis.chariot.smartpowergrid {
	functionality pmu_z1 {
		output pmu_data_z1
	}
	
	functionality pmu_z2 {
		output pmu_data_z2
	}
	
	functionality pmu_z3 {
		output pmu_data_z3
	}
	
	functionality breaker_z1 {
		input breaker_action_z1
	}
	
	functionality breaker_z2 {
		input breaker_action_z2
	}
	
	functionality breaker_z3 {
		input breaker_action_z3
	}
	
	functionality relay_z1 {
		input pmu_data_z1
		output breaker_action_z1
	}
	
	functionality relay_z2 {
		input pmu_data_z2
		output breaker_action_z2
	}
	
	functionality relay_z3 {
		input pmu_data_z3
		output breaker_action_z3
	}
	
	composition protection_z1{
		pmu_z1.pmu_data_z1 to relay_z1.pmu_data_z1
		relay_z1.breaker_action_z1 to breaker_z1.breaker_action_z1
	}
	
	composition protection_z2{
		pmu_z2.pmu_data_z2 to relay_z2.pmu_data_z2
		relay_z2.breaker_action_z2 to breaker_z2.breaker_action_z2
	}
	
	composition protection_z3{
		pmu_z3.pmu_data_z3 to relay_z3.pmu_data_z3
		relay_z3.breaker_action_z3 to breaker_z3.breaker_action_z3
	}
}
