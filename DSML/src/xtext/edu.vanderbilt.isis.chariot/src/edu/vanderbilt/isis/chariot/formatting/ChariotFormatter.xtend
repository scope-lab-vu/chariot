package edu.vanderbilt.isis.chariot.formatting

import org.eclipse.xtext.Keyword
import org.eclipse.xtext.formatting.impl.AbstractDeclarativeFormatter
import org.eclipse.xtext.formatting.impl.FormattingConfig
import com.google.inject.Inject
import edu.vanderbilt.isis.chariot.services.ChariotGrammarAccess

class ChariotFormatter extends AbstractDeclarativeFormatter {
	@Inject extension ChariotGrammarAccess

	/*
	 * Method that overrides configureFormatting from AbstractDeclarativeFormatter.
	 */
	@Override override protected void configureFormatting(FormattingConfig it) {
		setWrappedLineIndentation(1)

		setLinewrap(1).after(importRule)
		setLinewrap(2).after(functionalityRule)
		setLinewrap(1).around(functionalityOutputParamsRule)
		setLinewrap(1).around(functionalityInputParamsRule)
		setLinewrap(2).around(compositionRule)
		setLinewrap(1).around(functionalityConnectionRule)
		
		setLinewrap(1).around(systemObjectiveRule)

		setAutoLinewrap(150)
		
		findKeywordPairs("{", "}").forEach(p|formatCurlyBraces(p.first, p.second))
		findKeywordPairs("(", ")").forEach(p|formatParentheses(p.first, p.second))
		findKeywordPairs("<", ">").forEach(p|formatParentheses(p.first, p.second))
		findKeywords(",").forEach(kw|setNoSpace.before(kw))
		findKeywords(":").forEach(kw|setNoSpace.before(kw))
		findKeywords(";").forEach(kw|formatSemicolon(kw))
		findKeywords(".").forEach(kw|formatDot(kw))
		
		setLinewrap(0, 1, 2).before(SL_COMMENTRule)
		setLinewrap(0, 1, 2).before(ML_COMMENTRule)
		setLinewrap(0, 1, 1).after(ML_COMMENTRule)
	}

	/*
	 * Method to format semicolons by removing space before a semicolon and adding
	 * a new line after a semicolon.
	 */
	def formatSemicolon(FormattingConfig it, Keyword semicolon) {
		setNoSpace().before(semicolon);
		setLinewrap().after(semicolon);
	}

	/*
	 * Method to format dots by ensuring no spaces around a dot.
	 */
	def formatDot(FormattingConfig it, Keyword dot) {
		setNoSpace().around(dot);
	}

	/*
	 * Method to format curly braces by ensuring proper indentation of contents
	 * inside a pair of curly braces and new lines after each curly brace.
	 */
	def formatCurlyBraces(FormattingConfig it, Keyword kw1, Keyword kw2) {
		setIndentationIncrement.after(kw1)
		setIndentationDecrement.before(kw2)
		setLinewrap.after(kw1)
		setLinewrap(1).after(kw2)
	}

	/*
	 * Method to format parentheses by ensuring no spaces around them.
	 */
	def formatParentheses(FormattingConfig it, Keyword kw1, Keyword kw2) {
		setNoSpace().around(kw1)
		setNoSpace().around(kw2)
	}
}
