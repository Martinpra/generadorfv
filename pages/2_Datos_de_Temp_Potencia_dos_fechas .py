import os
import datetime 
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time

with st.sidebar: 
    st.write('# Completar datos Pag. 2')
    
    N = st.slider('Cantidad de paneles', min_value=1,  max_value =1000, value=250, step=1) 
 
    Ppico = st.number_input('Pot. pico del panel (W)', min_value=0,  max_value =500, value=240, step=10) 
  
    kp = st.number_input('Coef. de Pot - Temp (1/°C)', min_value=-0.01,  max_value=0., value=-0.0044, step=0.0001, format='%.4f')
      
    eta = st.number_input('Rendimiento General (p.u.)', min_value=0.1,  max_value=1., value=0.97, step=0.01, format='%.2f')
    
    valor = st.number_input('sumar temperatura', min_value=1,  max_value =1000, value=250, step=1) 
    
st.title('Grafico de temperatura y potencia seleccionando dos fechas')
carpeta = os.path.dirname(__file__)
ruta_excel = os.path.join(carpeta, 'Datos_climatologicos_Santa_Fe_2019.xlsx')
df = pd.read_excel(ruta_excel, index_col=0)
df['Potencia (KW)'] = N * df['Irradiancia (W/m²)']/1000 * Ppico * (1 + kp * (df['Temperatura (°C)'] - 25)) * eta * 1e-3 #(KW)
df['Incremento'] = (valor* df['Temperatura (°C)'])/100 + + df['Temperatura (°C)']
df['Potencia1 (KW)'] = N * df['Irradiancia (W/m²)']/1000 * Ppico * (1 + kp * (df['Incremento'] - 25)) * eta * 1e-3 #(KW) +
col1, col2, col3, col4 = st.columns(4, gap="large")
intervalo = 10
opciones_tiempo = [time(h, m) for h in range(24) for m in range(0, 60, intervalo)]
with col1:
     key_1_date = "first_date"
     fecha_seleccionada_1 = st.sidebar.date_input("Seleccione la Fecha", datetime.today().replace(year=2019).date(), key=key_1_date)

with col2:
     key_1_time = "first_time"
     hora_inicio_1 = st.sidebar.selectbox("Seleccione la Hora de Inicio", opciones_tiempo, format_func=lambda x: x.strftime("%H:%M"), key=key_1_time)

with col3:
     key_2_date = "second_date"
     fecha_seleccionada_2 = st.sidebar.date_input("Seleccione la Fecha", datetime.today().replace(year=2019).date(), key=key_2_date)

with col4:
     key_2_time = "second_time"
     hora_inicio_2 = st.sidebar.selectbox("Seleccione la Hora de Inicio", opciones_tiempo, format_func=lambda x: x.strftime("%H:%M"), key=key_2_time)
     
fecha_hora_inicio_1 = datetime.combine(fecha_seleccionada_1, hora_inicio_1)

    
fecha_hora_inicio_2 = datetime.combine(fecha_seleccionada_2, hora_inicio_2)

st.write("Nombre de Columnas:", df.columns)


date_column_name = 'Fecha'  
if date_column_name not in df.columns:
    st.error(f"Column '{date_column_name}' not found in DataFrame.")
else:
    
    filtered_df = df[(df[date_column_name] >= fecha_hora_inicio_1) & (df[date_column_name] <= fecha_hora_inicio_2)]
    st.dataframe(filtered_df)
   
    chart_data = pd.DataFrame({
        "Fechas": filtered_df[date_column_name],
        "Temperatura": filtered_df['Temperatura (°C)'],
    })

  
    st.bar_chart(chart_data, x="Fechas", y="Temperatura")

    
    chart_data = pd.DataFrame({
        "Fechas": filtered_df[date_column_name],
        "Potencia": filtered_df['Potencia (KW)'],
    })

    st.line_chart(chart_data, x="Fechas", y="Potencia")