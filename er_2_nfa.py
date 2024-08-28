from automata_and_re import NFA
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
def charToNFA(char):
	trans = {
		0:{char:{1}},
		1:{}
	}
	nfa = NFA.NFA({0,1},{char},trans,0,{1})
	return nfa


def isER(char):
	op = ['*','.','|','(',')']
	for i in op:
		if char == i:
			return False
	return True

def prepareList(list):
	newlist = []
	for i in list:
		if isER(i):
			newlist.append(charToNFA(i))
		else:
			newlist.append(i)
	return newlist

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

#Do a shift in targetAutomata states in transitions and add them to resultingAutomata
def shiftStates(shift, resultingAutomata, targetAutomata):
	for i in targetAutomata.delta:
		for j in targetAutomata.delta[i]:
			newset = set()
			for k in targetAutomata.delta[i][j]:
				newset.add(k+shift)
			targetAutomata.delta[i][j] = newset
		resultingAutomata.delta[i+shift] = targetAutomata.delta[i]
		resultingAutomata.q.add(i+shift)

#Connect all targetAutomata end states to targetState on resultingAutomata with epsilon 
def updateEndStates(shift,targetState,resultingAutomata,targetAutomata):
		for i in targetAutomata.f:
			newset = set()
			newset.add(targetState)
			if(targetAutomata.delta[i].get('')): #Check if already have an epsilon transition in this state, if have, make an union
				resultingAutomata.delta[i+shift][''] = newset | targetAutomata.delta[i]['']
			else:
				resultingAutomata.delta[i+shift][''] = newset


#Reduce the stack applying one operation
def erToNFAs(stack):
	symbol = stack.pop()
	if(symbol == '.'):
		afn2 = stack.pop()
		afn1 = stack.pop()
		afn = afn1
		afn.sigma |= afn2.sigma 
		
		shift = len(afn.delta) #This is the shift factor for all AFN2 states index
		#Create an epsilon transition from all AFN end states to AFN2 q0
		updateEndStates(0,afn2.q0 + shift,afn,afn)

		#Renaming States
		#Do a shift in all AFN2 states index and add they into AFN delta and add all AFN2 states to AFN.q
		shiftStates(shift,afn,afn2)
		
		afn.f = set()
		for i in afn2.f:
			afn.f.add(i+shift)  #Resulting AFN end states are AFN2 end states

		#Finally add the new AFN to the stack	
		stack.append(afn)
	elif(symbol == '|'):
		afn2 = stack.pop()
		afn1 = stack.pop()
		newfinal = len(afn1.q)+len(afn2.q)+1
		afn = NFA.NFA({0,newfinal},afn1.sigma|afn2.sigma,{},0,{newfinal})
		shift = len(afn1.q)
		afn.delta[0] = {'':{afn1.q0+1,afn2.q0+shift+1}} #Create two epsilon transitions from AFN q0 to AFN1 and AFN2 initial states 

		#Renaming States
		#First we update ANF1 states index by applying a +1 shift on it, becouse now we have a new q0 state
		shiftStates(1,afn,afn1)

		#Renaming States
		#Then update ANF2 states index shifting they +shift+1
		shiftStates(shift+1,afn,afn2)
			
		afn.delta[newfinal] = {} #Add newfinal state to transitions dictionary
		
		#Now crate epsilon transitions from AFN1 and AFN2 end states to AFN new end state
		#Notice tha ANF1 and AFN2 lists of end states are not updated, thats why whe shift on getting transitions
		updateEndStates(1,newfinal,afn,afn1)
		updateEndStates(shift+1,newfinal,afn,afn2)

		stack.append(afn)
	elif(symbol == '*'):
		afn1 = stack.pop()
		newfinal = len(afn1.delta)+1
		afn = NFA.NFA({0,newfinal},afn1.sigma,{},0,{newfinal})
		afn.delta[0] = {'':{afn1.q0+1,newfinal}} #Create two epsilon transitions from AFN q0 to AFN1 q0

		#Renaming States
		#+1 shift
		shiftStates(1,afn,afn1)

		afn.delta[newfinal] = {'':{afn1.q0+1}} #Add newfinal state to transitions dictionary

		#Create an epsilon transition from all AFN1 end states to AFN end state
		updateEndStates(1,newfinal,afn,afn1)
		stack.append(afn)

def erToNFA(er):
	stack = []
	listaER = prepareList(er)
	for i in listaER:
		if type(i) != type('|'):
			stack.append(i)
		else:
			stack.append(i)
			erToNFAs(stack)
			# stack.pop(-2) #Delete the remaining '('
	return stack