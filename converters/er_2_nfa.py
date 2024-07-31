from ..automata_and_re import NFA
from collections import deque

class operator:
	def __init__(self, operator):
		if (operator == '|'):
			self.symbol = '|'
			self.priority = 3
		elif (operator == '.'):
			self.symbol = '.'
			self.priority = 2
		elif (operator == '*'):
			self.symbol == '*'
			self.priority = 1
		elif (operator == '('):
			self.symbol = '('
			self.priority = 0
		elif (operator == ')'):
			self.symbol = ')'
			self.priority = 0

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

def shuntingYard(er_expression):
	output_queue = []
	operator_queue = deque() #creates list with stack methods
	for i in range (len(er_expression)):
		#if the character is an operand
		if (isOperand(er_expression[i])):
			output_queue.append(er_expression)
		#if the character is other thing
		else:
			operatorObj = operator(er_expression[i])
			while ((operator_queue) and (operator_queue[-1].symbol != '(') and (operator_queue[-1].priority >= operatorObj.priority)):
				output_queue.append(operator_queue[-1].symbol)
				operator_queue.pop()
				operator_queue.append(operatorObj)
			if operatorObj.symbol == '(':
				operator_queue.append(operatorObj)
			elif operatorObj.symbol == ')':
				while (operator_queue) and (operator_queue[-1].symbol != '('):
					output_queue.append(operator_queue[-1].symbol)
					operator_queue.pop()
					if (operator_queue[-1].symbol == "("):
						#output_queue.append(operator_queue[-1].symbol) we don't do this
						operator_queue.pop() #discard the left parenthesis
		while operator_queue :
			if (operator_queue.symbol != '('):
				output_queue.append(operator_queue[-1].symbol)
			operator_queue.pop()
		return output_queue

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
	2:{'0':{1}, '1':{0}, '':{3}},
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
		afn.delta[afn.f][''] = afn2.q0 + len(afn.q) #Create an epsilon transition from AFN1 f to AFN2 q0
		
		#Do a shift in AFN2 states and add they to AFN delta
		shift = len(afn) 
		for i in afn2:
			for j in afn2[i]:
				newset = set()
				for k in afn2[i][j]:
					newset.add(k+shift)
				afn2[i][j] = newset
			afn[i+shift] = afn2[i]
			
	
