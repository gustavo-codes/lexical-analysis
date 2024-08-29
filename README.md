# Analizador Léxico
Ele tem a função de ler um código na linguagem A especificada abaixo e verificar se há algum erro léxico. Após verificar de que não há nenhum erro lexico, ele retorna os tokens dá linguagem que servirão mais tarde como entrada de um analizador sintático.
## A liguagem
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