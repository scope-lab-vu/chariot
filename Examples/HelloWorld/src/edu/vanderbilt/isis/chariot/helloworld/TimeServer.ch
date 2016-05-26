import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// A time server component that handles synchronous time requests.
	chariotComponent TimeServer {
		// A pull output port to service time queries.
		pullOutPort server_port time
		
		provides time_server {
			server_port as time_server.time
		}
		
		// A sporadic trigger that instigates execution of this component's
		// business logic once message is received in server_port.
		sporadicTrigger for port server_port
		run {
			'
				time curr_time
				curr_time.time = get_current_time()	// Get and store current time in String format.
				send (server_port, curr_time)				
			'
		}
	}	
}