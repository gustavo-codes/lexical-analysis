class NFA:
    def __init__(self, q=None, sigma=None, delta=None, q0=None, f=None):
        self.q = q  # Estados
        self.sigma = sigma  # Alfabeto
        self.delta = delta  # Transiçao
        self.q0 = q0  # Estado inicial 
        self.f = f  # Estado final/aceitaçao

    def setQ0(self, q0):
        self.q0 = q0

    def setF(self, anotherFinalState):
        if (anotherFinalState not in self.f):
            self.f.append(anotherFinalState)

    def addDelta(self, outGoingState, inGoingState, inputStr):
        #if the transiction doesn't already exist, create it
        if( not self.delta[outGoingState]):
            self.delta[outGoingState] = None
        elif (self.delta[outGoingState]) and (not self.delta[outGoingState][inputStr]):
            self.delta[outGoingState][inputStr] = None
        if (inGoingState not in self.delta[outGoingState][inputStr]): #this is really an independent "if"
            self.delta[outGoingState][inputStr].append(inGoingState)        
    
    def addState(self, outGoingState, inGoingState, inputStr):
        #append the new states to the NFA
        if (outGoingState not in self.q):
            self.q.append(outGoingState)
        if (inGoingState not in self.q):
            self.q.append(inGoingState)

    def addInputStrAlphabet(inputStr):
        if inputStr not in self.sigma:
            self.sigma.append(inputStr)

    def accepts(self, entrada):
        current_states = {self.q0}
        for symbol in entrada:
            next_states = set()
            for state in current_states:
                if symbol in self.delta[state]:
                    next_states.update(self.delta[state][symbol])
            current_states = next_states
        return bool(current_states & self.f)


transitions = {
    0: {'0': {0}, '1': {0, 1}},
    1: {'0': {2}, '1': {0}},
    2: {'0': {1}, '1': {2}}
}

nfa = NFA({0, 1, 2}, {'0', '1'}, transitions, 0, {0})

print(nfa.accepts('1011101')) 