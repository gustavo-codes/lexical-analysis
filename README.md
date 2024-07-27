# lexicalAnalyser

## 1. Description

A simple lexicle analyser that implements an hypothetical language named "A" for the compilers class of the Federal University of Ceará. Here it is a quick summary on the language:

- Only has the data types `int` and `string`;
- Does not have loops or conditionals;
- Only has the operators `+`, `-`, `*`, `=`, `>`, and `<`;
- Does not have bitwise operators;
- Does not contain functions or the ability to initiate blocks;
- Does not contain macros or imports;
- All other characteristics are identical to C, including the syntax.

This lexical analyser followed these steps in order to recognize the tokens from the "A" language:

1. Implementation of regular expressions for each token
2. Implementation of an algorithm that takes as input all the regular expressions made and return a single NFA
3. Implementation of an algorithm that receives as input a single NFA and returns a DFA 
4. Implementation of the lexical analyser itself taking as base the DFA 

Example of usage

```
input

int a = 0 ;
in b = 5 + a ;
string c = “teSte” ;
```

```
output

INT VAR EQ NUM SEMICOLON
INT VAR EQ NUM ADD VAR SEMICOLON
STRING VAR EQ CONST SEMICOLON
```

## 2. Regular expressions used

1. INT: int
2. CONST: string 
3. ID: ( _ | \[a-z] | \[A-Z]) ( _ | \[a-z] | \[A-Z] | \[0-9])*
4. EQ: =
5. NUM: \[0-9]+
6. ADD: +
7. SUB: -
8. MULT: *
9. SEMICOLON: ;

## 3. On the structure of the folder and files

- `automata_and_re`: Provide all the automatas and regular expressions needed.
    1. `NFA.py`: Defines a class for implementing a NFA
    2. `DFA.py`: Defines a class for implementing a DFA
    3. `re.txt`: all the regular expressions for each token of "A"

- `converters`: This directory has all the functions regarding the translations necessary for the implementation of the lexical analyser. Such translations are listed bellow:
    1. regular expressions to NFA (defined on `er_2_nfa.py`):
        - receives all the regular expressions that are defined on `re.txt` and return a single NFA for it.
        - The NFA itself is them written into a file `NFA.txt` that describes it.
        - It make such convertion using the Thompson's algorithm
    1. NFA to DFA: 
        - Receives a NFA and returns a DFA (defined on `er_2_dfa.py`)
        - The resulting DFA is then written into `DFA.txt`
- `lexicalAnalyserA.py`:
    - It executs the lexical analyser itself
    - If `DFA.txt` is not empty, then it uses the DFA defined there.
    - If `DFA.txt` is empty, recursively calls the translation algorithms

## 4.On the classes used

1. NFA(q, sigma, delta, q0, f)
    - Defined on `automata_and_re/NFA.py`
    - `q` : `[INT]`
        - is a list of integers that represent the set of all the states of the NFA
        - each state is represented by a number
    - `sigma`: [`CHAR`]
        - is a list of characters that represent the alphabet recognized by the NFA
    - `delta`:
        - > {INT:{CHAR:[INT]} <br>
          > outgoing state : input symbol:[incoming states]
        - Defines the transiction function.
    - `q0`: `INT`
        - an intenger that represents the initial state of the NFA
    - `f`: `[INT]`
        - A list of integers that represent the set of final states
2. `DFA.py`
    - Defined on `Defined on `automata_and_re/DFA.py`
    - It is basically the NFA, but with small changes to the transiction function
    

---