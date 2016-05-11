package edu.vanderbilt.isis.chariot.ui

import java.util.Iterator
import org.eclipse.xtext.CrossReference
import org.eclipse.xtext.nodemodel.ILeafNode
import org.eclipse.xtext.nodemodel.INode
import org.eclipse.xtext.resource.XtextResource
import org.eclipse.xtext.ui.editor.syntaxcoloring.IHighlightedPositionAcceptor
import org.eclipse.xtext.ui.editor.syntaxcoloring.ISemanticHighlightingCalculator

class SemanticHighlightingCalculator implements ISemanticHighlightingCalculator {

	override void provideHighlightingFor(XtextResource resource, IHighlightedPositionAcceptor acceptor) {
		if(resource == null) return;

		var Iterator<INode> allNodes = resource.getParseResult().getRootNode().getAsTreeIterable().iterator()
		while (allNodes.hasNext()) {
			var INode node = allNodes.next()
			if (node.getGrammarElement() instanceof CrossReference) {
				acceptor.addPosition(node.getOffset(), node.getLength(), SemanticHighlightingConfiguration.CROSS_REF);
			}

		}
	}
}
	

	