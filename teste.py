from automata_and_re import NFA
from automata_and_re import DFA
import nfa_2_dfa
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

#Make an union an save every er end state
def nfaUnion(list):
	endStates = {
		'INT':{},
		'CONST':{},
		'EQ' :{},
		'ADD' :{},
		'MULT':{} ,
		'SEMICOLON':{},
		'ID':{},
		'NUMBER':{},
		'STRING':{}}

	

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
		


def printAutomata(automata):
	print("Alfabeto")
	print(automata.sigma)
	print("Estados:")
	print(automata.q)
	print("Estado inicial:")
	print(automata.q0)
	print("Estados finais:")
	print(automata.f)
	# print("Transições:")
	# for i in automata.delta:
	# 	print(i)
	# 	print(automata.delta[i])

def stringToList(str):
	list = []
	for i in str:
		list.append(i)
	return list

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
	
a = {
	0:{'a':{1}},
	1:{}
}

b = {
	0:{'b':{1}},
	1:{}
}

c = {
	0:{'c':{1}},
	1:{}
}

d = {
	0:{'d':{1}},
	1:{}	
}

nfa1 = NFA.NFA({0,1},{'a'},a,0,{1})
nfa2 = NFA.NFA({0,1},{'b'},b,0,{1})
nfa3 = NFA.NFA({0,1},{'c'},c,0,{1})
nfa4 = NFA.NFA({0,1},{'d'},d,0,{1})

#ers = ['(','(',nfa1,nfa2,'.',')','(','(',nfa3,nfa4,'|',')','*',')','|',')']
#ers = ['(','(','(',nfa1,nfa2,'|',')',nfa3,'|',')',nfa4,'|',')']
#ers = ['(','(','(','(',nfa1,nfa2,'.',')',nfa3,'.',')',nfa4,'.',')','*',')']
#ers = ['(','(',nfa1,nfa2,'|',')','(	',nfa3,nfa4,'|',')','.',')']
#ers = ['(','(','(',nfa1,nfa2,'.',')','*',')','(',nfa3,nfa4,'.',')','|',')']
ers = ['(','(','a','b','|',')','*',')']


inter = 'in.t.'
conster = 'st.r.i.n.g.'
eqer = '='
adder = '+'
multer = '*'
suber = '-'
semicoloner = ';'
ider = '_ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z||AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z||_ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z||AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z||01|2|3|4|5|6|7|8|9||?.'
numer = '01|2|3|4|5|6|7|8|9|01|2|3|4|5|6|7|8|9|?.'
stringer = '\"ab|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|?AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|?.01|2|3|4|5|6|7|8|9|?.*?.-?.+?.=?.;?._?.?.\".'

listER = [inter, conster ,eqer , adder ,multer ,semicoloner,ider,numer,stringer]
final = inter + conster + '|' + eqer + '|' + adder + '|' + multer + '|' + semicoloner + '|' + ider + '|' + numer + '|' + stringer + '|'
intER = ['(','(','i','n','.',')','t','.',')']
stringER = ['(','(','(','(','(','s','t','.',')','r','.',')','i','.',')','n','.',')','g','.',')']
exemple = inter + conster + '|'

endStatesMap = {
	6:'INT',
	18: 'CONST',
	566: 'NUM',
	488: 'ID',
	844: 'STRING',
	26: 'SEMICOLON',
	22: 'SUM_OP',
	20: 'EQ_OP',
	24: 'MULT_OP',
	846: 'SUB_OP',
}

intNFA = erToNFA(inter)
constNFA = erToNFA(conster)
eqNFA = erToNFA(eqer)
addNFA = erToNFA(adder)
multNFA = erToNFA(multer)
semicolonNFA = erToNFA(semicoloner)
idNFA = erToNFA(ider)
numNFA = erToNFA(numer)
stringNFA = erToNFA(stringer)

listNFA = [erToNFA(inter),erToNFA(conster),erToNFA(eqer),erToNFA(adder),erToNFA(multer),erToNFA(semicoloner),erToNFA(ider),erToNFA(numer),erToNFA(stringer),erToNFA(suber)]

nfa = nfaUnion(listNFA)
printAutomata(nfa)

for i in nfa.accepts('"Ola"'):
	print(endStatesMap[i])


#482 ID 559 NUM
# printAutomata(erToNFA(inter))
# printAutomata(erToNFA(exemple))
# print(nfa.accepts('0'))
# print(stringNFA.accepts('')) #Bugando 




# intER = erToNFA(list(final))

# print(intER)
# print(printAutomata(intER[-1]))
# dfa = nfa_2_dfa.nfa_to_dfa(intER[-1])

# print(dfa.accepts('string'))
# printAutomata(dfa)



"""
shift = len(b)
for i in c:
    for j in c[i]:
        newset = set()
        for k in c[i][j]:
            newset.add(k+shift)
        c[i][j] = newset
    b[i+shift] = c[i]

for i in b:
    print(i)
    print(b[i])
"""