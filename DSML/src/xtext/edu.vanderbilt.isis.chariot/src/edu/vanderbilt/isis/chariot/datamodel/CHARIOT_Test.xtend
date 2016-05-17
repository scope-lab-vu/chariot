package edu.vanderbilt.isis.chariot.datamodel

import com.mongodb.Mongo
import org.junit.Test
import edu.vanderbilt.isis.chariot.datamodel.NodeCategory.DM_NodeCategory


class CHARIOT_Test {
	@Test def test () {
		val mongo = new Mongo()
		try {
			val db = mongo.getDB('testdb')
			
			val satellites = new DM_NodeCategory => [
				name = "Satellites"
				addNodeTemplate [
					name = "SatAlpha"
					//setStatus (Status.ACTIVE)
				]
			]
			satellites.addNodeTemplate [
				name = "SatBeta"
				//setStatus (Status.INACTIVE)
			]
			satellites.insert(db)
		}
		finally {
			mongo.close
		}
	}
}