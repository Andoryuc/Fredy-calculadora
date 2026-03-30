import streamlit as st
import metodos as mt
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Métodos Numéricos", layout="centered")

st.title("🧮 Calculadora de Métodos Numéricos")

# -------- FUNCIÓN PARA GRAFICAR --------
def graficar_funcion(expresion, x_simbolo, raiz=None):
    x_vals = np.linspace(-10, 10, 400)
    y_vals = []

    for val in x_vals:
        try:
            y_vals.append(float(expresion.subs(x_simbolo, val)))
        except:
            y_vals.append(np.nan)

    plt.figure()
    plt.axhline(0)
    plt.axvline(0)
    plt.plot(x_vals, y_vals)

    if raiz is not None:
        plt.scatter(raiz, 0)
        plt.text(raiz, 0, f"{round(raiz,4)}")

    st.pyplot(plt)

# ------------------ CORTE ------------------
corte = st.radio("Selecciona el corte", ["1er Corte", "2do Corte"], horizontal=True)

st.divider()

# ================== 1ER CORTE ==================
if corte == "1er Corte":

    metodo = st.radio("Método", ["Bisección", "Newton", "Secante"], horizontal=True)

    st.divider()

    # -------- BISECCIÓN --------
    if metodo == "Bisección":
        st.subheader("Bisección")

        ecuacion = st.text_input("f(x)", "x^2 - 4")

        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("a", value=0.0)
        with col2:
            b = st.number_input("b", value=3.0)

        tol = st.number_input("Tolerancia", value=0.001)

        if st.button("Calcular"):
            expresion, x = mt.preparar_ecuacion(ecuacion)
            raiz, estado = mt.biseccion(expresion, x, a, b, tol)

            if raiz is not None:
                st.success(f"Raíz ≈ {raiz}")
                graficar_funcion(expresion, x, raiz)
            else:
                st.error("Intervalo inválido")

    # -------- NEWTON --------
    elif metodo == "Newton":
        st.subheader("Newton")

        ecuacion = st.text_input("f(x)", "x^2 - 4")
        x0 = st.number_input("Valor inicial", value=2.0)
        tol = st.number_input("Tolerancia", value=0.001)

        if st.button("Calcular"):
            expresion, x = mt.preparar_ecuacion(ecuacion)
            raiz, estado = mt.newton(expresion, x, x0, tol)

            if raiz is not None:
                st.success(f"Raíz ≈ {raiz}")
                graficar_funcion(expresion, x, raiz)
            else:
                st.error("Error en el método")

    # -------- SECANTE --------
    elif metodo == "Secante":
        st.subheader("Secante")

        ecuacion = st.text_input("f(x)", "x^2 - 4")

        col1, col2 = st.columns(2)
        with col1:
            x0 = st.number_input("x0", value=0.0)
        with col2:
            x1 = st.number_input("x1", value=3.0)

        tol = st.number_input("Tolerancia", value=0.001)

        if st.button("Calcular"):
            expresion, x = mt.preparar_ecuacion(ecuacion)
            raiz, estado = mt.secante(expresion, x, x0, x1, tol)

            if raiz is not None:
                st.success(f"Raíz ≈ {raiz}")
                graficar_funcion(expresion, x, raiz)
            else:
                st.error("Error en el método")

# ================== 2DO CORTE ==================
elif corte == "2do Corte":

    metodo = st.radio("Método", ["Derivadas", "Trapecio", "Simpson"], horizontal=True)

    st.divider()

    # -------- DERIVADAS --------
    if metodo == "Derivadas":
        tabla = st.data_editor({"x":[0,1,2],"f(x)":[0,0,0]}, num_rows="dynamic")

        tipo = st.selectbox("Tipo", ["central","derecha","izquierda","cinco"])
        x_eval = st.number_input("Valor de x")

        if st.button("Calcular"):
            x_vals = tabla["x"].tolist()
            fx_vals = tabla["f(x)"].tolist()

            if x_eval in x_vals:
                pos = x_vals.index(x_eval)
                resultado, estado = mt.puntos(x_vals, fx_vals, pos, tipo)

                if resultado is not None:
                    st.success(f"Resultado ≈ {resultado}")
                else:
                    st.error("Error en cálculo")
            else:
                st.error("x no está en la tabla")

    # -------- TRAPECIO --------
    elif metodo == "Trapecio":
        tabla = st.data_editor({"x":[0,1,2],"f(x)":[0,0,0]}, num_rows="dynamic")

        if st.button("Calcular"):
            x_vals = tabla["x"].tolist()
            fx_vals = tabla["f(x)"].tolist()

            resultado = mt.trapecio_datos(x_vals, fx_vals)
            st.success(f"Área ≈ {resultado}")

    # -------- SIMPSON --------
    elif metodo == "Simpson":
        tabla = st.data_editor({"x":[0,1,2,3],"f(x)":[0,0,0,0]}, num_rows="dynamic")

        if st.button("Calcular"):
            x_vals = tabla["x"].tolist()
            fx_vals = tabla["f(x)"].tolist()

            resultado = mt.simpson_datos(x_vals, fx_vals)

            if resultado is not None:
                st.success(f"Área ≈ {resultado}")
            else:
                st.error("Intervalos deben ser pares")