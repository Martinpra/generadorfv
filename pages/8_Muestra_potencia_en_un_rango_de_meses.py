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
    st.write('# Completar datos Pag. 8')
    
    N = st.slider('Cantidad de paneles', min_value=1,  max_value=1000, value=250, step=1) 
    Ppico = st.number_input('Pot. pico del panel (W)', min_value=0,  max_value=500, value=240, step=10) 
    kp = st.number_input('Coef. de Pot - Temp (1/°C)', min_value=-0.01,  max_value=0., value=-0.0044, step=0.0001, format='%.4f')
    eta = st.number_input('Rendimiento General (p.u.)', min_value=0.1,  max_value=1., value=0.97, step=0.01, format='%.2f')

   
    selected_months = st.slider('Seleccione los meses que desea', min_value=1, max_value=12, value=(1, 12), step=1)


df['FechaHora'] = pd.to_datetime(df['Fecha'])
df['Mes'] = df['FechaHora'].dt.month

filtered_df = df[df['Mes'].between(selected_months[0], selected_months[1])]


potencias_mensuales = []
for mes in range(selected_months[0], selected_months[1] + 1):
    filtro_mes = filtered_df['Mes'] == mes
    df_mes = filtered_df[filtro_mes]
    
    pot_media_mes = df_mes['Irradiancia (W/m²)'].mean()
    potencia_mensual = N * Ppico * eta * (1 + kp * (df_mes['Temperatura (°C)'].mean() - 25))
    potencias_mensuales.append(potencia_mensual)


chart_data = pd.DataFrame({
    "Meses": [datetime(2000, mes, 1).strftime('%b') for mes in range(selected_months[0], selected_months[1] + 1)],
    "Potencia Mensual": potencias_mensuales,
})


chart_data['Meses'] = pd.Categorical(chart_data['Meses'], categories=[datetime(2000, i, 1).strftime('%b') for i in range(1, 13)], ordered=True)

chart_data = chart_data.sort_values('Meses')


st.bar_chart(chart_data, x="Meses", y="Potencia Mensual")
st.dataframe(chart_data)
