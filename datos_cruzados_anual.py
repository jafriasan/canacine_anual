#Código que genera sección de Datos cruzados del dashboard de Canacine con estadísticas de taquilla en México

import streamlit as st
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go

def dashboard_datos_cruzados():

    st.title("📈 Datos cruzados")

    # -----------------------------
    # CARGA DE DATOS
    # -----------------------------
    archivo = "cubo_resumen_2000_2025.xlsx"

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
        ["Taquilla ingreso", "Taquilla boletos", "Títulos", "Estrenos"],
        index=0
    )
    #st.markdown("### ⚙️ Filtros")
    
    st.sidebar.header("Filtros")

    anios = st.sidebar.multiselect(
        "Año(s)",
        sorted(df_base["year"].dropna().unique()),
        default=[ultimo_anio]
    )

    pais = st.sidebar.multiselect(
        "País de origen",
        options=[1, 0],
        default=[1, 0],
        format_func=lambda x: "México" if x == 1 else "Resto"
    )

    # NOTA AGREGADA JUSTO DEBAJO DEL FILTRO
    st.sidebar.markdown(
    "<p style='font-size:11px; color:gray;'>"
    "En País de origen, México Refiere a casos con participación de México como país de origen (primario o no primario)."
    "</p>",
    unsafe_allow_html=True
    )
    
    st.sidebar.markdown(
    "<p style='font-size:11px; color:gray;'>"
    "Rango de cines, refiere al número de cines en los que se exhibió la película en su primer fin de semana)."
    "</p>",
    unsafe_allow_html=True
    )
    
    st.sidebar.markdown(
    "<p style='font-size:11px; color:gray;'>"
    "Fuente: Comscore."
    "</p>",
    unsafe_allow_html=True
    )

    # -----------------------------
    # APLICAR FILTROS
    # -----------------------------
    df = df_base.copy()

    if anios:
        df = df[df["year"].isin(anios)]

    if pais:
        df = df[df["mexico"].isin(pais)]

    # -----------------------------
    # AGRUPACIÓN PAÍS PRIMARIO
    # -----------------------------
    def clasificar_pais(x):
        x = str(x).lower()
        if "mex" in x:
            return "México"
        elif "usa" in x or "estados unidos" in x or "united states" in x:
            return "USA"
        else:
            return "Otros"

    df["pais_group"] = df["pais_primario"].apply(clasificar_pais)

    # -----------------------------
    # AGRUPACIÓN PAÍS NO PRIMARIO
    # -----------------------------
    def clasificar_pais_sec(x):
        x = str(x).lower()
        if "mex" in x:
            return "México"
        elif "usa" in x or "estados unidos" in x or "united states" in x:
            return "USA"
        else:
            return "Otros"

    df["pais_group_sec"] = df["pais_no_primario"].apply(clasificar_pais_sec)

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
        # GÉNERO
        # -------------------------
        genero = df_filtrado.groupby("genero_primario", as_index=False)[variable].sum()
        genero = genero.sort_values(variable, ascending=False)

        top9_gen = genero.head(9)
        otros_gen = pd.DataFrame({
            "genero_primario": ["Otros"],
            variable: [genero.iloc[9:][variable].sum()]
        })

        genero_final = pd.concat([top9_gen, otros_gen])

        fig1 = px.pie(
            genero_final,
            names="genero_primario",
            values=variable,
            title=f"{titulo} por género primario (Top 9 + Otros)"
        )

        fig1.update_traces(textposition="inside", textinfo="percent")
        fig1.update_layout(height=700)

        st.plotly_chart(fig1, use_container_width=True)

        # -------------------------
        # CLASIFICACIÓN (%)
        # -------------------------
        clasif = df_filtrado.groupby("clas", as_index=False)[variable].sum()
        total = clasif[variable].sum()
        clasif["pct"] = (clasif[variable] / total) * 100

        fig2 = px.bar(
            clasif,
            x="clas",
            y="pct",
            title=f"{titulo} por clasificación (%)",
            hover_data={variable: ":,.0f", "pct": ":.1f"}
        )

        fig2.update_traces(
            texttemplate="%{y:,.1f}%",
            textposition="outside",
            hovertemplate=(
                "Clasificación: %{x}<br>"
                "Valor: %{customdata[0]:,.0f}<br>"
                "Porcentaje: %{y:.1f}%<br>"
                "<extra></extra>"
            )
        )

        fig2.update_layout(
            yaxis_title="Porcentaje (%)",
            xaxis_title="",
            yaxis=dict(range=[0, clasif["pct"].max() * 1.2])
        )

        st.plotly_chart(fig2, use_container_width=True)

        # -------------------------
        # PAÍS PRIMARIO
        # -------------------------
        pais_chart = df_filtrado.groupby("pais_group", as_index=False)[variable].sum()

        fig3 = px.pie(
            pais_chart,
            names="pais_group",
            values=variable,
            title=f"{titulo} por país primario (México / USA / Otros)",
            color="pais_group",
            color_discrete_map={
                "México": "#16a34a",
                "USA": "#2563eb",
                "Otros": "#9ca3af"
            }
        )

        fig3.update_traces(textposition="inside", textinfo="percent+label")
        fig3.update_layout(height=700)

        st.plotly_chart(fig3, use_container_width=True)

        # -------------------------
        # PAÍS NO PRIMARIO
        # -------------------------
        pais_sec = df_filtrado.groupby("pais_group_sec", as_index=False)[variable].sum()

        total_sec = pais_sec[variable].sum()
        pais_sec["Porcentaje (%)"] = (pais_sec[variable] / total_sec) * 100

        pais_sec = pais_sec.sort_values("Porcentaje (%)", ascending=False)

        fig4 = px.bar(
            pais_sec,
            x="pais_group_sec",
            y="Porcentaje (%)",
            title=f"{titulo} por país no primario (%)",
            color="pais_group_sec",
            color_discrete_map={
                "México": "#16a34a",
                "USA": "#2563eb",
                "Otros": "#9ca3af"
            },
            hover_data={variable: ":,.0f", "Porcentaje (%)": ":.1f"}
        )

        fig4.update_traces(
            texttemplate="%{y:,.1f}%",
            textposition="outside",
            hovertemplate=(
                "País: %{x}<br>"
                "Valor: %{customdata[0]:,.0f}<br>"
                "Porcentaje: %{y:.1f}%<br>"
                "<extra></extra>"
            )
        )

        fig4.update_layout(
            showlegend=False,
            yaxis=dict(range=[0, pais_sec["Porcentaje (%)"].max() * 1.25]),
            xaxis_title=""
        )

        st.plotly_chart(fig4, use_container_width=True)

        # -------------------------
        # DISTRIBUIDORES
        # -------------------------
        dist = df_filtrado.groupby("dist_1", as_index=False)[variable].sum()
        dist = dist.sort_values(variable, ascending=False)

        top9 = dist.head(9)
        otros = pd.DataFrame({
            "dist_1": ["Otros"],
            variable: [dist.iloc[9:][variable].sum()]
        })

        dist_final = pd.concat([top9, otros])

        fig5 = px.pie(
            dist_final,
            names="dist_1",
            values=variable,
            title=f"{titulo} por distribuidor (Top 9 + Otros)"
        )

        fig5.update_layout(height=700)

        st.plotly_chart(fig5, use_container_width=True)
        
       # -------------------------
       # RANGO DE SEMANAS EN CINES
       # -------------------------

        # Agrupar
        sem = df_filtrado.groupby("rango_semanas", as_index=False)[variable].sum()

        # Mapeo de etiquetas
        mapa_semanas = {
            "S00": "Preestrenos",
            "S01": "1 Semana",
            "S02": "2 Semanas",
            "S03": "3 Semanas",
            "S04": "4 Semanas",
            "S05": "5 Semanas",
            "S06": "6 Semanas",
            "S07": "7 Semanas",
            "S08": "8 Semanas",
            "S09": "9 Semanas",
            "S10": "10 Semanas",
            "S11": "11 Semanas",
            "S12": "12 Semanas",
            "S13": "13 Semanas",
            "S14": "14 Semanas",
            "S15": "15 Semanas",
            "S16": "16 Semanas",
            "S17": "Más de 16 semanas"
        }

        # Aplicar etiquetas
        sem["rango_semanas_label"] = sem["rango_semanas"].map(mapa_semanas)

        # Ordenar correctamente (por código original, no por valor)
        sem = sem.sort_values("rango_semanas")

        # Gráfica completa (sin top ni otros)
        fig6 = px.pie(
        sem,
            names="rango_semanas_label",
            values=variable,
            title=f"{titulo} por rango de semanas en cines"
        )

        fig6.update_layout(height=700)

        st.plotly_chart(fig6, use_container_width=True)     
        
        # -----------------------------------------------
        # RANGO DE CINES EL FIN DE SEMANA DE ESTRENO (%)
        # -----------------------------------------------
        
        mapa_cines = {
            "NA": "No aplica",
            "C01": "1 Cine",
            "C02": "2 Cines",
            "C03": "3 Cines",
            "C04": "4 Cines",
            "C05": "5 Cines",
            "C06": "6-10 Cines",
            "C07": "11-15 Cines",
            "C08": "16-20 Cines",
            "C09": "21-30 Cines",
            "C10": "31-40 Cines",
            "C11": "41-50 Cines",
            "C12": "51-100 Cines",
            "C13": "101-200 Cines",
            "C14": "201-300 Cines",
            "C15": "301-400 Cines",
            "C16": "401-500 Cines",
            "C17": "501-700 Cines",
            "C18": "701-900 Cines",
            "C19": "> 900 Cines"
        }    

        cines = df_filtrado.groupby("rango_cines", as_index=False)[variable].sum()

        total = cines[variable].sum()
        cines["pct"] = (cines[variable] / total) * 100

        # Crear columna con etiquetas
        cines["rango_cines_label"] = cines["rango_cines"].map(mapa_cines)

        # Orden correcto
        orden_cines = ["NA"] + [f"C{str(i).zfill(2)}" for i in range(1, 20)]

        cines["rango_cines"] = pd.Categorical(
            cines["rango_cines"],
            categories=orden_cines,
            ordered=True
        )

        cines = cines.sort_values("rango_cines")

        # Gráfica
        fig7 = px.bar(
            cines,
            x="rango_cines_label",
            y="pct",
            title=f"{titulo} por rango de cines (%)",
            hover_data={variable: ":,.0f", "pct": ":.1f"}
        )

        fig7.update_traces(
            texttemplate="%{y:,.1f}%",
            textposition="outside",
            hovertemplate=(
                "Rango de cines: %{x}<br>"
                "Valor: %{customdata[0]:,.0f}<br>"
                "Porcentaje: %{y:.1f}%<br>"
                "<extra></extra>"
                )
        )

        fig7.update_layout(
            yaxis_title="Porcentaje (%)",
            xaxis_title="",
            yaxis=dict(range=[0, cines["pct"].max() * 1.2])
        )

        st.plotly_chart(fig7, use_container_width=True)

    # =====================================================
    # SELECCIÓN MÉTRICA
    # =====================================================
    if metrica == "Taquilla ingreso":
        generar_dashboard("ing_year", "Ingreso", df)

    elif metrica == "Taquilla boletos":
        generar_dashboard("adm_year", "Boletos", df)

    elif metrica == "Títulos":
        generar_dashboard("titulos", "Títulos", df)

    elif metrica == "Estrenos":
        generar_dashboard("estreno", "Estrenos", df)
        
