# Analisador Léxico
Ele tem a função de ler um código na linguagem A especificada abaixo e verificar se há algum erro léxico. Após verificar de que não há nenhum erro lexico, ele retorna os tokens dá linguagem que servirão mais tarde como entrada de um analisador sintático.
## A linguagem
A Linguagem A é definida a partir da Linguagem C, as características da A são:
- Possui apenas os tipos de dados int e string;
- Não possui laços de repetição e nem condicionais;
- Possui somente os operadores +, - *, =, > e <;
- Não possui operadores de bit;
- Não contem funções e nem a possibilidade de iniciar blocos;
- Não contem macros ou importações;
- As demais características são idênticas ao C, inclusive a sintaxe.

## Uso do analisador
1. Escreva seu código no arquivo `input.txt`.
    * **TODAS** as palavra devem estar **SEPARADAS** por pelo menos um espaço.
    * Nenhuma string deve conter um espaço dentro dela (ex: string a = "joão pedro").
    * O ponto e vírgula **NÃO DEVE** estar colado em nenhuma palavra (ex: int a;)
2. Execute o arquivo `lexicalAnalyserA.py`.
    * Faça isso rodando o comando `python lexicalAnalyserA.py` no windows.
    * Ou `python3 lexicalAnalyserA.py` no linux.
3. Abra o arquivo `output.txt`, se o código estiver lexicamente correto, você verá os tokens, se o código tiver algum erro léxico você verá ERRO.

### Exemplo de entrada
```
int  a  = 2 ;
int  b  = 4 ;
string   pedro =   "Pedro"  ;
int soma = a + b  * c - 2 ;

int c = a - b ;             
```

### Saída
```
INT ID EQ_OP NUM SEMICOLON 
INT ID EQ_OP NUM SEMICOLON 
STRING ID EQ_OP CONST SEMICOLON 
INT ID EQ_OP ID SUM_OP ID MULT_OP ID SUB_OP NUM SEMICOLON 

INT ID EQ_OP ID SUB_OP ID SEMICOLON 

```

## Tokens
Os tokens dentro do código são representados em forma pós-fixa e sem parênteses. Por exemplo, a expressão regular $(i\cdot n)\cdot t$ é representada $in\cdot t \cdot $. Os tokens e o que eles representam podem ser encontrados no arquivo `tokens.txt`
| Token    | Expressão Regular (Formato pós-fixo sem parênteses) |
| -------- | ------- |
| INT  |   in.t.  |
| STRING | st.r.i.n.g.   |
| EQ_OP    | =   |
| MULT_OP    | *   |
| SUB_OP    | -   |
| SUM_OP    | +   |
| SEMICOLON    | ;   |
| ID    | _ab\|c\|d\|e\|f\|g\|h\|i\|j\|k\|l\|m\|n\|o\|p\|q\|r\|s\|t\|u\|v\|w\|x\|y\|z\|\|AB\|C\|D\|E\|F\|G\|H\|I\|J\|K\|L\|M\|N\|O\|P\|Q\|R\|S\|T\|U\|V\|W\|X\|Y\|Z\|\|_ab\|c\|d\|e\|f\|g\|h\|i\|j\|k\|l\|m\|n\|o\|p\|q\|r\|s\|t\|u\|v\|w\|x\|y\|z\|\|AB\|C\|D\|E\|F\|G\|H\|I\|J\|K\|L\|M\|N\|O\|P\|Q\|R\|S\|T\|U\|V\|W\|X\|Y\|Z\|\|01\|2\|3\|4\|5\|6\|7\|8\|9\|\|?.   |
| NUM    | 01\|2\|3\|4\|5\|6\|7\|8\|9\|01\|2\|3\|4\|5\|6\|7\|8\|9\|?. |
| CONST   | "ab\|c\|d\|e\|f\|g\|h\|i\|j\|k\|l\|m\|n\|o\|p\|q\|r\|s\|t\|u\|v\|w\|x\|y\|z\|?AB\|C\|D\|E\|F\|G\|H\|I\|J\|K\|L\|M\|N\|O\|P\|Q\|R\|S\|T\|U\|V\|W\|X\|Y\|Z\|?.01\|2\|3\|4\|5\|6\|7\|8\|9\|?. ?.<?.>?.*?.-?.+?.=?.;?._?.?.\".   |
| GREATER_OP   | >   |
| LESS_OP    | <   |

## Conversão de ER para NFA
O arquivo `er_2_nfa.py` contém o algorítmo que converte uma expressão regular em um autômato finito não deterministico baseado no [Algoritmo de Thompson](https://pt.wikipedia.org/wiki/Algoritmo_de_Thompson#:~:text=Em%20ci%C3%AAncia%20da%20computa%C3%A7%C3%A3o%2C%20Algoritmo,casar%20palavras%20com%20express%C3%B5es%20regulares.). Ele usa a função `assemble()` para juntar todos os autômatos de cada expressão regular em um só.

## Conversão de NFA para DFA
A conversão de autômato finito não determinístico para determinístico é feita no arquivo `nfa_2_dfa.py`.

## A análise léxica
É feita no arquivo `lexicalAnalyserA.py`. Ela consiste em chamar a função `assemble()` para montar o autômato e converter esse NFA para DFA. Tendo esse autômato em mãos, basta que, para cada palavra da entrada, o autômato faça a computação da mesma. Após essa computação ele consulta a tabela de estados finais:

``` py
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
```

O DFA retorna um estado que é um conjunto de estados do NFA original. O analisador checa se nesse conjunto há algum estado final dos tokens listados, se houver então escreve na saída o token.

### Ambiguidade
A ambiguidade ocorre apenas em dois casos, quando lemos `string` ou `int`, pois essas palavras podem ser tanto identificadores quando as palavras reservadas. Para resolver isso basta sempre que cair nesse caso, escrever o token das palavras reservadas já que elas tem precedência sobre o identificador.
