import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// A simple system comprising three nodes.
	system HelloWorld {
		lifeTime 5 months
		reliabilityThreshold 0.2
		
		node node1{
			meanTimeToFailure 5 months
			template SimpleNode
		}
		
		node node2{
			meanTimeToFailure 3 months
			template SimpleNode
		}
		
		node node3{
			meanTimeToFailure 8 months
			template SimpleNode
		}
		
		greeting_exchange as objective Greeting;
		time_query as objective TimeQuery
	}
}