import streamlit as st
import metodos as mt
import streamlit.components.v1 as components
import pandas as pd

# --- CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(
    page_title="Calculadora de Métodos Numéricos - UDES",
    page_icon="📊",
    layout="wide"
)

# --- ESTILOS PROFESIONALES (CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        border: 1px solid #464855;
    }
    </style>
    """, unsafe_allow_html=True)

# --- COMPONENTE GEOGEBRA ---
def generar_grafica(ecuacion):
    # Adaptación de sintaxis de Python a GeoGebra
    formula_ggb = ecuacion.replace("**", "^")
    
    html_content = f"""
    <script src="https://www.geogebra.org/apps/deployggb.js"></script>
    <div id="ggb-element" style="border: 1px solid #464855; border-radius: 8px; overflow: hidden;"></div>
    <script>
        var params = {{
            "appName": "graphing",
            "width": 800,
            "height": 450,
            "showToolBar": false,
            "showAlgebraInput": false,
            "showMenuBar": false,
            "appletOnLoad": function(api) {{
                api.evalCommand("f(x) = {formula_ggb}");
                api.setColor("f", 255, 0, 0);
                api.setThickness("f", 4);
            }}
        }};
        var applet = new GGBApplet(params, true);
        window.onload = function() {{ applet.inject('ggb-element'); }};
    </script>
    """
    components.html(html_content, height=460)

# --- NAVEGACIÓN PRINCIPAL ---
st.title("Calculadora de Métodos Numéricos")
st.sidebar.header("Módulos del Curso")
seleccion_corte = st.sidebar.radio(
    "Seleccione el periodo académico:",
    ["Primer Corte", "Segundo Corte"]
)

st.divider()

# --- LÓGICA DEL PRIMER CORTE (RAÍCES) ---
if seleccion_corte == "Primer Corte":
    st.header("Métodos para la Obtención de Raíces")
    
    col_input, col_viz = st.columns([1, 1.5], gap="medium")
    
    with col_input:
        metodo = st.selectbox("Algoritmo de resolución:", ["Bisección", "Newton", "Secante"])
        ecuacion = st.text_input("Función f(x):", placeholder="Ej: x**2 - 4")
        
        # Parámetros según el método seleccionado
        if metodo == "Bisección":
            c1, c2 = st.columns(2)
            a_val = c1.number_input("Límite inferior (a)", value=0.0)
            b_val = c2.number_input("Límite superior (b)", value=1.0)
        elif metodo == "Newton":
            x0_val = st.number_input("Aproximación inicial (x0)", value=1.0)
        elif metodo == "Secante":
            c1, c2 = st.columns(2)
            x0_val = c1.number_input("x0", value=0.0)
            x1_val = c2.number_input("x1", value=1.0)
            
        tolerancia = st.number_input("Tolerancia", value=0.0001, format="%.6f")
        
        if st.button("Ejecutar Cálculo"):
            if ecuacion:
                try:
                    expr, var_x = mt.preparar_ecuacion(ecuacion)
                    
                    if metodo == "Bisección":
                        res, it = mt.biseccion(expr, var_x, a_val, b_val, tolerancia)
                    elif metodo == "Newton":
                        res, it = mt.newton(expr, var_x, x0_val, tolerancia)
                    else:
                        res, it = mt.secante(expr, var_x, x0_val, x1_val, tolerancia)
                    
                    if res is not None:
                        st.subheader("Resultados")
                        st.metric("Raíz Aproximada", f"{res:.8f}")
                        st.metric("Iteraciones Realizadas", it)
                    else:
                        st.error("El método no convergió o el intervalo es inválido.")
                except Exception as error:
                    st.error(f"Error en la expresión matemática: {error}")

    with col_viz:
        st.subheader("Representación Gráfica")
        if ecuacion:
            generar_grafica(ecuacion)
        else:
            st.info("Ingrese una función para visualizar la gráfica.")

# --- LÓGICA DEL SEGUNDO CORTE (DATOS) ---
elif seleccion_corte == "Segundo Corte":
    st.header("Análisis Numérico Basado en Datos")
    
    tab_der, tab_int = st.tabs(["Diferenciación Numérica", "Integración Numérica"])
    
    with tab_der:
        st.subheader("Métodos de 3 y 5 Puntos")
        df_der = st.data_editor(
            {"x": [0.0, 0.2, 0.4, 0.6, 0.8], "f(x)": [1.0, 1.22, 1.49, 1.82, 2.22]},
            num_rows="dynamic",
            key="editor_derivadas"
        )
        
        col_opts = st.columns(2)
        tipo_der = col_opts[0].selectbox("Esquema de derivación:", ["central", "derecha", "izquierda", "cinco"])
        x_target = col_opts[1].number_input("Valor de x a evaluar:", value=0.0)
        
        if st.button("Calcular Derivada"):
            x_list = [float(val) for val in df_der["x"]]
            fx_list = [float(val) for val in df_der["f(x)"]]
            
            if x_target in x_list:
                idx = x_list.index(x_target)
                resultado, cod_error = mt.puntos(x_list, fx_list, idx, tipo_der)
                if resultado is not None:
                    st.metric("f'(x) Resultante", f"{resultado:.6f}")
                else:
                    st.error(f"Error de límites para el esquema seleccionado (Código: {cod_error})")
            else:
                st.error("El valor de x no se encuentra en la tabla proporcionada.")

    with tab_int:
        st.subheader("Integración por Trapecio y Simpson")
        df_int = st.data_editor(
            {"x": [0.0, 1.0, 2.0, 3.0, 4.0], "f(x)": [0.0, 1.0, 4.0, 9.0, 16.0]},
            num_rows="dynamic",
            key="editor_integracion"
        )
        
        col_btns = st.columns(2)
        
        if col_btns[0].button("Integrar por Trapecio"):
            x_list = [float(val) for val in df_int["x"]]
            fx_list = [float(val) for val in df_int["f(x)"]]
            res_trap = mt.trapecio_datos(x_list, fx_list)
            st.metric("Área Estimada (Trapecio)", f"{res_trap:.6f}")
            
        if col_btns[1].button("Integrar por Simpson"):
            x_list = [float(val) for val in df_int["x"]]
            fx_list = [float(val) for val in df_int["f(x)"]]
            res_simp, cod_error = mt.simpson_datos(x_list, fx_list)
            if res_simp is not None:
                st.metric("Área Estimada (Simpson)", f"{res_simp:.6f}")
            else:
                st.error("Error: El método de Simpson requiere un número par de intervalos.")