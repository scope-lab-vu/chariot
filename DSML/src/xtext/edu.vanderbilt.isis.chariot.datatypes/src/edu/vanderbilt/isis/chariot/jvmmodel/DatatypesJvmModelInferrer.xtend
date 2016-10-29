package edu.vanderbilt.isis.chariot.jvmmodel

import com.google.inject.Inject
import org.eclipse.xtext.xbase.jvmmodel.AbstractModelInferrer
import org.eclipse.xtext.xbase.jvmmodel.IJvmDeclaredTypeAcceptor
import org.eclipse.xtext.xbase.jvmmodel.JvmTypesBuilder
import edu.vanderbilt.isis.chariot.AllowableTypes
import org.eclipse.xtext.naming.IQualifiedNameProvider
import org.eclipse.xtext.common.types.util.Primitives
import org.eclipse.xtext.xbase.jvmmodel.IJvmModelAssociations
import com.mongodb.BasicDBObject
import com.mongodb.DBObject
import java.util.List
import static extension org.eclipse.xtext.EcoreUtil2.*
import org.eclipse.xtext.common.types.JvmDeclaredType
import org.xtext.mongobeans.lib.MongoBeanList
import org.xtext.mongobeans.lib.WrappingUtil
import org.xtext.mongobeans.lib.IMongoBean
import edu.vanderbilt.isis.chariot.datatypes.DomainModel
import edu.vanderbilt.isis.chariot.datatypes.Message
import edu.vanderbilt.isis.chariot.datatypes.MessageElement
import edu.vanderbilt.isis.chariot.datatypes.MessageOperation
import edu.vanderbilt.isis.chariot.datatypes.Invariant
import com.mongodb.DBCollection
import org.eclipse.xtext.common.types.JvmTypeReference
import java.util.logging.Logger

/**
 * <p>Infers a JVM model from the source model.</p> 
 * 
 * <p>The JVM model should contain all elements that would appear in the Java code 
 * which is generated from the source model. Other models link against the JVM model rather than the source model.</p>     
 */
class DatatypesJvmModelInferrer extends AbstractModelInferrer {

	/**
	 * convenience API to build and initialize JVM types and their members.
	 */
	@Inject extension JvmTypesBuilder

	@Inject extension IQualifiedNameProvider

	@Inject extension AllowableTypes

	@Inject extension Primitives

	@Inject extension IJvmModelAssociations associations

    val logger= Logger.getLogger("DatatypesJvmModelInferrer")
	/**
	 * The dispatch method {@code infer} is called for each instance of the
	 * given element's type that is contained in a resource.
	 * 
	 * @param element
	 *            the model to create one or more
	 *            {@link org.eclipse.xtext.common.types.JvmDeclaredType declared
	 *            types} from.
	 * @param acceptor
	 *            each created
	 *            {@link org.eclipse.xtext.common.types.JvmDeclaredType type}
	 *            without a container should be passed to the acceptor in order
	 *            get attached to the current resource. The acceptor's
	 *            {@link IJvmDeclaredTypeAcceptor#accept(org.eclipse.xtext.common.types.JvmDeclaredType)
	 *            accept(..)} method takes the constructed empty type for the
	 *            pre-indexing phase. This one is further initialized in the
	 *            indexing phase using the closure you pass to the returned
	 *            {@link org.eclipse.xtext.xbase.jvmmodel.IJvmDeclaredTypeAcceptor.IPostIndexingInitializing#initializeLater(org.eclipse.xtext.xbase.lib.Procedures.Procedure1)
	 *            initializeLater(..)}.
	 * @param isPreIndexingPhase
	 *            whether the method is called in a pre-indexing phase, i.e.
	 *            when the global index is not yet fully updated. You must not
	 *            rely on linking using the index if isPreIndexingPhase is
	 *            <code>true</code>.
	 */
	def dispatch void infer(DomainModel file, IJvmDeclaredTypeAcceptor acceptor, boolean isPreIndexingPhase) {
		for (msg : file.eAllOfType(Message)) {
			acceptor.accept(msg.toClass(msg.fullyQualifiedName)) [
				documentation = msg.documentation
				superTypes += typeRef(IMongoBean)
				addConstructors(msg)
				addDbObjectProperty(msg)
				members += msg.toField('log', typeRef(Logger)) [
					static = true
					final = true
					initializer = '''«Logger.typeName».getLogger(«msg.name».class)'''
				]
				for (feature : msg.features) {
					switch feature {
						MessageElement: {
							if (feature.isArray) 
								addListAccessor(feature)
							else
								addDelegateAccessors(feature)
						}
						MessageOperation:
							addMethod(feature)
					}
				}
				for (invariant:msg.invariants){
					addInvariant(invariant)
				}
			] 
		}
	}

	/**
	 * Method to add constructor of a message (data type).
	 * 
	 * @param inferredType	Type of the message (data type).
	 * @param msg			Message for which a constructor should be added.
	 */
	def protected addConstructors(JvmDeclaredType inferredType, Message msg) {
		val typeRef1 = typeRef(DBObject)
		inferredType.members += msg.toConstructor [
			documentation = '''Creates a new «msg.name» wrapping the given {@link «DBObject.name»}.'''
			parameters += msg.toParameter("dbObject", typeRef1)

			body = '''
				this._dbObject = dbObject;
			'''
		]
		inferredType.members += msg.toConstructor [
			documentation = '''Creates a new «msg.name» wrapping a new {@link «BasicDBObject.name»}.'''
			body = '''
				_dbObject = new «BasicDBObject»();
				_dbObject.put(JAVA_CLASS_KEY, "«inferredType.identifier»");
				«FOR feature : msg.features»
				«IF feature instanceof MessageElement»
				«feature.getInitializer»
				«ENDIF»
				«ENDFOR»
				
			'''
		]
	}
	
	/**
	 * Method to get initializer method of the given message (date type) element.
	 * 
	 * @param element	Message (data type) element for which a initializer must
	 * 					be retrieved.
	 * 
	 * @returns	Initializer method declaration for the given message (data type)
	 * 			element.
	 */
	def String getInitializer(MessageElement element) {
		if (element.isIsArray)
			return ""

		if (element.type.type.isMongoBean) {
			return '''
				set«element.name.toFirstUpper»(new «element.jvmType.simpleName» ());
			'''
		}
		if (!element.type.isPrimitive) {
			return '''
				set«element.name.toFirstUpper»(new «element.jvmType.simpleName» ());
			'''

		} else {
			'''
				set«element.name.toFirstUpper»(«element.type.getInitalValue»);
			'''
		}

	}

	/**
	 * 
	 */
	def protected addDbObjectProperty(JvmDeclaredType inferredType, Message msg) {
		inferredType.members += msg.toField('_dbObject', typeRef(DBObject))
		inferredType.members += msg.toGetter('dbObject', '_dbObject', typeRef(DBObject))
	}

	/**
	 * 
	 */
	def protected addListAccessor(JvmDeclaredType inferredType, MessageElement property) {
		val propertyType = property.jvmType.asWrapperTypeIfPrimitive
		if (propertyType.isMongoPrimitiveType) {
			inferredType.members += property.toMethod(
				'get' + property.name.toFirstUpper,
				typeRef(List, propertyType)
			) [
				documentation = property.documentation
				body = '''
					log.info("inside get«property.name.toFirstUpper»");
					return («List»<«propertyType»>) _dbObject.get("«property.name»");
				'''
			]
		} else {

			inferredType.members += property.toField('_' + property.name, typeRef(MongoBeanList, propertyType))

			inferredType.members += property.toMethod(
				'get' + property.name.toFirstUpper,
				typeRef(List, propertyType)
			) [
				documentation = property.documentation
				body = '''
					if(_«property.name»==null)
						_«property.name» = new «MongoBeanList»<«propertyType»>(_dbObject, "«property.name»");
					return _«property.name»;
				'''
			]
		}
	}

	/**
	 * 
	 */
	def protected addDelegateAccessors(JvmDeclaredType inferredType, MessageElement property) {
		inferredType.members += property.toMethod('get' + property.name.toFirstUpper, property.jvmType) [
			documentation = property.documentation
			body = '''
				«IF property.jvmType.type.isMongoBean»
					return «WrappingUtil».wrapAndCast((«DBObject») _dbObject.get("«property.name»"));
				«ELSE»
					return («property.jvmType.asWrapperTypeIfPrimitive») _dbObject.get("«property.name»");
				«ENDIF»
			'''
		]
		inferredType.members += property.toMethod('set' + property.name.toFirstUpper, typeRef(Void.TYPE)) [
			documentation = property.documentation
			parameters += property.toParameter(property.name, property.jvmType)
			body = '''
				«IF property.jvmType.type.isMongoBean»
					_dbObject.put("«property.name»", «WrappingUtil».unwrap(«property.name»));
				«ELSE»
					_dbObject.put("«property.name»", «property.name»);
				«ENDIF»
			'''
		]
	}
	
	/**
	 * 
	 */
	def String getInitalValue(JvmTypeReference primitiveType){
		var String name = primitiveType.getIdentifier();
		logger.info(name+' and '+Long.TYPE.getName() );
		if (Boolean.TYPE.getName().equals(name)) {
			return "false";
		}
		if (Integer.TYPE.getName().equals(name)) {
			return "0";
		}
		if (Byte.TYPE.getName().equals(name)) {
			return '0';
		}
		if (Short.TYPE.getName().equals(name)) {
			return '0';
		}
		if (Character.TYPE.getName().equals(name)) {
			return '\'a\'';
		}
		
		if (Long.TYPE.getName().equals(name)) {
			return "0";
		}
		if (Float.TYPE.getName().equals(name)) {
			return '0.0';
		}
		if (Double.TYPE.getName().equals(name)) {
		   return '0.0';
		}
	}

	/**
	 * 
	 */
	def protected addMethod(JvmDeclaredType inferredType, MessageOperation operation) {
		inferredType.members += operation.toMethod(operation.name, operation.returnType) [
			documentation = operation.documentation
			parameters += operation.parameters.map[operation.toParameter(name, parameterType)]
			body = operation.body
		]
	}

	/**
	 * 
	 */
	def protected addInvariant(JvmDeclaredType inferredType, Invariant operation) {
		inferredType.members += operation.toMethod(operation.name, typeRef(Boolean.TYPE)) [
			documentation = operation.documentation
			body =operation.invariantExpression
		]
	}
	
	/**
	 * 
	 */
	def protected addCheckpoint(JvmDeclaredType inferredType, Message bean) {
		val typeRef1 = typeRef(DBCollection)
		inferredType.members += bean.toMethod ("checkpoint",typeRef(Void.TYPE)) [
			documentation = '''checkpoint the «bean.name» wrapping the given {@link «DBObject.name»}.'''
			parameters += bean.toParameter("dbCollection", typeRef1)

			body = '''
				dbCollection.save(this._dbObject);
			'''
		]
	}

	/**
	 * 
	 */
	def protected getJvmType(MessageElement property) {
		property.type
	}
}



