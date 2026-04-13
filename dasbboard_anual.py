# Código que genera carátula del dashboard de Canacina con estadísticas de taquilla en México
# Actualmente sólo se incorpora estadística anual, que se complemnetará con secciones adicioales de estadística semanal y de fin de semana

import streamlit as st

# =====================================================
# CONFIGURACIÓN GENERAL (SIEMPRE PRIMERO)
# =====================================================
st.set_page_config(page_title="CANACINE Dashboard", layout="wide")

# =====================================================
# IMPORTA TUS DASHBOARDS
# =====================================================
from series_de_tiempo_anual import dashboard_series_tiempo
from datos_cruzados_anual import dashboard_datos_cruzados

# =====================================================
# ESTADO DE NAVEGACIÓN
# =====================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page

# =====================================================
# HOME / PORTADA
# =====================================================
if st.session_state.page == "home":

    st.markdown("""
        <style>
        .title {
            text-align: center;
            font-size: 70px;
            font-weight: 800;
            margin-top: 80px;
            color: #4C7DFF;  /* azul rey claro */
        }

        .subtitle {
            text-align: center;
            font-size: 22px;
            color: gray;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>CANACINE</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Estadísticas de taquilla en México</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "📈 Series de tiempo",
            use_container_width=True,
            on_click=go_to,
            args=("series",)
        )

    with col2:
        st.button(
            "📊 Datos cruzados",
            use_container_width=True,
            on_click=go_to,
            args=("cruzados",)
        )

# =====================================================
# DASHBOARD 1 - SERIES DE TIEMPO
# =====================================================
elif st.session_state.page == "series":

    st.markdown(
        "<h1 style='color:white;'>🎬 Reporte de Taquilla en México</h1>",
        unsafe_allow_html=True
    )

    st.button("⬅ Volver", on_click=go_to, args=("home",))

    st.markdown("---")

    dashboard_series_tiempo()

# =====================================================
# DASHBOARD 2 - DATOS CRUZADOS
# =====================================================
elif st.session_state.page == "cruzados":

    st.markdown(
        "<h1 style='color:white;'>🎬 Reporte de Taquilla en México</h1>",
        unsafe_allow_html=True
    )

    st.button("⬅ Volver", on_click=go_to, args=("home",))

    st.markdown("---")

    dashboard_datos_cruzados()
    
#streamlit run /Users/judith_frias/Comscore_data/Daily_report_comscore/Proyecto_Comscore/dashboard_anual.py
