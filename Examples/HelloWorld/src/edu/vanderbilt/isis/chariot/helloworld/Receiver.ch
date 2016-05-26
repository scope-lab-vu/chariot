import edu.vanderbilt.isis.chariot.helloworld.*
package edu.vanderbilt.isis.chariot.helloworld {
	// A receiver component that receives greeting messages, queries for time,
	// and prints related information.
	chariotComponent Receiver {
		// A push input port with buffer size of 10 to receive greeting messages.
		pushInPort receive_port greeting_message [10]
		
		// A pull input port for synchronous time query.
		pullInPort time_query_port time {
			timeout 2 seconds
		}
		
		provides receiver {
			receive_port as receiver.greeting
			time_query_port as receiver.time
		}
		
		// This trigger specifies that the Receiver component's business logic
		// gets triggered once a message is received in the receive_port.
		sporadicTrigger for port receive_port
		run {
			'
				greeting_message msg
				time curr_time
				take (receive_port, msg)
				receive (time_query_port, curr_time)	// This is a sync RMI.
				print ("Received greeting information: ")
				print ("Sender - ", msg.sender_id)
				print ("Message - ", msg.msg)
				print ("Time - ", curr_time)
			'
		}
	}	
}