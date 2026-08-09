"""Ejercicio 1: construye y dibuja el AST de una expresion regular a partir
de su notacion postfix (obtenida con Shunting Yard, lab. anterior)."""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shunting_yard import convertir

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # evita error con 'ε' en consola de Windows

BINARIOS = ('|', '_')  # '_' = concatenacion
UNARIOS = ('*',)
ETIQUETAS = {'_': '•', '#': 'ε'}  # simbolos internos mostrados con otro caracter


class Nodo:
    def __init__(self, simbolo, izq=None, der=None):
        self.simbolo = simbolo
        self.izq = izq
        self.der = der


def construir_arbol(postfix_tokens):
    """Recorre el postfix apilando operandos; cada operador desapila sus
    operandos, crea el nodo y lo vuelve a apilar (queda 1 nodo: la raiz)."""
    pila = []
    for tok in postfix_tokens:
        if tok in BINARIOS:
            der, izq = pila.pop(), pila.pop()
            pila.append(Nodo(tok, izq, der))
        elif tok in UNARIOS:
            pila.append(Nodo(tok, pila.pop()))
        else:
            pila.append(Nodo(tok))
    return pila[0]


def dibujar_arbol(nodo, titulo, archivo):
    posiciones = {}
    contador = [0]

    def asignar_x_y(n, profundidad):
        if n.izq:
            asignar_x_y(n.izq, profundidad + 1)
        posiciones[n] = (contador[0], -profundidad)
        contador[0] += 1
        if n.der:
            asignar_x_y(n.der, profundidad + 1)

    asignar_x_y(nodo, 0)

    fig, ax = plt.subplots(figsize=(max(6, len(posiciones) * 0.6), 6))
    for n, (x, y) in posiciones.items():
        for hijo in (n.izq, n.der):
            if hijo:
                x2, y2 = posiciones[hijo]
                ax.plot([x, x2], [y, y2], color="black", zorder=1)
    for n, (x, y) in posiciones.items():
        ax.scatter([x], [y], s=900, color="#cfe8ff", edgecolors="black", zorder=2)
        ax.text(x, y, ETIQUETAS.get(n.simbolo, n.simbolo), ha="center", va="center", fontsize=13, zorder=3)

    ax.set_title(titulo)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)


def main():
    archivo = sys.argv[1] if len(sys.argv) > 1 else "expresiones.txt"
    with open(archivo, "r", encoding="utf-8") as f:
        lineas = [linea.rstrip("\n") for linea in f if linea.strip()]

    os.makedirs("arboles", exist_ok=True)
    for i, regex in enumerate(lineas, start=1):
        postfix_tokens, postfix_str, _ = convertir(regex)
        arbol = construir_arbol(postfix_tokens)
        salida = f"arboles/arbol_{i}.png"
        dibujar_arbol(arbol, titulo=f"{regex}  ->  {postfix_str}", archivo=salida)
        print(f"Linea {i}: {regex}\n  Postfix: {postfix_str}\n  Arbol: {salida}")


if __name__ == "__main__":
    main()
