import streamlit as st
import metodos as m
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# --- CONFIGURACIÓN ESTÉTICA ---
st.set_page_config(page_title="UDES Computational Physics", layout="wide")

st.markdown("""
    <style>
    body { background-color: #050505; color: #e0e0e0; }
    .stApp { background: radial-gradient(circle at top right, #1a1a2e, #050505); }
    .card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
    }
    h1 { font-weight: 800; letter-spacing: -2px; color: #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
with st.sidebar:
    st.title("AFCC-Q Labs")
    st.info("Ingeniería de IA y Computación")
    seccion = st.radio("Módulo del Curso", ["Dashboard", "Corte 1: Raíces", "Corte 2: Derivación/Integración"])
    st.markdown("---")
    st.caption("Cada error es la lección que me entrena para el siguiente golpe.")

# --- DASHBOARD ---
if seccion == "Dashboard":
    st.title("⚛️ Física Computacional")
    st.write("Bienvenido, Andrés. Selecciona un módulo para procesar ecuaciones o datos experimentales.")
    
# --- CORTE 1 ---
elif seccion == "Corte 1: Raíces":
    st.title("🎯 Búsqueda de Raíces")
    
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            eq = st.text_input("Ecuación", "x^2 - 4")
            met = st.selectbox("Método", ["Bisección", "Newton", "Secante"])
            tol = st.number_input("Tolerancia", value=1e-5, format="%.5f")
            
            if met == "Bisección":
                a = st.number_input("Intervalo a", value=0.0)
                b = st.number_input("Intervalo b", value=3.0)
            elif met == "Newton":
                x0 = st.number_input("Punto inicial x0", value=1.0)
            else:
                x0 = st.number_input("x0", value=1.0)
                x1 = st.number_input("x1", value=2.0)
            
            if st.button("Ejecutar Algoritmo"):
                try:
                    expr, x_sym = m.preparar_ecuacion(eq)
                    if met == "Bisección": res, it = m.biseccion(expr, x_sym, a, b, tol)
                    elif met == "Newton": res, it = m.newton(expr, x_sym, x0, tol)
                    else: res, it = m.secante(expr, x_sym, x0, x1, tol)
                    
                    if res is not None:
                        st.success(f"Raíz encontrada: {res:.6f}")
                        st.metric("Convergencia en", f"{it} iteraciones")
                        
                        # Gráfica Abstracta
                        f_n = sp.lambdify(x_sym, expr, 'numpy')
                        x_v = np.linspace(float(res)-2, float(res)+2, 200)
                        y_v = f_n(x_v)
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=x_v, y=y_v, line=dict(color='#00f2ff', width=3), name="f(x)"))
                        fig.add_trace(go.Scatter(x=[res], y=[0], mode='markers', marker=dict(size=15, color='red', symbol='x')))
                        fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- CORTE 2 ---
elif seccion == "Corte 2: Derivación/Integración":
    st.title("📏 Cálculo Numérico")
    
    t1, t2 = st.tabs(["Diferenciación", "Integración"])
    
    with t1:
        st.write("Cálculo de derivadas por puntos")
        x_in = st.text_input("Valores de X", "0, 0.5, 1.0, 1.5, 2.0")
        y_in = st.text_input("Valores de f(X)", "1, 1.64, 2.71, 4.48, 7.38")
        idx = st.number_input("Posición de la lista", value=0, step=1)
        tipo = st.radio("Esquema", ["central", "derecha", "izquierda", "5 puntos"], horizontal=True)
        
        if st.button("Calcular Derivada"):
            lx = [float(i) for i in x_in.split(",")]
            ly = [float(i) for i in y_in.split(",")]
            resultado, error_code = m.puntos(lx, ly, idx, tipo)
            if resultado is not None:
                st.subheader(f"Resultado: {resultado:.6f}")
            else:
                st.warning(f"Fuera de rango (Código error: {error_code})")

    with t2:
        st.write("Cálculo de área bajo la curva")
        col_a, col_b = st.columns(2)
        lx = [float(i) for i in x_in.split(",")]
        ly = [float(i) for i in y_in.split(",")]
        
        if col_a.button("Trapecio"):
            area = m.trapecio_datos(lx, ly)
            st.metric("Área Estimada", f"{area:.6f}")
        
        if col_b.button("Simpson"):
            area, err = m.simpson_datos(lx, ly)
            if area: st.metric("Área Estimada", f"{area:.6f}")
            else: st.error("Se requiere un número par de intervalos.")