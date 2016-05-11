package edu.vanderbilt.isis.chariot.lib
import com.mongodb.DBCollection
import static extension edu.vanderbilt.isis.chariot.lib.WrappingUtil.*
/**
 * Example wrapper methods for DB interaction.
 */
class MongoExtensions {
	
	def <T extends IMongoBean> findOneBean(DBCollection collection, T wrapper) {
		collection.findOne(wrapper.getDbObject)?.wrap as T
	}
	
	def save(DBCollection collection, IMongoBean wrapper) {
		collection.save(wrapper.getDbObject)
	}
	
}