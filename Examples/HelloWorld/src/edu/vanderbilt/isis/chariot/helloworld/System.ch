import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// A simple system comprising three nodes.
	goalDescription HelloWorld {
		greeting_exchange as objective Greeting
		time_query as objective TimeQuery
	}
}