class NFA:
    def __init__(self, q, sigma, delta, q0, f):
        self.q = q  # Estados
        self.sigma = sigma  # Alfabeto
        self.delta = delta  # Transiçao
        self.q0 = q0  # Estado inicial 
        self.f = f  # Estado final/aceitaçao

    def epsilon_closure(self, states):
        """ Compute the epsilon closure for a set of states """
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if '' in self.delta.get(state, {}):  # Check for epsilon transitions
                for next_state in self.delta[state]['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def accepts(self, entrada):
        current_states = self.epsilon_closure({self.q0})
        for symbol in entrada:
            next_states = set()
            for state in current_states:
                if symbol in self.delta.get(state, {}):
                    next_states.update(self.delta[state][symbol])
            current_states = self.epsilon_closure(next_states)
        return current_states & self.f #Was bool(current_states & self.f) to print true or false


""" transitions = {
    0: {'0': {0}, '1': {0, 1}},
    1: {'0': {2}, '1': {0}},
    2: {'0': {1}, '1': {2}}
}

nfa = NFA({0, 1, 2}, {'0', '1'}, transitions, 0, {0})

print(nfa.accepts('1011101'))  

#2 a^n, n is even or divisble by 3
transitions = {
    'p' : {'' : {'q', 'r'}},
    'q' : {'a' : {'q1'}},
    'q1' : {'a' : {'q'}},
    'r' : {'a': {'r1'}}, 
    'r1' : {'a': {'r2'}},
    'r2' : {'a': {'r'}} 
}

a = NFA({'p', 'q', 'r', 'q1', 'r1', 'r2'}, {'a'}, transitions, 'p', {'q', 'r'})
print(a.accepts('a'*2))
print(a.accepts('aaa'))
print(a.accepts('aaaaa'))
"""

