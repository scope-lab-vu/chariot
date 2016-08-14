package edu.vanderbilt.isis.chariot.generator

import org.eclipse.xtext.generator.IGenerator
import org.eclipse.emf.ecore.resource.Resource
import org.eclipse.xtext.generator.IFileSystemAccess
import com.google.inject.Inject
import org.eclipse.xtext.xbase.compiler.JvmModelGenerator

/**
 * Main class for data types generation.
 */
class DataTypesGenerator implements IGenerator {
	//@Inject JvmModelGenerator g1
	//@Inject IDLGenerator g2
	
	/**
	 * Method that performs the generation.
	 * 
	 * @param input	Input resource on which generation must be performed.
	 * @param fsa	File system accessor.
	 */
	override doGenerate(Resource input, IFileSystemAccess fsa) {
		//g1.doGenerate(input,fsa)
		//g2.doGenerate(input,fsa) 
	}
} 