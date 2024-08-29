class DFA:
    def __init__ (self, q, sigma, delta, q0, f):
        self.q = q #Estados
        self.sigma = sigma #Alfabeto
        self.delta = delta #Transiçoes
        self.q0 = q0 #Estado inicial
        self.f = f #Estado Final

    def accepts(self, entrada):
        state = self.q0
        for i in entrada:
            try:
                state = self.delta[state][i]
            except KeyError:
                state = ''
        return state #in self.f  


""" 
#Exemplos, carece de mais testes: 
transitions = {0:{'0':0, '1':1},
       1:{'0':2, '1':0},
       2:{'0':1, '1':2}}

b = DFA({0, 1, 2}, {'0', '1'}, transitions, 0, {0})

print(b.accepts('1011101'))

print(b.accepts('10111011')) """