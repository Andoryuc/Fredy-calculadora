import streamlit as st
import metodos as mt

st.title("📊 Métodos Numéricos")

opcion = st.sidebar.selectbox(
    "Seleccione un método",
    ["Bisección", "Newton", "Secante", "Derivadas", "Trapecio", "Simpson"]
)

# ---------------- BISECCIÓN ----------------
if opcion == "Bisección":
    st.header("Método de Bisección")

    ecuacion = st.text_input("Ecuación")
    a = st.number_input("a")
    b = st.number_input("b")
    tol = st.number_input("Tolerancia", value=0.001)

    if st.button("Calcular"):
        if ecuacion:
            expresion, x = mt.preparar_ecuacion(ecuacion)
            raiz, estado = mt.biseccion(expresion, x, a, b, tol)

            if raiz is not None:
                st.success(f"Raíz: {raiz} | Iteraciones: {estado}")
            else:
                st.error("Intervalo inválido")

# ---------------- NEWTON ----------------
elif opcion == "Newton":
    st.header("Método de Newton")

    ecuacion = st.text_input("Ecuación")
    x0 = st.number_input("Valor inicial")
    tol = st.number_input("Tolerancia", value=0.001)

    if st.button("Calcular"):
        if ecuacion:
            expresion, x = mt.preparar_ecuacion(ecuacion)
            raiz, estado = mt.newton(expresion, x, x0, tol)

            if raiz is not None:
                st.success(f"Raíz: {raiz} | Iteraciones: {estado}")
            else:
                st.error("Error (derivada cero o no converge)")

# ---------------- SECANTE ----------------
elif opcion == "Secante":
    st.header("Método de la Secante")

    ecuacion = st.text_input("Ecuación")
    x0 = st.number_input("x0")
    x1 = st.number_input("x1")
    tol = st.number_input("Tolerancia", value=0.001)

    if st.button("Calcular"):
        if ecuacion:
            expresion, x = mt.preparar_ecuacion(ecuacion)
            raiz, estado = mt.secante(expresion, x, x0, x1, tol)

            if raiz is not None:
                st.success(f"Raíz: {raiz} | Iteraciones: {estado}")
            else:
                st.error("Error (división o no converge)")

# ---------------- DERIVADAS ----------------
elif opcion == "Derivadas":
    st.header("Método de 3 y 5 puntos")

    texto_x = st.text_input("lista_x (separada por espacio)")
    texto_fx = st.text_input("lista_fx (separada por espacio)")

    pos = st.number_input("Posición", step=1)
    tipo = st.selectbox("Tipo", ["central", "derecha", "izquierda", "cinco"])

    if st.button("Calcular"):
        if texto_x and texto_fx:
            lista_x = list(map(float, texto_x.split()))
            lista_fx = list(map(float, texto_fx.split()))

            resultado, estado = mt.puntos(lista_x, lista_fx, int(pos), tipo)

            if resultado is not None:
                st.success(f"Resultado: {resultado}")
            else:
                st.error("Error en datos o posición")

# ---------------- TRAPECIO ----------------
elif opcion == "Trapecio":
    st.header("Método del Trapecio")

    texto_x = st.text_input("lista_x")
    texto_fx = st.text_input("lista_fx")

    if st.button("Calcular"):
        if texto_x and texto_fx:
            lista_x = list(map(float, texto_x.split()))
            lista_fx = list(map(float, texto_fx.split()))

            resultado = mt.trapecio_datos(lista_x, lista_fx)
            st.success(f"Área: {resultado}")

# ---------------- SIMPSON ----------------
elif opcion == "Simpson":
    st.header("Método de Simpson")

    texto_x = st.text_input("lista_x")
    texto_fx = st.text_input("lista_fx")

    if st.button("Calcular"):
        if texto_x and texto_fx:
            lista_x = list(map(float, texto_x.split()))
            lista_fx = list(map(float, texto_fx.split()))

            resultado = mt.simpson_datos(lista_x, lista_fx)

            if resultado is not None:
                st.success(f"Área: {resultado}")
            else:
                st.error("Error: intervalos deben ser pares")