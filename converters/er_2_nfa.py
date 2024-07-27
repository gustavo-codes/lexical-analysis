from ..automata_and_re import NFA

"""
It receives as input a character that make part of a regular expression
and it says if it is really an input symboll or just a character that
makes part of the syntax of a regular expression, like "[", or "+"
"""
def isOperand(er_symboll):
	return
"""
The three next functions express the Thompson's algorithm
"""

"""
It receives a string that represents the regular expression,
a reference for a NFA object and a reference to integer "stateCounter".
The name of each state of the NFA is going to be a number and,
since the number of states are unknown, it is needed to save
the amount of states, so that we can name each state, that's why
"stateCounter" is useful.
"""
def prepareList(er, resultingNFA, stateCounter):
	lista_er = []
	for i in range(len(er)):
		if isOperand(er[i]) :
			resultingNFA.addInputStrAlphabet(er[i])
		else :
			lista_er.append(er[i])