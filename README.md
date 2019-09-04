# Compilador
Aplicação feita em __*Python*__ para a aula de __*Compiladores*__

---

### Fase 1
__Análise Léxica__:
* Definição de padrões através do uso de palavras-chave
* Implementação do Autômato Finito Determinístico para interpretação da linguagem proposta
![AFD](https://imgur.com/a/3oP3pWh)
* Fluxo de caracteres é lido da esquerda para a direita e agrupado em tokens;
* Forma a gramática

---
### Fase 2
__Análise Sintática__:
Agrupamento de tokens de forma hierarquica em coleções aninhadas com significado coletivo, ou seja, algo que foi declarado em linha deve fazer sentido em código.
* Reconhece estruturas sintáticas do fonte utilizando os tokens.
* É necessário uma gramática.
* Análise Top-Down, LL parsing;
* Análise Bottom-Up, LR parsing.
* Definição Dirigida pela Sintaxe;
* Esquema de Tradução
---
### Fase 3
__Análise Semântica__:
Realiza verificações a fim de assegurar que os componentes de um programa combinam de forma significativa.
* Coleta informações sobre tipos de identificadores e expressões;
* Verifica a consistência das operações do programa fonte de acordo com a definição da linguagem.
* Verificação de tipos.
---
### Definições
__Linguagem__:
```
Programa → Classe EOF
Classe → "class" ID ":" ListaFuncao Main "end" "."
DeclaraID → TipoPrimitivo ID ";"
ListaFuncao → ListaFuncao Funcao | ε
Funcao → "def" TipoPrimitivo ID "(" ListaArg ")" ":" (DeclaraID)∗ ListaCmd Retorno "end" ";"
ListaArg → Arg "," ListaArg | Arg
Arg → TipoPrimitivo ID
Retorno → "return" Expressao ";" | ε
Main → "defstatic" "void" "main" "(" "String" "[" "]" ID ")" ":" (DeclaraID)∗ ListaCmd "end" ";"
TipoPrimitivo → "bool" | "integer" | "String" | "double" | "void"
ListaCmd → ListaCmd Cmd | ε
Cmd → CmdIF | CmdWhile | CmdAtribui | CmdFuncao | CmdWrite
CmdIF → "if" "(" Expressao ")" ":" ListaCmd "end" ";" | "if" "(" Expressao ")" ":" ListaCmd "else" ":" ListaCmd "end" ";"
CmdWhile → "while" "(" Expressao ")" ":" ListaCmd "end" ";"
CmdWrite → "write" "(" Expressao ")" ";"
CmdAtribui → ID "=" Expressao ";"
CmdFuncao → ID "(" (Expressao ("," Expressao)∗ )? ")" ";"
Expressao → Expressao Op Expressao | ID | ID "(" (Expressao ("," Expressao)∗ )? ")" | ConstInteger | ConstDouble | ConstString | "true" | "false" | OpUnario Expressao | "(" Expressao")"
Op → "or" | "and" | "<" | "<=" | ">" | ">=" | "==" | "!=" | "/" | "*" | "-" | "+"
OpUnario → "-" | "!" 
```
__Descrição dos padrões propostos__:

* ID: deve iniciar com uma letra seguida de 0 ou mais produções de letras, dígitos e/ou caracteres _.
* ConstInteger: cadeia numérica contendo 1 ou mais produções de dígitos.
* ConstDouble cadeia numérica contendo 1 ou mais produções de dígitos, tendo em seguida um símbolo de ponto (.) e, em seguida, 1 ou mais produções de dígitos.
* ConstString: deve iniciar e finalizar com o caractere aspas (") contendo entre eles uma sequência de 1 ou mais produções de letras, dígitos e/ou símbolos da tabela ASCII – exceto o próprio caractere aspas.
* EOF é o código de fim de arquivo.
* Aspas na gramática apenas destacam os terminais, e os diferencia dos não-terminais.
* Apenas comentários de uma linha são permitidos e seguem o padrão de Python.
