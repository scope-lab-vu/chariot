import edu.vanderbilt.isis.chariot.simpledemo.*
package edu.vanderbilt.isis.chariot.simpledemo {
	system SmartParkingBasic {
		/*node beacon2{
			template LCDEdison;
			iface wlan0 address "192.168.1.8" network simpledemo; 
		}*/
		node beacon3{
			template LCDEdison;
			iface wlan0 address "192.168.1.4" network simpledemo; 
		}
		node beacon6{
			template LCDEdison;
			iface wlan0 address "192.168.1.9" network simpledemo; 
		}
		node beacon7{
			template LCDEdison;
			iface wlan0 address "192.168.1.10" network simpledemo; 
		}
		node beacon9{
			template BaseEdison;
			iface wlan0 address "192.168.1.3" network simpledemo; 
		}
		node beacon10{
			template BaseEdison;
			iface wlan0 address "192.168.1.7" network simpledemo; 
		}
		
		sender_receiver as localObjective SenderReceiver {
			appliesTo EdgeNode nodes;
			keep sender perNode;
		}
	}
}