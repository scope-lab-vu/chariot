import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// A sender component that periodically sends greeting.
	chariotComponent Sender {
		// A push port to send greeting.
		pushOutPort send_port greeting_message
		
		provides sender {
			send_port as sender.greeting
		}
		
		// A state variable to store component id.
		stateVar 'long' as my_id
		
		// A periodic trigger and consequent business logic.
		periodicTrigger @5 seconds
		run {
			'
				greeting_message msg
				msg.sender_id = my_id
				msg.msg = "Hello"
				send (send_port, msg)				
			'
		}
	}	
}