# Laboratorio No. 3

Video de ejecución (no listado): *pendiente de subir a YouTube*

## Estructura del repositorio

- `ejercicio1/` — código del Ejercicio 1 (infix → postfix → AST).
- `ejercicio2/` — respuesta del Ejercicio 2 (Lema de Arden) en PDF.

## Ejercicio 1

Convierte una expresión regular de infix a postfix (Shunting Yard, del
laboratorio anterior) y con ese postfix construye y dibuja el Árbol de
Sintaxis Abstracta (AST) correspondiente.

- `shunting_yard.py` — código del laboratorio anterior (infix a postfix),
  necesario aquí porque su salida es la entrada del Ejercicio 1. Expande
  `a+` a `aa*` y `a?` a `(a|ε)` antes de convertir.
- `arbol.py` — construye el AST a partir del postfix usando una pila
  (apila operandos; cada operador desapila sus hijos y apila el nodo
  resultante) y lo dibuja con `matplotlib`.
- `expresiones.txt` — las 4 expresiones regulares del enunciado.

Ejecución (desde `ejercicio1/`):

```
python arbol.py expresiones.txt
```

Genera `arboles/arbol_1.png` ... `arbol_4.png`, uno por cada línea del
archivo de entrada.

## Ejercicio 2

Ver `ejercicio2/ejercicio2.pdf`.
