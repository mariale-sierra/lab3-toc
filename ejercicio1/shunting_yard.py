import sys

PRECEDENCIA = {'|': 1, '_': 2, '*': 3, '+': 3, '?': 3}
CONCAT = '_'  # operador interno de concatenacion (no se usa '.' porque aparece como caracter literal en algunas regex)


def tokenizar(regex):
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == '\\' and i + 1 < len(regex):
            tokens.append(regex[i:i + 2])  # caracter escapado, ej. \( -> operando atomico
            i += 2
        elif c == '[':
            fin = regex.index(']', i)
            clase = regex[i + 1:fin]
            tokens.append('(')
            for j, ch in enumerate(clase):
                if j > 0:
                    tokens.append('|')
                tokens.append(ch)
            tokens.append(')')
            i = fin + 1
        else:
            tokens.append(c)
            i += 1
    return tokens


def es_operando(tok):
    return tok not in ('|', '(', ')', '*', '+', '?', CONCAT)


def extraer_ultima_expresion(tokens):
    if not tokens:
        raise ValueError("No hay una expresion valida antes de '+' o '?'")

    fin = len(tokens) - 1
    ultimo = tokens[fin]

    if ultimo == ')':
        parentesis = 0
        inicio = fin
        while inicio >= 0:
            tok = tokens[inicio]
            if tok == ')':
                parentesis += 1
            elif tok == '(':
                parentesis -= 1
                if parentesis == 0:
                    return inicio, tokens[inicio:fin + 1]
            inicio -= 1
        raise ValueError("Parentesis desbalanceados al expandir '+' o '?'")

    if ultimo in ('|', '(', CONCAT, '*', '+', '?'):
        raise ValueError("El operador '+' o '?' no tiene una expresion valida a la izquierda")

    return fin, [ultimo]


def expandir_extensiones(tokens):
    resultado = []

    for tok in tokens:
        if tok in ('+', '?'):
            inicio, expresion = extraer_ultima_expresion(resultado)

            if tok == '+':
                resultado = resultado[:inicio] + expresion + expresion + ['*']
            else:
                resultado = resultado[:inicio] + ['('] + expresion + ['|', '#', ')']
        else:
            resultado.append(tok)

    return resultado


def insertar_concatenacion(tokens):
    resultado = []
    for i, tok in enumerate(tokens):
        resultado.append(tok)
        if i + 1 < len(tokens):
            siguiente = tokens[i + 1]
            fin_expresion = es_operando(tok) or tok in (')', '*', '+', '?')
            inicio_expresion = es_operando(siguiente) or siguiente == '('
            if fin_expresion and inicio_expresion:
                resultado.append(CONCAT)
    return resultado


def shunting_yard(tokens):
    salida = []
    pila = []
    pasos = []

    for tok in tokens:
        if es_operando(tok):
            salida.append(tok)
            pasos.append(f"Operando '{tok}' -> Salida: {''.join(salida)} | Pila: {pila}")
        elif tok == '(':
            pila.append(tok)
            pasos.append(f"'(' -> Pila: {pila}")
        elif tok == ')':
            while pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()
            pasos.append(f"')' -> Salida: {''.join(salida)} | Pila: {pila}")
        else:
            while pila and pila[-1] != '(' and PRECEDENCIA[pila[-1]] >= PRECEDENCIA[tok]:
                salida.append(pila.pop())
            pila.append(tok)
            pasos.append(f"Operador '{tok}' -> Salida: {''.join(salida)} | Pila: {pila}")

    while pila:
        salida.append(pila.pop())
    pasos.append(f"Fin de expresion -> Salida: {''.join(salida)}")

    return salida, pasos


def convertir(regex):
    """Devuelve (postfix_tokens, postfix_string, pasos) para una expresion regular en infix."""
    tokens = tokenizar(regex)
    tokens = expandir_extensiones(tokens)
    tokens = insertar_concatenacion(tokens)
    postfix_tokens, pasos = shunting_yard(tokens)
    return postfix_tokens, ''.join(postfix_tokens), pasos


def main():
    archivo = sys.argv[1] if len(sys.argv) > 1 else "expresiones.txt"

    with open(archivo, "r", encoding="utf-8") as f:
        lineas = [linea.rstrip("\n") for linea in f if linea.strip()]

    for i, regex in enumerate(lineas, start=1):
        print(f"\nLinea {i}: {regex}")
        _, postfix, pasos = convertir(regex)
        for paso in pasos:
            print(f"  {paso}")
        print(f"  Postfix: {postfix}")


if __name__ == "__main__":
    main()
