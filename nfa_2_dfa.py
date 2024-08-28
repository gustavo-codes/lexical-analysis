from automata_and_re import NFA
from automata_and_re import DFA


def nfa_to_dfa(nfa: NFA) -> DFA:
    from collections import defaultdict, deque

    # Helper function to find epsilon closure
    def epsilon_closure(states):
        return nfa.epsilon_closure(states)

    # Initial state of DFA is the epsilon closure of NFA's initial state
    initial_dfa_state = frozenset(epsilon_closure({nfa.q0}))

    # Queue for breadth-first search
    queue = deque([initial_dfa_state])
    # Mapping of DFA states to their transitions
    dfa_delta = {}
    # Set of all DFA states
    dfa_states = {initial_dfa_state}
    # Set of DFA accepting states
    dfa_accepting_states = set()

    while queue:
        current_dfa_state = queue.popleft()
        dfa_delta[current_dfa_state] = {}

        for symbol in nfa.sigma:
            next_states = set()
            for nfa_state in current_dfa_state:
                if symbol in nfa.delta.get(nfa_state, {}):
                    next_states.update(nfa.delta[nfa_state][symbol])
            next_dfa_state = frozenset(epsilon_closure(next_states))

            if next_dfa_state not in dfa_states:
                dfa_states.add(next_dfa_state)
                queue.append(next_dfa_state)

            dfa_delta[current_dfa_state][symbol] = next_dfa_state

            if next_dfa_state & nfa.f:
                dfa_accepting_states.add(next_dfa_state)

    # Map DFA states to integers for easier representation
    state_mapping = {state: idx for idx, state in enumerate(dfa_states)}

    dfa_q = set(state_mapping.values())
    dfa_sigma = nfa.sigma
    dfa_q0 = state_mapping[initial_dfa_state]
    dfa_f = {state_mapping[state] for state in dfa_accepting_states}
    dfa_delta_mapped = {
        state_mapping[state]: {symbol: state_mapping[next_state]
                               for symbol, next_state in transitions.items()}
        for state, transitions in dfa_delta.items()
    }

    return DFA.DFA(dfa_q, dfa_sigma, dfa_delta_mapped, dfa_q0, dfa_f)

""" 
transitions_nfa = {
    'p': {'': {'q', 'r'}},
    'q': {'a': {'q1'}},
    'q1': {'a': {'q'}},
    'r': {'a': {'r1'}},
    'r1': {'a': {'r2'}},
    'r2': {'a': {'r'}}
}

nfa = NFA({'p', 'q', 'r', 'q1', 'r1', 'r2'}, {'a'}, transitions_nfa, 'p', {'r2'})
dfa = nfa_to_dfa(nfa)

print(dfa.accepts('aa')) 


#3 a^lb^mc^n, l >= 0, m, n >= 1

transitions = {
    'a': {'a': {'a'}, '': {'b'}},  
    'b': {'b': {'b'}, '': {'c'}}, 
    'c': {'c': {'c'}, '': {'d'}},  
    'd': {} 
}

nfa = NFA({'a', 'b', 'c', 'd'}, {'a', 'b', 'c'}, transitions, 'a', {'d'})
print(nfa.accepts('abc'))
print(nfa.accepts('bbcc'))
print(nfa.accepts('aaabbccccc'))

dfa = nfa_to_dfa(nfa)

print(dfa.accepts('abc'))
print(dfa.accepts('bbcc'))
print(dfa.accepts('aaabbccccc'))

"""