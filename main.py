import streamlit as st
import metodos as mt

st.set_page_config(page_title="Métodos Numéricos", layout="centered")

st.title("🧮 Calculadora de Métodos Numéricos")

# ------------------ SELECCIÓN DE CORTE ------------------
corte = st.radio(
    "Selecciona el corte",
    ["1er Corte", "2do Corte"],
    horizontal=True
)

st.divider()

# ------------------ MÉTODOS 1ER CORTE ------------------
if corte == "1er Corte":

    st.subheader("📌 Métodos de raíces")

    metodo = st.radio(
        "Selecciona el método",
        ["Bisección", "Newton", "Secante"],
        horizontal=True
    )

    st.divider()

    # --------- BISECCIÓN ---------
    if metodo == "Bisección":
        st.markdown("### 🔵 Bisección")

        ecuacion = st.text_input("f(x)", placeholder="Ej: x^2 - 4")

        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("a")
        with col2:
            b = st.number_input("b")

        tol = st.number_input("Tolerancia", value=0.001)

        if st.button("🟦 Calcular"):
            if ecuacion:
                expresion, x = mt.preparar_ecuacion(ecuacion)
                raiz, estado = mt.biseccion(expresion, x, a, b, tol)

                if raiz is not None:
                    st.success(f"Raíz ≈ {round(raiz,6)}")
                else:
                    st.error("Intervalo inválido")

    # --------- NEWTON ---------
    elif metodo == "Newton":
        st.markdown("### 🟢 Newton")

        ecuacion = st.text_input("f(x)")
        x0 = st.number_input("Valor inicial")
        tol = st.number_input("Tolerancia", value=0.001)

        if st.button("🟩 Calcular"):
            if ecuacion:
                expresion, x = mt.preparar_ecuacion(ecuacion)
                raiz, estado = mt.newton(expresion, x, x0, tol)

                if raiz is not None:
                    st.success(f"Raíz ≈ {round(raiz,6)}")
                else:
                    st.error("Error en el método")

    # --------- SECANTE ---------
    elif metodo == "Secante":
        st.markdown("### 🟡 Secante")

        ecuacion = st.text_input("f(x)")

        col1, col2 = st.columns(2)
        with col1:
            x0 = st.number_input("x0")
        with col2:
            x1 = st.number_input("x1")

        tol = st.number_input("Tolerancia", value=0.001)

        if st.button("🟨 Calcular"):
            if ecuacion:
                expresion, x = mt.preparar_ecuacion(ecuacion)
                raiz, estado = mt.secante(expresion, x, x0, x1, tol)

                if raiz is not None:
                    st.success(f"Raíz ≈ {round(raiz,6)}")
                else:
                    st.error("Error en el método")


# ------------------ MÉTODOS 2DO CORTE ------------------
elif corte == "2do Corte":

    st.subheader("📌 Métodos con datos")

    metodo = st.radio(
        "Selecciona el método",
        ["Derivadas", "Trapecio", "Simpson"],
        horizontal=True
    )

    st.divider()

    # --------- DERIVADAS ---------
    if metodo == "Derivadas":
        st.markdown("### 📐 Derivadas (3 y 5 puntos)")

        tabla = st.data_editor(
            {"x": [0,1,2], "f(x)": [0,0,0]},
            num_rows="dynamic"
        )

        tipo = st.selectbox("Tipo", ["central", "derecha", "izquierda", "cinco"])
        x_eval = st.number_input("Valor de x donde evaluar")

        if st.button("🟪 Calcular"):
            x_vals = tabla["x"].tolist()
            fx_vals = tabla["f(x)"].tolist()

            if x_eval in x_vals:
                pos = x_vals.index(x_eval)
                resultado, estado = mt.puntos(x_vals, fx_vals, pos, tipo)

                if resultado is not None:
                    st.success(f"Resultado ≈ {resultado}")
                else:
                    st.error("No se puede calcular en esa posición")
            else:
                st.error("Ese valor no está en la tabla")

    # --------- TRAPECIO ---------
    elif metodo == "Trapecio":
        st.markdown("### 📏 Trapecio")

        tabla = st.data_editor(
            {"x": [0,1,2], "f(x)": [0,0,0]},
            num_rows="dynamic"
        )

        if st.button("🟫 Calcular"):
            x_vals = tabla["x"].tolist()
            fx_vals = tabla["f(x)"].tolist()

            resultado = mt.trapecio_datos(x_vals, fx_vals)
            st.success(f"Área ≈ {resultado}")

    # --------- SIMPSON ---------
    elif metodo == "Simpson":
        st.markdown("### 📊 Simpson")

        tabla = st.data_editor(
            {"x": [0,1,2,3], "f(x)": [0,0,0,0]},
            num_rows="dynamic"
        )

        if st.button("🟧 Calcular"):
            x_vals = tabla["x"].tolist()
            fx_vals = tabla["f(x)"].tolist()

            resultado = mt.simpson_datos(x_vals, fx_vals)

            if resultado is not None:
                st.success(f"Área ≈ {resultado}")
            else:
                st.error("Intervalos deben ser pares")