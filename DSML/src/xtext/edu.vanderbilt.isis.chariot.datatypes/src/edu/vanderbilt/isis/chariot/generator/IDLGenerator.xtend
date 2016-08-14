package edu.vanderbilt.isis.chariot.generator

import org.eclipse.xtext.generator.IGenerator
import org.eclipse.emf.ecore.resource.Resource
import org.eclipse.xtext.generator.IFileSystemAccess
import edu.vanderbilt.isis.chariot.datatypes.Message
import com.google.inject.Inject
import org.eclipse.xtext.naming.IQualifiedNameProvider
import edu.vanderbilt.isis.chariot.datatypes.MessageElement
import edu.vanderbilt.isis.chariot.AllowableTypes
import java.util.HashSet

/*
 * Class for IDL generation from data type descriptions.
 */
class IDLGenerator implements IGenerator {
	@Inject extension IQualifiedNameProvider
	@Inject extension AllowableTypes allowableTypes

	/*
	 * Static class that represents sequence definition.
	 */
	static class SequenceDefinition {
		String typename
		long quantity
		String suffix

		/*
		 * Constructor.
		 * 
		 * @param name		Name of the sequence.
		 * @param maxbound	Maximum number of elements.
		 * @param type		Type of elements in the sequence.
		 */
		new(String name, long maxbound,String type) {
			quantity = maxbound
			suffix = name
		    typename = 	type
		}
	
		/*
		 * Method to get unique identifier.
		 * 
		 * @returns Unique identifier as a string.
		 */
		def String uniqueIdentifier() {
			return typename + '_' + suffix + quantity.toString
		}

		/*
		 * Method to get sequence name.
		 * 
		 * @returns Unique sequence name as a string.
		 */
		def String sequenceName() '''
		    «IF typename=="string"»
		    typedef string<«quantity»> «uniqueIdentifier»;
		    «ELSE»
		    typedef sequence<«typename»,«quantity»> «uniqueIdentifier»;
			«ENDIF»
		'''
	}

	/*
	 * Method that performs IDL generation.
	 * 
	 * @param input	Input resource on which generation must be performed.
	 * @param fsa	File system accessor.
	 */
	override doGenerate(Resource input, IFileSystemAccess fsa) {
		// throw new UnsupportedOperationException("TODO: auto-generated method stub")
		for (e : input.allContents.toIterable.filter(Message)) {

			var messageString = compileToString(e)	//e.compileToString

			fsa.generateFile(
				e.fullyQualifiedName.toString("/") + ".idl",
				beautify(messageString)	//messageString.beautify
			)
		}
	}

	/*
	 * Method to indent (beautify) generated IDL file.
	 * 
	 * @param code	IDL code to indent as a single string.
	 * 
	 * @returns Indented (beautified) version of the input IDL code.
	 */
	def String beautify(String code) {
		var indent = 0;
		var temp = new StringBuilder
		var contents = code.split("\n")
		var SEPARATOR = "    "
		for (line : contents) {

			if (line.contains("{")) {
				for (var i = 0; i < indent; i++) {
					temp.append(SEPARATOR)
				}
				temp.append(line.trim)
				temp.append("\n")
				indent++
			} else if (line.contains("}")) {
				indent--
				for (var i = 0; i < indent; i++) {
					temp.append(SEPARATOR)
				}
				temp.append(line.trim)
				temp.append("\n")
			} else {
				for (var i = 0; i < indent; i++) {
					temp.append(SEPARATOR)
				}
				temp.append(line.trim)
				temp.append("\n")
			}
		}
		return temp.toString
	}

	/*
	 * Method to compile a message (data type) into a string.
	 * 
	 * @param msg	Message (data type) that needs to be compiled to a string.
	 * 
	 * @return	The provided message (data type) converted to a single string.
	 */
	def String compileToString(Message msg) ''' 
			«var z= new HashSet<String>»
			«var x= msg.fullyQualifiedName»
			«var s = x.getSegmentCount»
			
			«FOR j : msg.features.filter(MessageElement)»
				«IF j.type.type.isMongoBean»
					«var result=z.add(j.type.qualifiedName)»
					«IF (result)»
					    «var n = j.type.qualifiedName.replace('.','/')»
						#include <«n».idl>
					«ENDIF»
				«ENDIF»
			«ENDFOR»
			«FOR i : 0..<s-1»
			module «x.getSegment(i)»
			{
			«ENDFOR»
			«FOR j : msg.features.filter(MessageElement)»
				«IF j.isIsArray»
					«var temp= new SequenceDefinition(msg.name,j.maxbound,j.idlType)»
					«temp.sequenceName»
				«ENDIF»
			«ENDFOR»
			struct «msg.name»
			{
			«FOR j : msg.features.filter(MessageElement)»
			«IF !j.isIsArray»
				«j.idlType»  «j.name»;«IF j.iskey»//@key«ENDIF»
			«ELSE»
				«var temp= new SequenceDefinition(msg.name,j.maxbound,j.idlType)»
				«temp.uniqueIdentifier»  «j.name» ;
			«ENDIF»
			«ENDFOR»
			};
			«FOR i : s-1..1»
			};
			«ENDFOR»
			
	'''
}