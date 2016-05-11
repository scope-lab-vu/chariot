package edu.vanderbilt.isis.chariot.ui

import org.eclipse.swt.SWT
import org.eclipse.swt.graphics.RGB
import org.eclipse.xtext.ui.editor.syntaxcoloring.DefaultHighlightingConfiguration
import org.eclipse.xtext.ui.editor.syntaxcoloring.IHighlightingConfigurationAcceptor
import org.eclipse.xtext.ui.editor.utils.TextStyle

class SemanticHighlightingConfiguration extends DefaultHighlightingConfiguration {
	package final static String CROSS_REF = "CrossReference"

	@Override override void configure(IHighlightingConfigurationAcceptor acceptor) {
		super.configure(acceptor)
		acceptor.acceptDefaultHighlighting(CROSS_REF, "Cross References", crossReferenceTextStyle())
	}

	@Override override TextStyle defaultTextStyle() {
		var TextStyle textStyle = new TextStyle()
		textStyle.setBackgroundColor(new RGB(255, 255, 255))
		textStyle.setColor(new RGB(0, 0, 0))
		return textStyle
	}

	def TextStyle crossReferenceTextStyle() {
		var TextStyle textStyle = defaultTextStyle().copy()
		textStyle.setStyle(SWT.ITALIC)
		return textStyle
	}

}
