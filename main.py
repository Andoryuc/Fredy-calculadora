import streamlit as st
import metodos as mt

st.set_page_config(layout="centered")

st.title("📊 Calculadora de Métodos Numéricos")

# ------------------- SELECCIÓN POR BOTONES -------------------
col1, col2 = st.columns(2)

with col1:
    metodo = st.radio(
        "📌 Métodos 1er Corte",
        ["Bisección", "Newton", "Secante"]
    )

with col2:
    metodo2 = st.radio(
        "📌 Métodos 2do Corte",
        ["Derivadas", "Trapecio", "Simpson"]
    )

# Elegir cuál usar
opcion = metodo if metodo else metodo2


# ------------------- FUNCIONES -------------------

# --------- BISECCIÓN ---------
if metodo == "Bisección":
    st.subheader("🔵 Método de Bisección")

    ecuacion = st.text_input("f(x)", placeholder="Ej: x^2 - 4")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a")
    with col2:
        b = st.number_input("b")

    tol = st.number_input("Tolerancia", value=0.001)

    if st.button("Calcular"):
        expresion, x = mt.preparar_ecuacion(ecuacion)
        raiz, estado = mt.biseccion(expresion, x, a, b, tol)

        if raiz:
            st.success(f"Raíz: {round(raiz,6)}")
        else:
            st.error("Intervalo inválido")


# --------- NEWTON ---------
elif metodo == "Newton":
    st.subheader("🟢 Método de Newton")

    ecuacion = st.text_input("f(x)")
    x0 = st.number_input("Valor inicial")
    tol = st.number_input("Tolerancia", value=0.001)

    if st.button("Calcular"):
        expresion, x = mt.preparar_ecuacion(ecuacion)
        raiz, estado = mt.newton(expresion, x, x0, tol)

        if raiz:
            st.success(f"Raíz: {round(raiz,6)}")
        else:
            st.error("Error en el método")


# --------- SECANTE ---------
elif metodo == "Secante":
    st.subheader("🟡 Método de Secante")

    ecuacion = st.text_input("f(x)")

    col1, col2 = st.columns(2)
    with col1:
        x0 = st.number_input("x0")
    with col2:
        x1 = st.number_input("x1")

    tol = st.number_input("Tolerancia", value=0.001)

    if st.button("Calcular"):
        expresion, x = mt.preparar_ecuacion(ecuacion)
        raiz, estado = mt.secante(expresion, x, x0, x1, tol)

        if raiz:
            st.success(f"Raíz: {round(raiz,6)}")
        else:
            st.error("Error en el método")


# ================== 2DO CORTE ==================

# --------- DERIVADAS ---------
elif metodo2 == "Derivadas":
    st.subheader("📐 Método de Derivadas")

    lista_x = st.data_editor(
        {"x": [0,1,2], "f(x)": [0,0,0]},
        num_rows="dynamic"
    )

    tipo = st.selectbox("Tipo", ["central", "derecha", "izquierda", "cinco"])

    x_eval = st.number_input("Valor de x donde evaluar")

    if st.button("Calcular"):
        x_vals = lista_x["x"].tolist()
        fx_vals = lista_x["f(x)"].tolist()

        # 🔥 Convertir valor real → índice
        if x_eval in x_vals:
            pos = x_vals.index(x_eval)
            resultado, estado = mt.puntos(x_vals, fx_vals, pos, tipo)

            if resultado:
                st.success(f"Resultado: {resultado}")
            else:
                st.error("No se puede calcular en esa posición")
        else:
            st.error("Ese valor de x no está en la tabla")


# --------- TRAPECIO ---------
elif metodo2 == "Trapecio":
    st.subheader("📏 Método del Trapecio")

    lista = st.data_editor(
        {"x": [0,1,2], "f(x)": [0,0,0]},
        num_rows="dynamic"
    )

    if st.button("Calcular"):
        x_vals = lista["x"].tolist()
        fx_vals = lista["f(x)"].tolist()

        resultado = mt.trapecio_datos(x_vals, fx_vals)
        st.success(f"Área: {resultado}")


# --------- SIMPSON ---------
elif metodo2 == "Simpson":
    st.subheader("📊 Método de Simpson")

    lista = st.data_editor(
        {"x": [0,1,2,3], "f(x)": [0,0,0,0]},
        num_rows="dynamic"
    )

    if st.button("Calcular"):
        x_vals = lista["x"].tolist()
        fx_vals = lista["f(x)"].tolist()

        resultado = mt.simpson_datos(x_vals, fx_vals)

        if resultado:
            st.success(f"Área: {resultado}")
        else:
            st.error("Intervalos deben ser pares")