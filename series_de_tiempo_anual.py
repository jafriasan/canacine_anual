#Código que genera la sección de Series de tiempo del Dashboard de Canacine (Estadísticas de taquilla en México)

import streamlit as st
import pandas as pd
#import plotly.express as px
import plotly.graph_objects as go


def dashboard_series_tiempo():

    st.title("📈 Series de tiempo")

    # -----------------------------
    # CARGA DE DATOS
    # -----------------------------
    archivo = "cubo_resumen_2000_2025.xlsx"

    @st.cache_data
    def load_data():
        return pd.read_excel(archivo, keep_default_na=False)

    df = load_data()

    # -----------------------------
    # MÉTRICA
    # -----------------------------
    metrica = st.sidebar.selectbox(
        "Métricas",
        ["Taquilla ingresos", "Taquilla boletos", "Títulos / Estrenos"],
        key="metrica_selector"
    )

    # -----------------------------
    # FILTROS
    # -----------------------------
    st.sidebar.header("Filtros")

    def create_filter(column=None, label="", options=None, format_func=None, default=None):
        if options is None:
            options = sorted(df[column].dropna().unique())

        if format_func is None:
            format_func = lambda x: x

        return st.sidebar.multiselect(
            label,
            options=options,
            default=default if default is not None else [],
            format_func=format_func
        )

    # -----------------------
    # FILTROS
    # -----------------------

    # País de origen
    f_mexico = create_filter(
        column=None,
        label="País de origen",
        options=[1, 0],
        format_func=lambda x: "México" if x == 1 else "Resto",
        default=[]
    )


    # Otros filtros
    f_pais = create_filter("pais_primario", "País primario")
    f_pais_no_primario = create_filter("pais_no_primario", "País no primario")
    f_genero = create_filter("genero_primario", "Género primario")
    f_clas = create_filter("clas", "Clasificación")
    f_dist = create_filter("dist_1", "Distribuidor")
    f_idioma = create_filter("ideomas", "Idioma")
    
    mapa_semanas = {
        #"S00": "Preestrenos",
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
    
    
    orden_semanas = [f"S{str(i).zfill(2)}" for i in range(1,18)]
    
    f_rango_sem = create_filter(
        "rango_semanas",
        "Rango de semanas en cine",
        options=orden_semanas,
        format_func=lambda x: mapa_semanas.get(x, x)
    )
    
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
    
    orden_cines = ["NA"] + [f"C{str(i).zfill(2)}" for i in range(1, 20)]
    
    f_rango_cines = create_filter(
        "rango_cines",
        "Rango de cines",
        options=orden_cines,
        format_func=lambda x: mapa_cines.get(x, x)
    )
    
    # NOTAS DEBAJO DEL FILTRO
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
    df_filtered = df.copy()

    if f_mexico:
        df_filtered = df_filtered[df_filtered["mexico"].isin(f_mexico)]

    if f_pais:
        df_filtered = df_filtered[df_filtered["pais_primario"].isin(f_pais)]

    if f_pais_no_primario:
        df_filtered = df_filtered[df_filtered["pais_no_primario"].isin(f_pais_no_primario)]

    if f_genero:
        df_filtered = df_filtered[df_filtered["genero_primario"].isin(f_genero)]

    if f_clas:
        df_filtered = df_filtered[df_filtered["clas"].isin(f_clas)]

    if f_dist:
        df_filtered = df_filtered[df_filtered["dist_1"].isin(f_dist)]

    if f_idioma:
        df_filtered = df_filtered[df_filtered["ideomas"].isin(f_idioma)]
        
    if f_rango_sem:
        df_filtered = df_filtered[df_filtered["rango_semanas"].isin(f_rango_sem)]
        
    if f_rango_cines:
        df_filtered = df_filtered[df_filtered["rango_cines"].isin(f_rango_cines)]

    # =====================================================
    # 📊 DASHBOARD INGRESOS
    # =====================================================
    if metrica == "Taquilla ingresos":

        df_grouped = (
            df_filtered
            .groupby("year", as_index=False)[["ing_year", "ing_real_year"]]
            .sum()
            .sort_values("year")
        )

        df_grouped["year"] = df_grouped["year"].astype(int)

        df_grouped["ing_year_millones"] = df_grouped["ing_year"] / 1_000_000
        df_grouped["ing_real_year_millones"] = df_grouped["ing_real_year"] / 1_000_000
        
        df_grouped["var_ing_year"] = df_grouped["ing_year_millones"].pct_change() * 100
        df_grouped["var_ing_real"] = df_grouped["ing_real_year_millones"].pct_change() * 100

        df_grouped["var_ing_year"] = df_grouped["var_ing_year"].fillna(0)
        df_grouped["var_ing_real"] = df_grouped["var_ing_real"].fillna(0)

        # -----------------------------
        # KPIs
        # -----------------------------
        total_ing = df_grouped["ing_year_millones"].sum()
        ultimo_ing = df_grouped["ing_year_millones"].iloc[-1]
        var_ing = df_grouped["var_ing_real"].iloc[-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total acumulado (millones)", f"{total_ing:,.0f}")
        col2.metric("📅 Último año (millones)", f"{ultimo_ing:,.0f}")
        col3.metric("📈 Variación real último año (%)", f"{var_ing:,.1f}%")

        st.markdown("---")


        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_grouped["year"],
            y=df_grouped["ing_year_millones"],
            name="Millones de pesos ingresados",
            marker_color="blue",
            text=df_grouped["ing_year_millones"],
            texttemplate="%{text:,.0f}",
            textposition="outside"
        ))

        fig.add_trace(go.Scatter(
            x=df_grouped["year"],
            y=df_grouped["ing_real_year_millones"],
            name="Datos ajustados por el INPC (2025 = 100)",
            mode="lines+markers",
            line=dict(color="red", width=3)
        ))

        x_min = int(df_grouped["year"].min())
        x_max = int(df_grouped["year"].max())

        fig.update_layout(
            title="Ingresos por año",
            xaxis=dict(
                range=[x_min - 0.5, x_max + 0.5],
                tickmode="linear",
                dtick=1
            ),
            margin=dict(t=80),
            legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center")
        )

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=df_grouped["year"],
            y=df_grouped["var_ing_year"],
            name="Variación nominal",
            line=dict(color="blue")
        ))

        fig2.add_trace(go.Scatter(
            x=df_grouped["year"],
            y=df_grouped["var_ing_real"],
            name="Variación real",
            line=dict(color="red")
        ))

        fig2.update_layout(
            title="Variación anual (%)",
            xaxis=dict(
                range=[x_min - 0.5, x_max + 0.5],
                tickmode="linear",
                dtick=1
            ),
            margin=dict(t=80),
            legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center")
        )

        st.plotly_chart(fig, use_container_width=True, key="ingresos")
        st.plotly_chart(fig2, use_container_width=True, key="variacion_ingresos")

        df_table = df_grouped

    # =====================================================
    # 🎬 DASHBOARD BOLETOS
    # =====================================================
    elif metrica == "Taquilla boletos":

        df_grouped = (
            df_filtered
            .groupby("year", as_index=False)[["adm_year"]]
            .sum()
            .sort_values("year")
        )

        df_grouped["year"] = df_grouped["year"].astype(int)
        df_grouped["adm_year_millones"] = df_grouped["adm_year"] / 1_000_000
        df_grouped["var_adm"] = df_grouped["adm_year_millones"].pct_change() * 100
        df_grouped.fillna(0, inplace=True)

        # KPIs
        total = df_grouped["adm_year_millones"].sum()
        ultimo = df_grouped["adm_year_millones"].iloc[-1]
        var = df_grouped["var_adm"].iloc[-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("🎟️ Total acumulado (millones)", f"{total:,.0f}")
        col2.metric("📅 Último año (millones)", f"{ultimo:,.0f}")
        col3.metric("📈 Variación último año (%)", f"{var:,.1f}%")

        st.markdown("---")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_grouped["year"],
            y=df_grouped["adm_year_millones"],
            marker_color="green",
            text=df_grouped["adm_year_millones"],
            texttemplate="%{text:,.0f}",
            textposition="outside"
        ))

        x_min = int(df_grouped["year"].min())
        x_max = int(df_grouped["year"].max())

        fig.update_layout(
            title="Millones de boletos vendidos por año",
            xaxis=dict(range=[x_min - 0.5, x_max + 0.5], tickmode="linear", dtick=1),
            margin=dict(t=80)
        )

        st.plotly_chart(fig, use_container_width=True, key="boletos")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_grouped["year"],
            y=df_grouped["var_adm"],
            mode="lines+markers",
            line=dict(color="green")
        ))

        fig2.update_layout(
            title="Variación anual (%)",
            xaxis=dict(range=[x_min - 0.5, x_max + 0.5], tickmode="linear", dtick=1),
            margin=dict(t=80)
        )

        st.plotly_chart(fig2, use_container_width=True, key="var_boletos")

        df_table = df_grouped

    # =====================================================
    # 🎬 DASHBOARD TÍTULOS / ESTRENOS
    # =====================================================
    else:

        df_grouped = (
            df_filtered
            .groupby("year", as_index=False)[["titulos", "estreno"]]
            .sum()
            .sort_values("year")
        )

        df_grouped["year"] = df_grouped["year"].astype(int)

        x_min = int(df_grouped["year"].min())
        x_max = int(df_grouped["year"].max())
        
        df_grouped["var_titulos"] = df_grouped["titulos"].pct_change() * 100
        df_grouped["var_estreno"] = df_grouped["estreno"].pct_change() * 100

        df_grouped["var_titulos"] = df_grouped["var_titulos"].fillna(0)
        df_grouped["var_estreno"] = df_grouped["var_estreno"].fillna(0)
        
        total_tit = df_grouped["titulos"].sum()
        ultimo_tit = df_grouped["titulos"].iloc[-1]
        var_tit = df_grouped["var_titulos"].iloc[-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total de títulos acumulado", f"{total_tit:,.0f}")
        col2.metric("📅 Último año", f"{ultimo_tit:,.0f}")
        col3.metric("📈 Variación último año (%)", f"{var_tit:,.1f}%")

        st.markdown("---")

        # -----------------------------
        # GRÁFICA 1: NIVELES
        # -----------------------------
        fig = go.Figure()

        # Barras (estrenos)
        fig.add_trace(go.Bar(
            x=df_grouped["year"],
            y=df_grouped["estreno"],
            name="Estrenos",
            marker_color="blue",
            text=df_grouped["estreno"],
            texttemplate="%{text:,.0f}",
            textposition="outside"
        ))

        # Línea (títulos)
        fig.add_trace(go.Scatter(
        x=df_grouped["year"],
        y=df_grouped["titulos"],
        name="Total de títulos",
        mode="lines+markers+text",  
        text=df_grouped["titulos"],
        texttemplate="%{text:,.0f}",
        textposition="top center", 
        line=dict(color="red", width=3)
        ))

        fig.update_layout(
            title="Total de títulos y estrenos por año",
            xaxis=dict(
                range=[x_min - 0.5, x_max + 0.5],
                tickmode="linear",
                dtick=1
            ),
            margin=dict(t=80),
            legend=dict(
                orientation="h",
                y=1.02,
                x=0.5,
                xanchor="center"
            )
        )

        # -----------------------------
        # GRÁFICA 2: VARIACIÓN
        # -----------------------------

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=df_grouped["year"],
            y=df_grouped["var_titulos"],
            name="Variación total de títulos (%)",
            mode="lines+markers",
            line=dict(color="red")
        ))

        fig2.add_trace(go.Scatter(
            x=df_grouped["year"],
            y=df_grouped["var_estreno"],
            name="Variación de estrenos (%)",
            mode="lines+markers",
            line=dict(color="blue")
        ))

        fig2.update_layout(
            title="Variación anual (%)",
            xaxis=dict(
                range=[x_min - 0.5, x_max + 0.5],
                tickmode="linear",
                dtick=1
            ),
            margin=dict(t=80),
            legend=dict(
                orientation="h",
                y=1.02,
                x=0.5,
                xanchor="center"
            )
        )

        st.plotly_chart(fig, use_container_width=True, key="titulos")
        st.plotly_chart(fig2, use_container_width=True, key="variacion_titulos")

        df_table = df_grouped

    # -----------------------------
    # TABLA FINAL
    # -----------------------------
    with st.expander("Ver datos agrupados"):
        st.dataframe(df_table)
