INE5426 - Construção de Compiladores
Análise de Código-Fonte e Síntese de Código Intermediário

Grupo:
Bruno Pamplona Huebes
Eric Fernandes Evaristo
Gabriela Furtado da Silveira
Otávio Wada

Descrição:

Compilador para a variação seguinte da linguagem ConvCC-2024-1:

PROGRAM → STATEMENT | FUNCLIST | ε
FUNCLIST → FUNCDEF MOREFUNCS
MOREFUNCS → FUNCLIST | ε
FUNCDEF → def ident(PARAMLIST) {STATELIST}
PARAMLIST → TYPE PARAMETER
PARAMETER → ident MAYBEPARAMS
MAYBEPARAMS → , PARAMLIST | ε
TYPE → int | float | string
STATEMENT → VARDECL; | ATRIBSTAT; | PRINTSTAT; | READSTAT; | RETURNSTAT; |
IFSTAT | FORSTAT | {STATELIST} | break; | ;
VARDECL → TYPE ident ARRAYSIZE
ARRAYSIZE → [int_constant] MAYBEARRAY | ε
MAYBEARRAY  → ARRAYSIZE | ε
ATRIBSTAT → LVALUE = ATRIBEXPR
ATRIBEXPR → EXPRESSION | ALLOCEXPRESSION | FUNCCALL
FUNCCALL → call ident(PARAMLISTCALL)
PARAMLISTCALL → ident SOCALLMEMAYBE | ε
SOCALLMEMAYBE → , PARAMLISTCALL | ε
PRINTSTAT → print EXPRESSION
READSTAT → read LVALUE
RETURNSTAT → return EXPRESSION
IFSTAT → if (EXPRESSION) {STATELIST} MAYBEELSE
MAYBEELSE → else {STATELIST} | ε
FORSTAT → for (ATRIBSTAT; EXPRESSION; ATRIBSTAT) STATEMENT
STATELIST → STATEMENT MAYBESTATELIST
MAYBESTATELIST → STATELIST | ε
ALLOCEXPRESSION → new TYPE [NUMEXPRESSION] INDEXEXPRESSION
INDEXEXPRESSION → [NUMEXPRESSION] INDEXEXPRESSION | ε
EXPRESSION → NUMEXPRESSION MAYBECOMPARE
MAYBECOMPARE → COMPARISON NUMEXPRESSION | ε
COMPARISON → < | > | <= | >= | == | !=
NUMEXPRESSION → TERM INDEXTERM
INDEXTERM →ADDSUB TERM INDEXTERM | ε
TERM → UNARYEXPR MULTUNARY
MULTUNARY → MULDIV UNARYEXPR MULTUNARY | ε
MULDIV → * | / | % | and
ADDSUB → + | - | or
UNARYEXPR → + FACTOR | − FACTOR | FACTOR | not FACTOR
FACTOR → int_constant | float_constant | string_constant | null | LVALUE | (EXPRESSION)
LVALUE → ident INDEXEXPRESSION


Execução:

Por utilizar Python, o compilador pode ser executado diretamente com o comando “make ARGS=[entrada.txt]“ com entrada.txt sendo o arquivo de código a ser analisado.

ex.:
>make ARGS=sample_programs/math.txt

Alguns programas teste estão incluídos na pasta sample_programs, os principais sendo math.txt,data.txt, e datetime_calc.txt