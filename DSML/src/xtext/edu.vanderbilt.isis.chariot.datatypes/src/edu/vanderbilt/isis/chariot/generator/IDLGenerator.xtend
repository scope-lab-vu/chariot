package edu.vanderbilt.isis.chariot.generator

import org.eclipse.xtext.generator.IGenerator
import org.eclipse.emf.ecore.resource.Resource
import org.eclipse.xtext.generator.IFileSystemAccess
import edu.vanderbilt.isis.chariot.datatypes.Message
import com.google.inject.Inject
import org.eclipse.xtext.naming.IQualifiedNameProvider
import edu.vanderbilt.isis.chariot.datatypes.MessageElement
import edu.vanderbilt.isis.chariot.AllowableTypes
import org.eclipse.jdt.internal.formatter.DefaultCodeFormatter
import org.eclipse.text.edits.TextEdit
import org.eclipse.jdt.core.formatter.CodeFormatter
import org.eclipse.jface.text.Document
import org.eclipse.text.edits.MalformedTreeException
import org.eclipse.jface.text.BadLocationException
import java.util.HashMap
import java.util.Set
import java.util.HashSet

class IDLGenerator implements IGenerator {
	@Inject extension IQualifiedNameProvider
	@Inject extension AllowableTypes allowableTypes

	static class SequenceDefinition {
		String typename
		long quantity
		String suffix

		new(Message y, long maxbound,String type) {
			
			quantity = maxbound
			suffix = y.name
			
		    typename = 	type
		}
	
		def String uniqueIdentifier() {
			typename + '_' + suffix + quantity.toString
		}

		def String sequenceName() '''
		    «IF typename=="string"»
		    typedef string<«quantity»> «uniqueIdentifier»;
		    «ELSE»
			typedef sequence<«typename»,«quantity»> «uniqueIdentifier»;
			«ENDIF»
		'''
	}

	static var typedefs = new HashMap<String, SequenceDefinition>

	override doGenerate(Resource input, IFileSystemAccess fsa) {
		// throw new UnsupportedOperationException("TODO: auto-generated method stub")
		for (e : input.allContents.toIterable.filter(Message)) {

			var messageString = e.compileToString

			fsa.generateFile(
				e.fullyQualifiedName.toString("/") + ".idl",
				messageString.beautify
			)
		}
	}

	def beautify(String code) {
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

//		var  cf = new DefaultCodeFormatter();
//		var te = cf.format(CodeFormatter.K_UNKNOWN, code, 0,code.length(),0,null);
//		
//		var dc = new Document(code);
//		try{
//			te.apply(dc)
//			return dc.get
//		}
//		catch (MalformedTreeException e) {
//			// TODO Auto-generated catch block
//			return code
//		} catch (BadLocationException e) {
//			// TODO Auto-generated catch block
//			return code
//		}
	}

	/*
	 * public static val mongoPrimitiveTypes = #{
	 * 	'double',
	 * 	'java.lang.Double',
	 * 	'java.lang.String',
	 * 	'boolean', 
	 * 	'char',
	 * 	'java.lang.Boolean',
	 * 	'long',
	 * 	'java.lang.Long'
	 * }«FOR n:0..<jsegmentsize-1» «j.type.fullyQualifiedName.getSegment(n)»/«ENDFOR»
	 * 					«var jsegmentsize=j.type.fullyQualifiedName.getSegmentCount()»
	 */
	def String compileToString(Message message) ''' 
			«var z= new HashSet<String>»
			«var x= message.fullyQualifiedName»
			«var s = x.getSegmentCount»
			
			«FOR j : message.features.filter(MessageElement)»
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
			«FOR j : message.features.filter(MessageElement)»
				«IF j.isIsArray»
					«var temp= new SequenceDefinition(message,j.maxbound,j.idlType)»
					«temp.sequenceName»
				«ENDIF»
			«ENDFOR»
			struct «message.name»
			{
			«FOR j : message.features.filter(MessageElement)»
			«IF !j.isIsArray»
				«j.idlType»  «j.name»;«IF j.iskey»//@key«ENDIF»
			«ELSE»
				«var temp= new SequenceDefinition(message,j.maxbound,j.idlType)»
				«temp.uniqueIdentifier»  «j.name» ;
			«ENDIF»
			«ENDFOR»
			};
			«FOR i : s-1..1»
			};
			«ENDFOR»
			
	'''

}
	
	