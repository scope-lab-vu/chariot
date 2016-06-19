package edu.vanderbilt.isis.chariot.simpledemo {
	functionality sender {
		output message;
	}
	
	functionality receiver {
		input message;
	}
	
	composition sender_receiver {
		sender.message to receiver.message;
	}
}