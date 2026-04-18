import sympy as sp
import numpy as np



def preparar_ecuacion(ecuacion):
  # Definimos la variable simbólica x
  x = sp.symbols("x")
    
  texto = ecuacion.replace("^", "**")
  texto= texto.replace("√", "sqrt")
  # Convertimos el texto a una expresión matemática  
  expresion = sp.sympify(texto)
    
  return expresion, x


#METODOS 1 CORTE FISICA

#------------ METODO DE BICCEPCION-----------------

def biseccion(expresion, x, a, b, tolerancia):
  
  f_a = float(expresion.subs(x, a))
  f_b = float(expresion.subs(x, b))

  
  if f_a * f_b >= 0:
    return None, 0

  iteraciones = int(np.ceil(np.log2((b - a) / tolerancia)))
  
  for i in range(iteraciones):
    c = (a + b) / 2
    f_c = float(expresion.subs(x, c))


    if f_a * f_c < 0:
      b = c
      f_b = f_c
    else:
      a = c
      f_a = f_c

  
  raiz = (a + b) / 2

  return raiz, iteraciones

#-------------------------------------------------

#------------ METODO DE NEWTON-----------------

def newton(expresion, x, x0, tolerancia, max_iter=100):
    
  # Derivada de la función
  derivada = sp.diff(expresion, x)
    
  # Valor inicial
  x_actual = x0
    
  for i in range(max_iter):
        
    # Evaluar función y derivada
    f_val = float(expresion.subs(x, x_actual))
    f_der = float(derivada.subs(x, x_actual))
        
    # Evitar división por cero
    if f_der == 0:
      return None, 0
        
    # Fórmula de Newton
    x_nuevo = x_actual - (f_val / f_der)
        
    # Verificar tolerancia
    if abs(x_nuevo - x_actual) < tolerancia:
      return x_nuevo, i+1
        
    # Actualizar valor
    x_actual = x_nuevo
  return None, 1

#-------------------------------------------------

#------------ METODO DE SECANTE-------------------

def secante(expresion, x, x0, x1, tolerancia, max_iter=100):
    
  # Valores iniciales
  x_anterior = x0
  x_actual = x1

  for i in range(max_iter):
        
    f_anterior = float(expresion.subs(x, x_anterior))
    f_actual = float(expresion.subs(x, x_actual))

    # Evitar división por cero
    if (f_actual - f_anterior) == 0:
      return None, 0
        
    # Fórmula de la secante
    x_nuevo = x_actual - (f_actual * (x_actual - x_anterior)) / (f_actual - f_anterior)

    # Verificar tolerancia
    if abs(x_nuevo - x_actual) < tolerancia:
      return x_nuevo, i+1

    # Actualizar valores
    x_anterior = x_actual
    x_actual = x_nuevo
  return None, 1



#METODOS 2 CORTE FISICA

#------------ METODO DE 3 Y 5 PUNTOS -------------------

def puntos(lista_x :list, lista_fx :list, posicion_incial :int, seleccion :str):
 
  h = (lista_x[1]-lista_x[0])
    
    # punto central
  if seleccion == "central":
    if posicion_incial == 0 or posicion_incial == len(lista_x)-1:
      return None, 0
    resultado = (lista_fx[posicion_incial + 1] - lista_fx[posicion_incial - 1]) / (2 * h)

    #derecha(forward)
  elif seleccion  == "derecha":
    if posicion_incial + 2 > len(lista_x)-1:
      return None, 1
    resultado = (-3 * lista_fx[posicion_incial] + 4 * lista_fx[posicion_incial + 1] - lista_fx[posicion_incial + 2]) / (2*h)
  
  #izquierda(back)
  elif seleccion == "izquierda":
    if posicion_incial - 2 < 0:
      return None, 2
    resultado = (3 * lista_fx[posicion_incial] - 4 * lista_fx[posicion_incial - 1] + lista_fx[posicion_incial - 2]) / (2*h)
  # 5 puntos
  else:
    if posicion_incial - 2 < 0 or posicion_incial + 2 > len(lista_x)-1: 
      return None, 3
    resultado = (-lista_fx[posicion_incial + 2] + 8 * lista_fx[posicion_incial + 1] - 8 * lista_fx[posicion_incial - 1] + lista_fx[posicion_incial - 2] ) / (12*h)

  return resultado, -1

#----------- METODO TRAPECIO ----------------
def trapecio_datos(lista_x :list, lista_fx :list):
    
  n = len(lista_x)
  resultado = 0

  for i in range(n - 1):
    h = lista_x[i+1] - lista_x[i]
    resultado += (h * (lista_fx[i] + lista_fx[i+1])) / 2

  return resultado


#----------- METODO SIMPSON ----------------

def simpson_datos(lista_x, lista_fx):

  n = len(lista_x) - 1  # número de intervalos

  # Validación: número de intervalos debe ser par
  if n % 2 != 0:
    return None, 1

  h = lista_x[1] - lista_x[0]

  suma = 0

  for i in range(1, n):
    if (i & 1) == 0:
      suma += 2 * lista_fx[i]
    else:
      suma += 4 * lista_fx[i]

  resultado = (h / 3) * (lista_fx[0] + suma + lista_fx[-1])

  return resultado, -1

#----------- METODO SIMPSON (POR ECUACION) ----------------

def simpson_ecuacion(expresion, x, a, b, n):
    # Validación: el número de intervalos (n) debe ser par
    if n % 2 != 0:
        return None, 1  # Retorna 1 como código de error

    h = (b - a) / n
    f_a = float(expresion.subs(x, a))
    f_b = float(expresion.subs(x, b))

    suma = f_a + f_b

    for i in range(1, n):
        x_i = a + i * h
        f_xi = float(expresion.subs(x, x_i))
        
        if i % 2 == 0:
            suma += 2 * f_xi
        else:
            suma += 4 * f_xi

    resultado = (h / 3) * suma

    return resultado, -1