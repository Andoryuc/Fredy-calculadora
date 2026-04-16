import streamlit as st
import metodos as mt
import streamlit.components.v1 as components
import pandas as pd

# --- CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="UDES | COMPUTATIONAL ENGINE",
    page_icon="🎮",
    layout="wide"
)

# --- CSS GAMING MODE (NEON & GLOW) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');

    /* Fondo Base */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d0d1a 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* Títulos estilo Gaming */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
    }

    /* Barra Lateral Estilizada */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.95);
        border-right: 2px solid #7000ff;
    }

    /* Tarjetas de Resultado (HUD Style) */
    .result-box {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: inset 0 0 15px rgba(0, 242, 255, 0.2), 0 0 20px rgba(0, 0, 0, 0.5);
        margin: 15px 0;
    }

    /* Botones con Efecto RGB */
    .stButton>button {
        background: linear-gradient(90deg, #7000ff, #00f2ff);
        color: white !important;
        border: none !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border-radius: 5px;
        transition: 0.3s all;
        text-shadow: 1px 1px 2px black;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.8);
    }

    /* Data Editor / Tablas */
    div[data-testid="stTable"] {
        background-color: #111;
        border: 1px solid #7000ff;
    }

    /* Input Fields */
    input {
        background-color: #1a1a2e !important;
        border: 1px solid #7000ff !important;
        color: #00f2ff !important;
        font-family: 'JetBrains Mono', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- COMPONENTE GEOGEBRA GAMING ---
def draw_geogebra(ecuacion):
    formula = ecuacion.replace("**", "^")
    html = f"""
    <div style="border: 2px solid #7000ff; border-radius: 15px; overflow: hidden; box-shadow: 0 0 30px rgba(112, 0, 255, 0.3);">
        <script src="https://www.geogebra.org/apps/deployggb.js"></script>
        <div id="ggb-element"></div>
        <script>
            var params = {{
                "appName": "graphing", "width": 800, "height": 500,
                "showToolBar": false, "showAlgebraInput": false,
                "showMenuBar": false,
                "appletOnLoad": function(api) {{
                    api.evalCommand("f(x) = {formula}");
                    api.setColor("f", 0, 0, 255);
                    api.setThickness("f", 5);
                    api.setGridVisible(true);
                }}
            }};
            var applet = new GGBApplet(params, true);
            window.onload = function() {{ applet.inject('ggb-element'); }};
        </script>
    </div>
    """
    components.html(html, height=520)

# --- NAVEGACIÓN (CORREGIDA) ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 1.2rem;'>System Modules</h2>", unsafe_allow_html=True)
    corte_actual = st.radio("SELECT PHASE:", ["PHASE 01: RAÍCES", "PHASE 02: DATOS"])
    st.divider()
    st.caption("ENGINE STATUS: ONLINE")

# --- LÓGICA DE INTERFAZ ---
if corte_actual == "PHASE 01: RAÍCES":
    st.title("🎯 Root Analysis System")
    
    col_input, col_graph = st.columns([1, 1.5], gap="large")
    
    with col_input:
        with st.container():
            st.markdown("### Config")
            metodo = st.selectbox("Algoritmo:", ["Bisección", "Newton", "Secante"])
            ecuacion = st.text_input("Function f(x):", "x**2 - 2")
            
            if metodo == "Bisección":
                c1, c2 = st.columns(2)
                a = c1.number_input("Limit A", value=0.0)
                b = c2.number_input("Limit B", value=2.0)
            elif metodo == "Newton":
                x0 = st.number_input("Start X0", value=1.0)
            else:
                c1, c2 = st.columns(2)
                x0 = c1.number_input("X0", value=0.0)
                x1 = c2.number_input("X1", value=1.0)
                
            tol = st.number_input("Tolerance", value=0.0000000000001, format="%.6f")
            
            if st.button("RUN CALCULATION"):
                try:
                    expr, var_x = mt.preparar_ecuacion(ecuacion)
                    if metodo == "Bisección": res, it = mt.biseccion(expr, var_x, a, b, tol)
                    elif metodo == "Newton": res, it = mt.newton(expr, var_x, x0, tol)
                    else: res, it = mt.secante(expr, var_x, x0, x1, tol)
                    
                    if res is not None:
                        st.markdown(f"""
                            <div class="result-box">
                                <p style="color:#00f2ff; font-family:'Orbitron';">RESULTADO DETECTADO:</p>
                                <h2 style="margin:0; color:#fff;">x = {res:.8f}</h2>
                                <p style="color:#7000ff; font-family:'JetBrains Mono'; margin-top:10px;">ITERACIONES: {it}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("SYSTEM ERROR: Divergencia detectada.")
                except Exception as e:
                    st.error(f"Sintaxis inválida: {e}")

    with col_graph:
        st.subheader("Visual Spectrum")
        if ecuacion:
            draw_geogebra(ecuacion)

elif corte_actual == "PHASE 02: DATOS":
    st.title("📊 Numerical Data Processing")
    
    tab_der, tab_int = st.tabs(["[ DERIVACIÓN ]", "[ INTEGRACIÓN ]"])
    
    with tab_der:
        st.markdown("### Data Input Matrix")
        df_der = st.data_editor(
            {"x": [0.0, 0.1, 0.2, 0.3], "f(x)": [1.0, 1.1, 1.3, 1.6]},
            num_rows="dynamic"
        )
        col_s1, col_s2 = st.columns(2)
        tipo = col_s1.selectbox("Scheme:", ["central", "derecha", "izquierda", "cinco"])
        target = col_s2.number_input("Eval X:", value=0.0)
        
        if st.button("EXECUTE DERIVATIVE"):
            xl, fl = list(df_der["x"]), list(df_der["f(x)"])
            if target in xl:
                res, err = mt.puntos(xl, fl, xl.index(target), tipo)
                if res is not None:
                    st.markdown(f'<div class="result-box">f\'({target}) = {res:.6f}</div>', unsafe_allow_html=True)
                else: st.error(f"Error Code: {err}")
            else: st.error("Target X not in matrix.")

    with tab_int:
        st.markdown("### Area Integration")
        df_int = st.data_editor(
            {"x": [0.0, 1.0, 2.0], "f(x)": [0.0, 1.0, 4.0]},
            num_rows="dynamic", key="int_edit"
        )
        c1, c2 = st.columns(2)
        if c1.button("TRAPEZOIDAL RULE"):
            res = mt.trapecio_datos(list(df_int["x"]), list(df_int["f(x)"]))
            st.info(f"Área: {res:.6f}")
        if c2.button("SIMPSON RULE"):
            res, err = mt.simpson_datos(list(df_int["x"]), list(df_int["f(x)"]))
            if res: st.info(f"Área: {res:.6f}")
            else: st.error("Simpson requiere intervalos pares.")