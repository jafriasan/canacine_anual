# Se crea la sección de series de tiempos para la estadística de cines. Esta sección es parte de un dashboard de taquilla en México.

import streamlit as st
import pandas as pd
#import plotly.express as px
import plotly.graph_objects as go


def dashboard_series_tiempo_cines():

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
            ["Taquilla ingresos", "Taquilla boletos","Cines","Pantallas"],
            key="metrica_selector"
    )

    # -----------------------------
    # FILTROS
    # -----------------------------
    st.sidebar.header("Filtros")

    def create_filter(column, label, df_source, options=None, format_func=None, default=None):
        if options is None:
            options = sorted(df_source[column].dropna().unique())

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
        
        
    orden_rango_tit = [f"T{str(i).zfill(2)}" for i in range(1,18)]    
        
        
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
        
        
    orden_rango_pan = [f"P{str(i).zfill(2)}" for i in range(1,9)]  
        

    # -----------------------
    # BASE DATAFRAME
    # -----------------------
    df_temp = df.copy()

    # -----------------------
    # 1. ESTADO
    # -----------------------
    f_estado = create_filter(
        "estado_f",
        "Entidad(es) federativa(s)",
        df_temp
    )

    if f_estado:
        df_temp = df_temp[df_temp["estado_f"].isin(f_estado)]

    # -----------------------
    # 2. CIUDAD (DEPENDE DE ESTADO)
    # -----------------------
    f_ciudad = create_filter(
        "ciudad_f",
        "Ciudad(es)",
        df_temp
    )

    if f_ciudad:
        df_temp = df_temp[df_temp["ciudad_f"].isin(f_ciudad)]

    # -----------------------
    # 3. CIRCUITO (DEPENDE DE CIUDAD)
    # -----------------------
    f_circuito = create_filter(
        "circuito",
        "Circuito",
        df_temp
    )

    if f_circuito:
        df_temp = df_temp[df_temp["circuito"].isin(f_circuito)]

    # -----------------------
    # 4. REGIÓN
    # -----------------------
    f_region = create_filter(
        "region",
        "Región",
        df_temp
    )

    if f_region:
        df_temp = df_temp[df_temp["region"].isin(f_region)]

    # -----------------------
    # 5. RANGO TÍTULOS
    # -----------------------
    f_rango_tit = create_filter(
        "rango_titulos",
        "Rango de títulos exhibidos",
        df_temp,
        options=orden_rango_tit,
        format_func=lambda x: mapa_rango_tit.get(x, x)
    )

    if f_rango_tit:
        df_temp = df_temp[df_temp["rango_titulos"].isin(f_rango_tit)]

    # -----------------------
    # 6. RANGO PANTALLAS
    # -----------------------
    f_rango_pan = create_filter(
        "rango_pantallas",
        "Rango de pantallas",
        df_temp,
        options=orden_rango_pan,
        format_func=lambda x: mapa_rango_pan.get(x, x)
    )

    if f_rango_pan:
        df_temp = df_temp[df_temp["rango_pantallas"].isin(f_rango_pan)]

    # -----------------------
    # DATA FINAL
    # -----------------------
    df_filtered = df_temp.copy()

    # NOTA
    st.sidebar.markdown(
        "<p style='font-size:11px; color:gray;'>Fuente: Comscore.</p>",
        unsafe_allow_html=True
    )


    # -----------------------------
    # APLICAR FILTROS
    # -----------------------------

    df_filtered = df.copy()

    if f_circuito:
            df_filtered = df_filtered[df_filtered["circuito"].isin(f_circuito)]
            
    if f_rango_pan:
            df_filtered = df_filtered[df_filtered["rango_pantallas"].isin(f_rango_pan)]
            
    if f_rango_tit:
            df_filtered = df_filtered[df_filtered["rango_titulos"].isin(f_rango_tit)]

    if f_region:
            df_filtered = df_filtered[df_filtered["region"].isin(f_region)]

    if f_estado:
            df_filtered = df_filtered[df_filtered["estado_f"].isin(f_estado)]

    if f_ciudad:
            df_filtered = df_filtered[df_filtered["ciudad_f"].isin(f_ciudad)]

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
    # 🎬 DASHBOARD CINES
    # =====================================================
    elif metrica == "Cines":

            df_grouped = (
                df_filtered
                .groupby("year", as_index=False)[["cines"]]
                .sum()
                .sort_values("year")
            )

            df_grouped["year"] = df_grouped["year"].astype(int)

            x_min = int(df_grouped["year"].min())
            x_max = int(df_grouped["year"].max())
            
            df_grouped["var_cines"] = df_grouped["cines"].pct_change() * 100
            df_grouped["var_cines"] = df_grouped["var_cines"].fillna(0)

            
            total_cines = df_grouped["cines"].sum()
            ultimo_cines = df_grouped["cines"].iloc[-1]
            var_cines = df_grouped["var_cines"].iloc[-1]

            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total de cines acumulado", f"{total_cines:,.0f}")
            col2.metric("📅 Último año", f"{ultimo_cines:,.0f}")
            col3.metric("📈 Variación último año (%)", f"{var_cines:,.1f}%")

            st.markdown("---")

            # -----------------------------
            # GRÁFICA 1: NIVELES
            # -----------------------------
            fig = go.Figure()

            # Barras (cines)
            fig.add_trace(go.Bar(
                x=df_grouped["year"],
                y=df_grouped["cines"],
                name="Cines",
                marker_color="blue",
                text=df_grouped["cines"],
                texttemplate="%{text:,.0f}",
                textposition="outside"
            ))


            fig.update_layout(
                title="Total de cines por año",
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
                y=df_grouped["var_cines"],
                name="Variación total de cines (%)",
                mode="lines+markers",
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
                legend=dict(
                    orientation="h",
                    y=1.02,
                    x=0.5,
                    xanchor="center"
                )
            )

            st.plotly_chart(fig, use_container_width=True, key="cines")
            st.plotly_chart(fig2, use_container_width=True, key="variacion_cines")

            df_table = df_grouped
            
    # =====================================================
    # 🎬 DASHBOARD PANTALLAS
    # =====================================================
    else:

                df_grouped = (
                    df_filtered
                    .groupby("year", as_index=False)[["pantallas"]]
                    .sum()
                    .sort_values("year")
                )

                df_grouped["year"] = df_grouped["year"].astype(int)

                x_min = int(df_grouped["year"].min())
                x_max = int(df_grouped["year"].max())
                
                df_grouped["var_pan"] = df_grouped["pantallas"].pct_change() * 100
                df_grouped["var_pan"] = df_grouped["var_pan"].fillna(0)

                
                total_pan = df_grouped["pantallas"].sum()
                ultimo_pan = df_grouped["pantallas"].iloc[-1]
                var_pan = df_grouped["var_pan"].iloc[-1]

                col1, col2, col3 = st.columns(3)
                col1.metric("💰 Total de pantallas acumulado", f"{total_pan:,.0f}")
                col2.metric("📅 Último año", f"{ultimo_pan:,.0f}")
                col3.metric("📈 Variación último año (%)", f"{var_pan:,.1f}%")

                st.markdown("---")

                # -----------------------------
                # GRÁFICA 1: NIVELES
                # -----------------------------
                fig = go.Figure()

                # Barras (pantallas)
                fig.add_trace(go.Bar(
                    x=df_grouped["year"],
                    y=df_grouped["pantallas"],
                    name="Pantallas",
                    marker_color="blue",
                    text=df_grouped["pantallas"],
                    texttemplate="%{text:,.0f}",
                    textposition="outside"
                ))


                fig.update_layout(
                    title="Total de pantallas por año",
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
                    y=df_grouped["var_pan"],
                    name="Variación total de pantallas (%)",
                    mode="lines+markers",
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
                    legend=dict(
                        orientation="h",
                        y=1.02,
                        x=0.5,
                        xanchor="center"
                    )
                )

                st.plotly_chart(fig, use_container_width=True, key="pantallas")
                st.plotly_chart(fig2, use_container_width=True, key="variacion_pantallas")

                df_table = df_grouped

    # -----------------------------
    # TABLA FINAL
    # -----------------------------
    with st.expander("Ver datos agrupados"):
            st.dataframe(df_table)    
