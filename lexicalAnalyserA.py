from er_2_nfa import assemble
from nfa_2_dfa import nfa_to_dfa

endStatesMap = {
	6:'INT',
	18: 'STRING',
	566: 'NUM',
	488: 'ID',
	856: 'CONST',
	26: 'SEMICOLON',
	22: 'SUM_OP',
	20: 'EQ_OP',
	24: 'MULT_OP',
	858: 'SUB_OP',
	860: 'GREATER_OP',
	862: 'LESS_OP'
}

def lexicalAnalisys():
    inputFile = open("input.txt","r")
    outputFile = open("output.txt","w")
    input = inputFile.readlines()
    lines = [line.rstrip('\n') for line in input]
    err = False
    inputFile.close()

    outputLines = list()
    for i in lines:
        entries = i.split(' ')
        output = list()
        for j in entries:
            tokens = list()
            if j != '':
                endState = dfa.accepts(j)
                for k in endState:
                    if(k in endStatesMap.keys()):
                        tokens.append(endStatesMap[k])

                if len(i) != 0:
                    if len(tokens) == 0 :
                        err = True
                    else:
                        output.append(tokens[0])
        outputLines.append(output)

    if(err):
        outputFile.write('ERRO')
    else:
        for i in outputLines:
            line = i
            line.append('\n')
            for j in range(len(line) -1):
                line[j] += ' '
            outputFile.writelines(line)


nfa = assemble()
dfa = nfa_to_dfa(nfa)
lexicalAnalisys()

