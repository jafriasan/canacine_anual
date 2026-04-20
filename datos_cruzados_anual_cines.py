# Crea la sección de datos cruzados con estadística de Cines. Esta sección forma parte de un dashboard de taquilla en México

import streamlit as st
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go


def dashboard_datos_cruzados_cines():

    st.title("📈 Datos cruzados")
    
    # -----------------------------
    # CARGA DE DATOS
    # -----------------------------
    archivo = "cubo_cines_2000_2025.xlsx"

    @st.cache_data
    def load_data():
        return pd.read_excel(archivo, keep_default_na=False)

    df_base = load_data()

    # -----------------------------
    # VALORES POR DEFECTO
    # -----------------------------
    ultimo_anio = df_base["year"].max()

    # -----------------------------
    # MÉTRICAS Y FILTROS
    # -----------------------------
        
    metrica = st.sidebar.selectbox(
            "Métricas",
            ["Taquilla_ingresos", "Taquilla_boletos","Cines","Pantallas"],
            index=0
    )
    #st.markdown("### ⚙️ Filtros")
        
    st.sidebar.header("Filtros")

    anios = st.sidebar.multiselect(
            "Año(s)",
            sorted(df_base["year"].dropna().unique()),
            default=[ultimo_anio]
    )

    # primero filtra estados
    estados = st.sidebar.multiselect(
        "Entidad(es) federativa(s)",
        sorted(df_base["estado_f"].dropna().unique()),
        default=None
    )

    # filtra dataset intermedio
    df_temp = df_base.copy()

    if estados:
        df_temp = df_temp[df_temp["estado_f"].isin(estados)]

    # ahora ciudades DEPENDEN de estados
    ciudades = st.sidebar.multiselect(
        "Ciudad(es)",
        sorted(df_temp["ciudad_f"].dropna().unique()),
        default=None
    )

    # NOTA AGREGADA JUSTO DEBAJO DEL FILTRO
    st.sidebar.markdown(
        "<p style='font-size:11px; color:gray;'>"
        "Fuente: Comscore."
        "</p>",
    unsafe_allow_html=True
    )

    mapa_rango_tit = {
            "T01": "1-25 Títulos",
            "T02": "26-50 Títulos",
            "T03": "51-75 Títulos",
            "T04": "76-100 Títulos",
            "T05": "101-125 Títulos",
            "T06": "126-150 Títulos",
            "T07": "151-175 Títulos",
            "T08": "176-200 Títulos",
            "T09": "201-225 Títulos",
            "T10": "226-250 Títulos",
            "T11": "251-275 Títulos",
            "T12": "276-300 Títulos",
            "T13": "301-325 Títulos",
            "T14": "326-350 Títulos",
            "T15": "351-375 Títulos",
            "T16": "375-400 Títulos",
            "T17": "> 400 Títulos"
    }
        
        
    #orden_rango_tit = [f"T{str(i).zfill(2)}" for i in range(1,18)]    

    mapa_rango_pan = {
            "P01": "1 Pantalla",
            "P02": "2 Pantallas",
            "P03": "3 Pantallas",
            "P04": "4 Pantallas",
            "P05": "5 Pantallas",
            "P06": "6-10 Pantallas",
            "P07": "11-15 Pantallas",
            "P08": "> 15 Pantallas"
    }
        
        
    #orden_rango_pan = [f"P{str(i).zfill(2)}" for i in range(1,18)]  

    # -----------------------------
    # APLICAR FILTROS
    # -----------------------------
    df = df_base.copy()

    if anios:
            df = df[df["year"].isin(anios)]
            
    if estados:
        df = df[df["estado_f"].isin(estados)]
        
    if ciudades:
        df = df[df["ciudad_f"].isin(ciudades)]

    # =====================================================
    # DASHBOARD
    # =====================================================
    def generar_dashboard(variable, titulo, df_filtrado):

            # -------------------------
            # KPI
            # -------------------------
            total_metric = df_filtrado[variable].sum()

            st.markdown("### ∑ Conteo de filtros seleccionados")
            st.metric(
                label=f"Total {titulo}",
                value=f"{total_metric:,.0f}"
            )

            st.markdown("---")

            # -------------------------
            # CIRCUITO
            # -------------------------
            circuito = df_filtrado.groupby("circuito", as_index=False)[variable].sum()
            circuito = circuito.sort_values(variable, ascending=False)

            top9_cir = circuito.head(9)
            otros_cir = pd.DataFrame({
                "circuito": ["Otros"],
                variable: [circuito.iloc[9:][variable].sum()]
            })

            circuito_final = pd.concat([top9_cir, otros_cir])

            fig1 = px.pie(
                circuito_final,
                names="circuito",
                values=variable,
                title=f"{titulo} por circuito de distribución (Top 9 + Otros)"
            )

            fig1.update_traces(textposition="inside", textinfo="percent")
            fig1.update_layout(height=700)

            st.plotly_chart(fig1, use_container_width=True)

            # -------------------------
            # RANGO DE PANTALLAS (%)
            # -------------------------
            df_pan = df_filtrado.copy()

            # Mapear etiquetas
            df_pan["rango_pan_label"] = df_pan["rango_pantallas"].map(mapa_rango_pan)
             
            # Agrupar
            pan = df_pan.groupby("rango_pan_label", as_index=False)[variable].sum()
             
            # Calcular porcentaje
            total_pan = pan[variable].sum()
            pan["pct"] = (pan[variable] / total_pan) * 100

            # Orden lógico (no por valor)
            orden_labels_pan = [mapa_rango_pan[k] for k in mapa_rango_pan.keys()]
            pan["rango_pan_label"] = pd.Categorical(
                 pan["rango_pan_label"],
                 categories=orden_labels_pan,
                 ordered=True
                 )
            pan = pan.sort_values("rango_pan_label")

            # Gráfica
            fig4 = px.bar(
                 pan,
                 x="rango_pan_label",
                 y="pct",
                 title=f"{titulo} por rango de pantallas (%)",
                 hover_data={variable: ":,.0f", "pct": ":.1f"}
                 )

            fig4.update_traces(
                 texttemplate="%{y:,.1f}%",
                 textposition="outside",
                 hovertemplate=(
                     "Rango: %{x}<br>"
                     "Valor: %{customdata[0]:,.0f}<br>"
                     "Porcentaje: %{y:.1f}%<br>"
                     "<extra></extra>"
                     )
                 )

            fig4.update_layout(
                 yaxis_title="Porcentaje (%)",
                 xaxis_title="",
                 yaxis=dict(range=[0, pan["pct"].max() * 1.2])
                 )

            st.plotly_chart(fig4, use_container_width=True)
                  
            # -------------------------
            # RANGOS DE TÍTULOS (Top 9 + Otros)
            # -------------------------
            df_rangos = df_filtrado.copy()

            # Mapear etiquetas
            df_rangos["rango_tit_label"] = df_rangos["rango_titulos"].map(mapa_rango_tit)

            # Agrupar
            rangos = df_rangos.groupby("rango_tit_label", as_index=False)[variable].sum()

            # Ordenar de mayor a menor (IMPORTANTE para Top 9)
            rangos = rangos.sort_values(variable, ascending=False)

            # Top 9
            top9 = rangos.head(9)

            # Otros
            otros = pd.DataFrame({
                "rango_tit_label": ["Otros"],
                variable: [rangos.iloc[9:][variable].sum()]
            })

            # Concatenar
            rangos_final = pd.concat([top9, otros])

            # Pie chart
            fig3 = px.pie(
                rangos_final,
                names="rango_tit_label",
                values=variable,
                title=f"{titulo} por rango de títulos exhibidos (Top 9 + Otros)"
            )

            fig3.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            fig3.update_layout(height=700)

            st.plotly_chart(fig3, use_container_width=True)
            
            # -------------------------
            # REGION (%)
            # -------------------------
            region = df_filtrado.groupby("region", as_index=False)[variable].sum()
            total = region[variable].sum()
            region["pct"] = (region[variable] / total) * 100
            
            fig2 = px.bar(
                region,
                x="region",
                y="pct",
                title=f"{titulo} por región geográfica (%)",
                hover_data={variable: ":,.0f", "pct": ":.1f"}
                )

            fig2.update_traces(
                  texttemplate="%{y:,.1f}%",
                  textposition="outside",
                  hovertemplate=(
                      "Región: %{x}<br>"
                      "Valor: %{customdata[0]:,.0f}<br>"
                      "Porcentaje: %{y:.1f}%<br>"
                      "<extra></extra>"
                      )
                  )

            fig2.update_layout(
                  yaxis_title="Porcentaje (%)",
                  xaxis_title="",
                  yaxis=dict(range=[0, region["pct"].max() * 1.2])
                  )

            st.plotly_chart(fig2, use_container_width=True)
      
            # -------------------------
            # MAPA (CIUDADES)
            # -------------------------
            
            df_map = (
                df_filtrado
                .dropna(subset=["lat", "lon", variable])
                .groupby(["estado_f", "ciudad_f", "lat", "lon"], as_index=False)[variable]
                .sum()
                )

            df_map["lat"] = pd.to_numeric(df_map["lat"], errors="coerce")
            df_map["lon"] = pd.to_numeric(df_map["lon"], errors="coerce")

            fig5 = px.scatter_mapbox(
                df_map,
                lat="lat",
                lon="lon",
                size=variable,
                color=variable,
                hover_name="ciudad_f",
                hover_data=["estado_f", variable],
                zoom=4,
                mapbox_style="open-street-map"
                )

            fig5.update_layout(
                title=f"{titulo} por ciudad y estado",
                height=600
                )

            st.plotly_chart(fig5, use_container_width=True)
          
    # =====================================================
    # SELECCIÓN MÉTRICA
    # =====================================================
    if metrica == "Cines":
            generar_dashboard("cines", "Cines", df)

    elif metrica == "Pantallas":
            generar_dashboard("pantallas", "Pantallas", df)

    elif metrica == "Taquilla_ingresos":
            generar_dashboard("ing_year", "Ingresos", df)
            
    elif metrica == "Taquilla_boletos":
            generar_dashboard("adm_year", "Boletos", df)
