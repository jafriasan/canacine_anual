# Código que genera la portada de un dashboard con estadística de taquilla en México.

import streamlit as st

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
st.set_page_config(page_title="CANACINE Dashboard", layout="wide")

# =====================================================
# IMPORTA TUS DASHBOARDS
# =====================================================
from series_de_tiempo_anual import dashboard_series_tiempo
from datos_cruzados_anual import dashboard_datos_cruzados

# 👇 NUEVOS DASHBOARDS (CINES)
from series_de_tiempo_anual_cines import dashboard_series_tiempo_cines
from datos_cruzados_anual_cines import dashboard_datos_cruzados_cines

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
            color: #4C7DFF;
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

    # -----------------------------
    # BOTONES
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "📈 Títulos: Series de tiempo",
            use_container_width=True,
            on_click=go_to,
            args=("series",)
        )
        
        # 👇 TEXTO DEBAJO DEL BOTÓN
        st.markdown("""
                    <p style="font-size:14px; color:gray;">
                    Se presenta estadística anual del número de títulos exhibidos en México y la taquilla asociada, 
                    tanto en ingresos como en boletos vendidos. Estos datos para las dimensiones (filtros) de país 
                    de origen (México y el resto), país primario y no primario, género primario, clasificación, distribuidor, rango de semanas en cartelera,
                    rango de cines, y también se distigue entre el total de títulos y los estrenos. La información se presenta
                    en gráficas de series de tiempo, para el periodo del año 2000 a la fecha. 
                    </p>
                    """, unsafe_allow_html=True)

        st.button(
            "🎬 Cines: Series de tiempo",
            use_container_width=True,
            on_click=go_to,
            args=("cines_series",)
        )
        
        st.markdown("""
                    <p style="font-size:14px; color:gray;">
                    Se presenta estadística anual del número de cines/pantallas en México y la taquilla asociada, 
                    tanto en ingresos como en boletos vendidos. Estos datos para las dimensiones (filtros) de circuito de exhibición,
                    región, entidad federativa, ciudad, rango de títulos exhibidos y rango de pantallas. La información se presentan
                    en gráficas de series de tiempo, para el periodo del año 2000 a la fecha. 
                    </p>
                    """, unsafe_allow_html=True)

    with col2:
        st.button(
            "📊 Títulos: Datos cruzados",
            use_container_width=True,
            on_click=go_to,
            args=("cruzados",)
        )
        
        st.markdown("""
                    <p style="font-size:14px; color:gray;">
                    Se presenta estadística anual del número de títulos exhibidos en México y la taquilla asociada, 
                    tanto en ingresos como en boletos vendidos. Estos datos para los filtros de año(s), país 
                    de origen (México y el resto), y también se distigue entre el total de títulos y los estrenos. La información
                    se presenta en gráficas de datos cruzados para los filtros seleccionados y para las dimensiones de
                    país primario y no primario, género primario, clasificación, distribuidora, rango de semanas en cartelera y rango de cines.  
                    </p>
                    """, unsafe_allow_html=True)

        st.button(
            "🔗 Cines: Datos cruzados",
            use_container_width=True,
            on_click=go_to,
            args=("cines_cruzados",)
        )
        
        st.markdown("""
                    <p style="font-size:14px; color:gray;">
                    Se presenta estadística anual del número de cines/pantallas en México y la taquilla asociada, 
                    tanto en ingresos como en boletos vendidos. Estos datos para los filtros de año(s), entidad(es) federativa(s) y ciudad(es).
                    La información se presenta en gráficas de datos cruzados para los filtros seleccionados
                    y las dimensiones de circuito de exhibición, rango de títulos exhibidos, rango de pantallas y región.
                    Las dimensiones de entidad federativa y ciudad se presentan en formato de mapa.
                    </p>
                    """, unsafe_allow_html=True)

# =====================================================
# DASHBOARD 1 - SERIES DE TIEMPO (TÍTULOS)
# =====================================================
elif st.session_state.page == "series":

    st.markdown("<h1>🎬 Reporte de Taquilla en México</h1>", unsafe_allow_html=True)

    st.button("⬅ Volver", on_click=go_to, args=("home",))
    st.markdown("---")

    dashboard_series_tiempo()
    

# =====================================================
# DASHBOARD 2 - DATOS CRUZADOS (TÍTULOS)
# =====================================================
elif st.session_state.page == "cruzados":

    st.markdown("<h1>🎬 Reporte de Taquilla en México</h1>", unsafe_allow_html=True)

    st.button("⬅ Volver", on_click=go_to, args=("home",))
    st.markdown("---")

    dashboard_datos_cruzados()

# =====================================================
# 🎬 DASHBOARD 3 - CINES SERIES DE TIEMPO
# =====================================================
elif st.session_state.page == "cines_series":

    st.markdown("<h1>🎬 Cines: Series de tiempo</h1>", unsafe_allow_html=True)

    st.button("⬅ Volver", on_click=go_to, args=("home",))
    st.markdown("---")

    dashboard_series_tiempo_cines()

# =====================================================
# 🔗 DASHBOARD 4 - CINES DATOS CRUZADOS
# =====================================================
elif st.session_state.page == "cines_cruzados":

    st.markdown("<h1>🔗 Cines: Datos cruzados</h1>", unsafe_allow_html=True)

    st.button("⬅ Volver", on_click=go_to, args=("home",))
    st.markdown("---")

    dashboard_datos_cruzados_cines()
    
#streamlit run /Users/judith_frias/Comscore_data/Daily_report_comscore/Proyecto_Comscore/dashboard_anual_intento_1.py
