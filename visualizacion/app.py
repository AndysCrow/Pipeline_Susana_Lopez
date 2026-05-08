import streamlit as st
import os
import sys


# ──────────────────────────────────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────────────────────────────────
dir_file = os.path.dirname(os.path.abspath(__file__))
root_file = os.path.dirname(dir_file)
sys.path.append(root_file)

from trazabilidad.dataframe import LogTrazabilidad
from ui_archivos import cargar_archivo
from ui_pipeline import ejecutar_pipeline
from ui_resultados import mostrar_resultados


# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pipeline de Limpieza — Hospital Susana López de Valencia",
    page_icon="assets/logo_pag.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ──────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ─────────────────────────────────────────────────────────────
   GLOBAL
───────────────────────────────────────────────────────────── */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F4F6F4;
    color: #1F2937;
}

/* Ocultar Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Contenedor principal */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* ─────────────────────────────────────────────────────────────
   TIPOGRAFÍA
───────────────────────────────────────────────────────────── */

h1 {
    color: #29235C !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}

h2, h3 {
    color: #29235C !important;
    font-weight: 700 !important;
}

h4, h5, h6 {
    color: #327531 !important;
    font-weight: 600 !important;
}

p, span, label {
    color: #374151;
}

/* ─────────────────────────────────────────────────────────────
   HEADER
───────────────────────────────────────────────────────────── */

.header-container {
    background: #76B82A;
    border: 1px solid #D1D5DB;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}

.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ─────────────────────────────────────────────────────────────
   CARDS
───────────────────────────────────────────────────────────── */

.card {
    background: #76B82A;
    border: 1px solid #D1D5DB;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* ─────────────────────────────────────────────────────────────
   BOTONES
───────────────────────────────────────────────────────────── */

.stButton > button {
    width: 100%;
    background: #327531;
    color: white;
    border: none;
    padding: 0.85rem 1rem;
    font-weight: 700;
    font-size: 15px;
    transition: 0.15s ease;
    box-shadow: none;
}

.stButton > button:hover {
    background: #76B82A;
    color: white;
}

/* ─────────────────────────────────────────────────────────────
   FILE UPLOADER
───────────────────────────────────────────────────────────── */

[data-testid="stFileUploader"] {
    border: 2px dashed #76B82A;
    background: #FAFCF7;
    padding: 1rem;
}


[data-testid="stFileUploaderDropzone"] {
    background-color: #76B82A !important;
    color: #1F2937 !important; 
}

[data-testid="stFileUploader"] section {
    padding: 1rem;
}
            

/* ─────────────────────────────────────────────────────────────
   ALERTAS
───────────────────────────────────────────────────────────── */

.stAlert {
    border-radius: 0px;
    border: 1px solid #D1D5DB;
    box-shadow: none;
}

/* ─────────────────────────────────────────────────────────────
   MÉTRICAS
───────────────────────────────────────────────────────────── */

[data-testid="metric-container"] {
    background: white;
    border: 1px solid #D1D5DB;
    padding: 1rem;
    box-shadow: none;
}

/* ─────────────────────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────────────────────── */

[data-testid="stSidebar"] {
    background: #29235C;
}

/* ─────────────────────────────────────────────────────────────
   DIVISORES
───────────────────────────────────────────────────────────── */

hr {
    border-color: #D1D5DB;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* ─────────────────────────────────────────────────────────────
   TABS
───────────────────────────────────────────────────────────── */

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border: 1px solid #D1D5DB;
    padding: 10px 18px;
}

/* ─────────────────────────────────────────────────────────────
   SCROLLBAR
───────────────────────────────────────────────────────────── */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #BFC7BF;
}

::-webkit-scrollbar-thumb:hover {
    background: #9FA89F;
}

</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="header-container">', unsafe_allow_html=True)

col_logo, col_titulo, col_info = st.columns([2, 4, 2])

# ── LOGO ─────────────────────────────────────────────────────────────────────
with col_logo:
    st.markdown(
        "<div style='text-align:center'>",
        unsafe_allow_html=True
    )
    st.image("assets/logo.png", width=250)
    st.markdown("</div>", unsafe_allow_html=True)

# ── UNIVERSIDAD ─────────────────────────────────────────────────────────────


# ── TITULO ───────────────────────────────────────────────────────────────────
with col_titulo:

    st.markdown("###### HOSPITAL SUSANA LÓPEZ DE VALENCIA · E.S.E")

    st.title("Pipeline de Limpieza de Morbilidad")

    st.markdown("""
    <span style="
        color:#6B7280;
        font-size:15px;
    ">
    Procesamiento automatizado de base de datos para analisis de morbilidad.
    </span>
    """, unsafe_allow_html=True)


# ── INFO ─────────────────────────────────────────────────────────────────────
with col_info:
    st.markdown(
        "<div style='text-align:center'>",
        unsafe_allow_html=True
    )
    st.image("assets/logo_uni.png", width=300)
    st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# MÉTRICAS SUPERIORES
# ──────────────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
col_izq, col_der = st.columns([1, 1.8], gap="large")


# ──────────────────────────────────────────────────────────────────────────────
# PANEL IZQUIERDO
# ──────────────────────────────────────────────────────────────────────────────
with col_izq:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📂 Carga de archivo")

    st.markdown("""
    <span style="color:#6B7280; font-size:14px;">
    Seleccione el archivo institucional que será procesado por el pipeline.
    </span>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    ruta_archivo = cargar_archivo()

    if ruta_archivo is not None:

        st.success("Archivo cargado correctamente.")

        log = LogTrazabilidad()

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("⚙️ Ejecución")

        st.markdown("""
        <span style="color:#6B7280; font-size:14px;">
        Inicie el procesamiento automatizado de registros clínicos.
        </span>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        

        if st.button(
            "▶ Procesar archivo",
            type="primary",
            use_container_width=True
        ):
            ejecutar_pipeline(ruta_archivo, log)

    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# PANEL DERECHO
# ──────────────────────────────────────────────────────────────────────────────
with col_der:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Resultados")

    st.markdown("""
    <span style="color:#6B7280; font-size:14px;">
    Resultados generados durante el procesamiento institucional.
    </span>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    mostrar_resultados()

    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)


st.html(
    """
    <div style="text-align: center; font-family: sans-serif; margin-top: 50px; backgorund-color: #F4F6F4; padding: 20px; border-top: 1px solid #D1D5DB;">
        <p style="color: #555; font-size: 14px; margin-bottom: 5px;">
            © 2026 - Hospital Susana López de Valencia E.S.E.
        </p>
        <p style="color: #888; font-size: 14px; margin-top: 0;">
            Powered by Ingeniería de sistemas - Corporación Universitaria Comfacauca
        </p>
    </div>
    """
)