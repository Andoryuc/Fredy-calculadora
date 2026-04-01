import streamlit as st
import metodos as mt
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(
    page_title="AFCC-Q | Computational Engine",
    page_icon="⚛️",
    layout="wide", # Cambiamos a wide para mejor aprovechamiento del espacio
    initial_sidebar_state="expanded"
)

# --- 2. INYECCIÓN DE CSS "MEGA PRO" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@300;500&display=swap');

    /* Variables de Color */
    :root {
        --primary-cyan: #00f2ff;
        --secondary-purple: #7000ff;
        --bg-dark: #0a0a0c;
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    /* Fondo y Tipografía */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #0a0a0c 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Estilo de la Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
    }

    /* Títulos y Subtítulos */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(90deg, #fff, #555);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Cards de Resultados (Glassmorphism) */
    .result-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-top: 20px;
        border-left: 5px solid var(--primary-cyan);
    }

    /* Botones Personalizados */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid var(--glass-border);
        background: linear-gradient(135deg, rgba(0,242,255,0.1) 0%, rgba(112,0,255,0.1) 100%);
        color: white;
        font-weight: 600;
        padding: 15px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        border-color: var(--primary-cyan);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
        transform: translateY(-2px);
    }

    /* Inputs Estilizados */
    .stTextInput>div>div>input, .stNumberInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    /* Logo AFCC-Q */
    .brand {
        font-family: 'JetBrains Mono', monospace;
        color: var(--primary-cyan);
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. COMPONENTE GEOGEBRA MEJORADO ---
def geogebra_pro(ecuacion, color_hex="0, 242, 255"):
    ggb_ecuacion = ecuacion.replace("**", "^")
    # Convertir RGB para JS
    html_code = f"""
    <script src="https://www.geogebra.org/apps/deployggb.js"></script>
    <div id="ggb-element" style="border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);"></div>
    <script>
        var params = {{
            "appName": "graphing", "width": 800, "height": 450,
            "showToolBar": false, "showAlgebraInput": false,
            "showMenuBar": false, "enableRightClick": false,
            "appletOnLoad": function(api) {{
                api.evalCommand("f(x) = {ggb_ecuacion}");
                api.setColor("f", {color_hex});
                api.setThickness("f", 6);
                api.setGridVisible(true);
            }}
        }};
        var applet = new GGBApplet(params, true);
        window.onload = function() {{ applet.inject('ggb-element'); }};
    </script>
    """
    components.html(html_code, height=470)

# --- 4. BARRA LATERAL (BRANDING) ---
with st.sidebar:
    st.markdown('<div class="brand">SYSTEM: AFCC-Q // UNIT: UDES</div>', unsafe_allow_html=True)
    st.title("Control Panel")
    corte = st.selectbox("Módulo de Ingeniería", ["Corte I: Raíces", "Corte II: Datos"], index=0)
    st.divider()
    st.markdown("> *Cada error es la lección que me entrena para el siguiente golpe.*")

# --- 5. LÓGICA PRINCIPAL ---

if "Corte I" in corte:
    st.title("🎯 Root Finding Engine")
    
    col_input, col_graph = st.columns([1, 1.5], gap="large")
    
    with col_input:
        st.subheader("Configuración")
        metodo = st.selectbox("Algoritmo", ["Bisección", "Newton", "Secante"])
        ecuacion = st.text_input("Función Objetivo f(x)", "x**2 - 4", help="Usa x**2 para potencias")
        
        # Colores dinámicos según método
        colors = {"Bisección": "0, 242, 255", "Newton": "112, 0, 255", "Secante": "255, 49, 49"}
        current_color = colors.get(metodo)

        with st.expander("Parámetros del Método", expanded=True):
            if metodo == "Bisección":
                c1, c2 = st.columns(2)
                a = c1.number_input("Límite a", value=0.0)
                b = c2.number_input("Límite b", value=3.0)
            elif metodo == "Newton":
                x0 = st.number_input("Aproximación x0", value=1.0)
            else:
                c1, c2 = st.columns(2)
                x0 = c1.number_input("x0", value=1.0)
                x1 = c2.number_input("x1", value=2.0)
            
            tol = st.number_input("Tolerancia (ε)", value=0.0001, format="%.5f")

        if st.button("🚀 Ejecutar Análisis"):
            if ecuacion:
                try:
                    expresion, x_sym = mt.preparar_ecuacion(ecuacion)
                    if metodo == "Bisección": 
                        raiz, it = mt.biseccion(expresion, x_sym, a, b, tol)
                    elif metodo == "Newton": 
                        raiz, it = mt.newton(expresion, x_sym, x0, tol)
                    else: 
                        raiz, it = mt.secante(expresion, x_sym, x0, x1, tol)

                    if raiz is not None:
                        st.markdown(f"""
                        <div class="result-card">
                            <h3 style="margin:0; color:#fff;">Resultado Encontrado</h3>
                            <p style="font-size:1.5rem; color:var(--primary-cyan); font-weight:bold; margin:10px 0;">x ≈ {raiz:.8f}</p>
                            <p style="font-family:'JetBrains Mono'; font-size:0.8rem; color:#888;">CONVERGENCIA: {it} ITERACIONES</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Error: El método no convergió en el intervalo.")
                except Exception as e:
                    st.error(f"Error de Sintaxis: {e}")

    with col_graph:
        st.subheader("Visualización en Tiempo Real")
        if ecuacion:
            geogebra_pro(ecuacion, current_color)
        else:
            st.info("Esperando definición de función...")

elif "Corte II" in corte:
    st.title("📊 Numerical Data Analysis")
    
    metodo = st.tabs(["Diferenciación", "Integración (Trapecio)", "Integración (Simpson)"])
    
    # Aquí puedes replicar el estilo de columnas y result-cards para el segundo corte
    with metodo[0]:
        st.subheader("Derivación por Puntos")
        # ... (Tu lógica de tabla del segundo corte aquí)