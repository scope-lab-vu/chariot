package edu.vanderbilt.isis.chariot.smartpowergrid {
	functionality pmu {
		output pmu_data
	}
	
	functionality breaker {
		input breaker_action
	}
	
	functionality relay {
		input pmu_data
		output breaker_action
	}
	
	composition sensing {
		pmu.pmu_data to relay.pmu_data
	}
	
	composition actuating {
		relay.breaker_action to breaker.breaker_action
	}
}