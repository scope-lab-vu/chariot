import edu.vanderbilt.isis.chariot.simpledemo.*
package edu.vanderbilt.isis.chariot.simpledemo {
	external app Sender {
 		provides sender{
 			message_t as sender.message;
 		}
 		
 		startScript "python SimpleDemo/sender.py"
 	}
}