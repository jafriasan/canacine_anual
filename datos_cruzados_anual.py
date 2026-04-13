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
        return pd.read_excel(archivo)

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
        "Aaño(s)",
        sorted(df_base["year"].dropna().unique()),
        default=[ultimo_anio]
    )

    pais = st.sidebar.multiselect(
        "País de origen",
        options=[1, 0],
        default=[1, 0],
        format_func=lambda x: "México" if x == 1 else "Resto"
    )

    # NOTA AGREGADA
    st.sidebar.markdown(
    "<p style='font-size:11px; color:gray;'>"
    "En País de origen, México Refiere a casos con participación de México como país de origen (primario o no primario)."
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
