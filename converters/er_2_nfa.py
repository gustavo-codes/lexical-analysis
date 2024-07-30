from ..automata_and_re import NFA

"""
It receives as input a character that make part of a regular expression
and it says if it is really an input symboll or just a character that
makes part of the syntax of a regular expression, like "[", or "+"
"""
def isOperand(er_symboll):
	lower_case_alphabet=[chr(i) for i in range(ord('a'), ord('z')+1)]
	upper_case_alphabet=[chr(i) for i in range(ord('A'), ord('Z')+1)]
	numbers = [chr(i) for i in range(0,10)]
	other_operands = ['_','=','+','-','*',';']
	all_operands = []
	all_operands.extend(lower_case_alphabet)
	all_operands.extend(upper_case_alphabet)
	all_operands.extend(numbers)
	all_operands.extend(other_operands)
	if (er_symboll in all_operands):
		return True
	return False
	
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

"""
Recieves a stack and do one of the three Regular Expressions operations
a = {
	0:{'0':{1}, '1':{1}},
	1:{'0':{0}, '1':{2}},
	2:{'0':{1}, '1':{0}}
}
b = {
	0:{'0':{2}, '1':{1}},
	1:{'0':{1}, '1':{2}},
	2:{'0':{1}, '1':{0}}
}

a.b = {
	0:{'0':{1}, '1':{1}},
	1:{'0':{0}, '1':{2}},
	2:{'0':{1}, '1':{0}, '':{3}}
	3:{'0':{5}, '1':{4}},
	4:{'0':{4}, '1':{5}},
	5:{'0':{4}, '1':{3}}
}
"""
def erToNFA(stack):
	symbol = stack.pop()
	if(symbol == '.'):
		afn1 = stack.pop()
		afn2 = stack.pop()
		afn = afn1

	