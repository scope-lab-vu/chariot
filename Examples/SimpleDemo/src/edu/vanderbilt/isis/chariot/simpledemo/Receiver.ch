import edu.vanderbilt.isis.chariot.simpledemo.*
package edu.vanderbilt.isis.chariot.simpledemo {
	external app Receiver {
 		provides receiver{
 			message_t as receiver.message;
 		}
 		
 		requires LCDEdison.lcd device;
 		
 		startScript "python SimpleDemo/receiver.py"
 	}
}