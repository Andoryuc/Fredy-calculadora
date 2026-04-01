import streamlit as st
import metodos as mt
import streamlit.components.v1 as components

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="AFCC-Q | Métodos Numéricos", layout="centered")

# --- FUNCIÓN PARA EL IFRAME DE GEOGEBRA ---
def geogebra_component(ecuacion):
    # Ajustamos la ecuación de Python a formato GeoGebra
    ggb_ecuacion = ecuacion.replace("**", "^")
    
    html_code = f"""
    <script src="https://www.geogebra.org/apps/deployggb.js"></script>
    <div id="ggb-element" style="border: 2px solid #00f2ff; border-radius: 15px; overflow: hidden;"></div>
    <script>
        var params = {{
            "appName": "graphing",
            "width": 700,
            "height": 400,
            "showToolBar": false,
            "showAlgebraInput": false,
            "showMenuBar": false,
            "enableRightClick": true,
            "appletOnLoad": function(api) {{
                api.evalCommand("f(x) = {ggb_ecuacion}");
                api.setColor("f", 255, 0, 0); // Color Neón
                api.setThickness("f", 5);
            }}
        }};
        var applet = new GGBApplet(params, true);
        window.onload = function() {{ applet.inject('ggb-element'); }};
    </script>
    """
    components.html(html_code, height=420)

# --- ESTILO ---
st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🧮 Calculadora de Métodos Numéricos</h1>", unsafe_allow_html=True)

# ------------------ SELECCIÓN DE CORTE ------------------
corte = st.radio("Selecciona el corte", ["1er Corte", "2do Corte"], horizontal=True)
st.divider()

# ------------------ MÉTODOS 1ER CORTE ------------------
if corte == "1er Corte":
    st.subheader("📌 Métodos de raíces")
    metodo = st.radio("Selecciona el método", ["Bisección", "Newton", "Secante"], horizontal=True)
    st.divider()

    # Inputs comunes
    ecuacion = st.text_input("f(x)", placeholder="Ej: x^2 - 4")
    
    # Botón para mostrar gráfica antes de calcular
    if st.button("🖼️ Mostrar Gráfica en GeoGebra"):
        if ecuacion:
            geogebra_component(ecuacion)
        else:
            st.warning("Escribe una ecuación primero.")

    # --------- BISECCIÓN ---------
    if metodo == "Bisección":
        st.markdown("### 🔵 Bisección")
        col1, col2 = st.columns(2)
        with col1: a = st.number_input("a")
        with col2: b = st.number_input("b")
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
        col1, col2 = st.columns(2)
        with col1: x0 = st.number_input("x0")
        with col2: x1 = st.number_input("x1")
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
    metodo = st.radio("Selecciona el método", ["Derivadas", "Trapecio", "Simpson"], horizontal=True)
    st.divider()

    if metodo == "Derivadas":
        st.markdown("### 📐 Derivadas (3 y 5 puntos)")
        tabla = st.data_editor({"x": [0.0, 1.0, 2.0], "f(x)": [0.0, 0.0, 0.0]}, num_rows="dynamic")
        tipo = st.selectbox("Tipo", ["central", "derecha", "izquierda", "cinco"])
        x_eval = st.number_input("Valor de x donde evaluar")

        if st.button("🟪 Calcular"):
            x_vals = [float(x) for x in tabla["x"]]
            fx_vals = [float(f) for f in tabla["f(x)"]]
            if x_eval in x_vals:
                pos = x_vals.index(x_eval)
                resultado, estado = mt.puntos(x_vals, fx_vals, pos, tipo)
                if resultado is not None:
                    st.success(f"Resultado ≈ {resultado}")
                else:
                    st.error("No se puede calcular en esa posición")
            else:
                st.error("Ese valor no está en la tabla")

    elif metodo == "Trapecio":
        st.markdown("### 📏 Trapecio")
        tabla = st.data_editor({"x": [0.0, 1.0, 2.0], "f(x)": [0.0, 0.0, 0.0]}, num_rows="dynamic")
        if st.button("🟫 Calcular"):
            x_vals, fx_vals = tabla["x"].tolist(), tabla["f(x)"].tolist()
            st.success(f"Área ≈ {mt.trapecio_datos(x_vals, fx_vals)}")

    elif metodo == "Simpson":
        st.markdown("### 📊 Simpson")
        tabla = st.data_editor({"x": [0.0, 1.0, 2.0, 3.0], "f(x)": [0.0, 0.0, 0.0, 0.0]}, num_rows="dynamic")
        if st.button("🟧 Calcular"):
            x_vals, fx_vals = tabla["x"].tolist(), tabla["f(x)"].tolist()
            resultado, estado = mt.simpson_datos(x_vals, fx_vals)
            if resultado is not None: st.success(f"Área ≈ {resultado}")
            else: st.error("Intervalos deben ser pares")