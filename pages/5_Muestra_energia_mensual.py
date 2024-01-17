import os
import datetime 
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time

carpeta = os.path.dirname(__file__)
ruta_excel = os.path.join(carpeta, 'Datos_climatologicos_Santa_Fe_2019.xlsx')
df = pd.read_excel(ruta_excel, index_col=0)
st.dataframe(df)

with st.sidebar: 
    st.write('# Completar datos Pag. 2')
    
    N = st.slider('Cantidad de paneles', min_value=1,  max_value=1000, value=250, step=1) 
    Ppico = st.number_input('Pot. pico del panel (W)', min_value=0,  max_value=500, value=240, step=10) 
    kp = st.number_input('Coef. de Pot - Temp (1/°C)', min_value=-0.01,  max_value=0., value=-0.0044, step=0.0001, format='%.4f')
    eta = st.number_input('Rendimiento General (p.u.)', min_value=0.1,  max_value=1., value=0.97, step=0.01, format='%.2f')


df['FechaHora'] = pd.to_datetime(df['Fecha'])
df['Mes'] = df['FechaHora'].dt.month


energias_mensuales = []
for mes in range(1, 13):
    filtro_mes = df['Mes'] == mes
    df_mes = df[filtro_mes]
    
    pot_media_mes = df_mes['Irradiancia (W/m²)'].mean()
    
    siguiente_mes = 1 if mes + 1 > 12 else mes + 1
    horas_en_mes = 24 * pd.Timestamp(f'2019-{siguiente_mes}-1').days_in_month
    energia_mensual = pot_media_mes * horas_en_mes / 1000
    energias_mensuales.append(energia_mensual)


meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
chart_data = pd.DataFrame({
    "Meses": meses,
    "Energia Mensual": energias_mensuales,
})


custom_order = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
chart_data['Meses'] = pd.Categorical(chart_data['Meses'], categories=custom_order, ordered=True)


chart_data = chart_data.sort_values('Meses')

st.bar_chart(chart_data, x="Meses", y="Energia Mensual")
st.dataframe(chart_data)




