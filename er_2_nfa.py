from automata_and_re import NFA
from collections import deque

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

#Create a simple NFA that accepts 'char'
def charToNFA(char):
	trans = {
		0:{char:{1}},
		1:{}
	}
	nfa = NFA.NFA({0,1},{char},trans,0,{1})
	return nfa

def isER(char):
	op = ['?','.','|','(',')']
	for i in op:
		if char == i:
			return False
	return True

def token(list):
	if len(list) == 0:
		return list[0]
	else:
		if list[0] == 'INT':
			return list[0]
		if list[0] == 'CONST':
			return list[0]
	

#Make an union an save every er end state
def nfaUnion(list):
	nfa = NFA.NFA({0},set(),{0:{'':set()}},0, set())
	count = 1

	for i in range(len(list)):
		shiftStates(count,nfa,list[i])
		for j in list[i].f:
			newSet = set()
			newSet.add(j+count)
			nfa.f |= newSet
		

		newSet = set()
		newSet.add(count)
		nfa.delta[0][''] |= newSet
		nfa.sigma |= list[i].sigma

		for j in list[i].f:
			count += j + 1
	
	return nfa

#Turn an er list into an automata and symblos list
def prepareList(list):
	newlist = []
	for i in list:
		if isER(i):
			newlist.append(charToNFA(i))
		else:
			newlist.append(i)
	return newlist

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
	elif(symbol == '?'):
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
	return stack[-1]

def assemble():
	inter = 'in.t.'
	stringer = 'st.r.i.n.g.'
	eqer = '='
	adder = '+'
	multer = '*'
	suber = '-'
	semicoloner = ';'
	ider = '_ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z||AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z||_ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z||AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z||01|2|3|4|5|6|7|8|9||?.'
	numer = '01|2|3|4|5|6|7|8|9|01|2|3|4|5|6|7|8|9|?.'
	conster = '\"ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|?AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|?.01|2|3|4|5|6|7|8|9|?. ?.<?.>?.*?.-?.+?.=?.;?._?.?.\".'
	greaterer = '>'
	lesser = '<'

	listNFA = [erToNFA(inter),erToNFA(stringer),erToNFA(eqer),erToNFA(adder),erToNFA(multer),erToNFA(semicoloner),erToNFA(ider),erToNFA(numer),erToNFA(conster),erToNFA(suber),erToNFA(greaterer),erToNFA(lesser)]

	nfa = nfaUnion(listNFA)

	return nfa