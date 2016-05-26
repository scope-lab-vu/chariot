package edu.vanderbilt.isis.chariot.helloworld {
	// Functionality that represents a greeting sender.
	functionality sender {
		output greeting
	}
	
	// Functionality that represents a greeting receiver.
	// This should also query current time.
	functionality receiver {
		input greeting, time
	}
	
	// Functionality that represents a time server, which
	// is responsible for sending time.
	functionality time_server {
		output time
	}
	
	// Composition that captures interaction between greeting
	// sender and receiver.
	composition greeting_exchange {
		sender.greeting to receiver.greeting
	}
	
	// Composition that captures interaction between client
	// that query/requests for time and server that responds
	// with the current time.
	composition time_query {
		receiver.time to time_server.time
	}
}