package edu.vanderbilt.isis.chariot

import com.google.inject.Inject
import org.eclipse.xtext.common.types.JvmType
import org.eclipse.xtext.common.types.JvmTypeReference
import org.eclipse.xtext.common.types.util.RawSuperTypes
import edu.vanderbilt.isis.chariot.datatypes.Message
import edu.vanderbilt.isis.chariot.datatypes.MessageElement

class AllowableTypes {
	@Inject extension RawSuperTypes
	public static val mongoPrimitiveTypes = #{
		'double',
		'java.lang.Double',
		'java.lang.String',
		'boolean',
		'char',
		'java.lang.Boolean',
		'long',
		'java.lang.Long'
	}

	def isMongoPrimitiveType(JvmTypeReference typeRef) { 
		mongoPrimitiveTypes.contains(typeRef.qualifiedName)
	}

	def isMongoType(JvmTypeReference typeRef) {
		typeRef.isMongoPrimitiveType || typeRef.type.isMongoBean
	}

	def isMongoBean(JvmType type) {
		return type.collectNames.contains('edu.vanderbilt.isis.chariot.lib.IMongoBean')
	}

	def getLCMType(MessageElement message) {
		if (message.type.isMongoPrimitiveType) {
			val x = message.type.qualifiedName
			if (x == "double" || x == double)
				return "double"
			if (x == "java.lang.String")
				return "string"
			if (x == "boolean" || x == "char")
				return x
			if (x == "java.lang.Boolean")
				return "boolean"
			if (x == "java.lang.Long" || x == "long")
				return "int64_t" 
		} else if (message.type.type.isMongoBean) {
			var tname= message.type.qualifiedName
			return tname+'_lcm' 
		} 
	}

	def getIdlType(MessageElement message) {
		if (message.type.isMongoPrimitiveType) {
			val x = message.type.qualifiedName
			if (x == "double" || x == double)
				return "double"
			if (x == "java.lang.String")
				return "string"
			if (x == "boolean" || x == "char" || x == "long")
				return x
			if (x == "java.lang.Boolean")
				return "boolean"
			if (x == "java.lang.Long")
				return "long"
		} else if (message.type.type.isMongoBean) {
			return message.type.simpleName
		}

	}
}