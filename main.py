# -*- coding: utf-8 -*-
import os
import datetime 
import streamlit as st
import pandas as pd
import numpy as np



with st.sidebar: 
    st.write('# Completar datos')
    N = st.slider('Cantidad de paneles', min_value=1,  max_value =1000, value=250, step=1) 
 
    Ppico = st.number_input('Pot. pico del panel (W)', min_value=0,  max_value =500, value=240, step=10) 
  
    kp = st.number_input('Coef. de Pot - Temp (1/°C)', min_value=-0.01,  max_value=0., value=-0.0044, step=0.0001, format='%.4f')
      
    eta = st.number_input('Rendimiento General (p.u.)', min_value=0.1,  max_value=1., value=0.97, step=0.0001, format='%.2f')
    
    
   
    
tab1, tab2, tab3 = st.tabs(['Generacion_FV', 'Tuplas', 'Grafico por mes'])
with tab1:
    
   col1, col2, col3 = st.columns(3, gap="large")

with col1:
   G = st.number_input('Irradiancia (W/m²)', min_value=0,  max_value =2000, value=1000) 

with col2:
   Tc = st.number_input('Temperatura Celda (°C)', min_value=-20.,  max_value =60., value=25., step=1., format='%.1f') 

with col3:
   st.write('Presione el boton')
   btn = st.button("Calcular", type="primary")
    
    
if btn:
    p = N * G/1000 * Ppico * (1 + kp * (Tc - 25)) * eta * 1e-3 #(KW)
    st.info(f'la potencia obtenidaes **{p: 2f} (W)**')
else:
    st.warning('debe ingresar los valores y presionar el boton')
        
    carpeta = os.path.dirname(__file__)
    ruta_excel = os.path.join(carpeta, 'Datos_climatologicos_Santa_Fe_2019.xlsx')
    df = pd.read_excel(ruta_excel, index_col=1)
    df['Potencia (KW)'] = N * df['Irradiancia (W/m²)']/1000 * Ppico * (1 + kp * (df['Temperatura (°C)'] - 25)) * eta * 1e-3 #(KW)
    #tabla_mayo = df.loc['2019-1', :]
    #st.dataframe(df)


    #st.line_chart(tabla_mayo, y = 'Temperatura (°C)')
    
        
with tab2:
   
    carpeta = os.path.dirname(__file__)
    ruta_excel = os.path.join(carpeta, 'Datos_climatologicos_Santa_Fe_2019.xlsx')
    df = pd.read_excel(ruta_excel, index_col=0)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    d1 = st.date_input("Ingrese la Primer Fecha", datetime.date(2019, 7, 6))

with col2:
    t1 = st.time_input("Ingrese la Primer Hora", datetime.time(0, 0))

with col3:
    d2 = st.date_input("Ingrese la Segunda Fecha", datetime.date(2019, 7, 8))

with col4:
    t2 = st.time_input("Ingrese la Segunda Hora", datetime.time(0, 0))


start_datetime = datetime.datetime.combine(d1, t1)

end_datetime = datetime.datetime.combine(d2, t2)


st.write("Column Names:", df.columns)


date_column_name = 'Fecha'  
if date_column_name not in df.columns:
    st.error(f"Column '{date_column_name}' not found in DataFrame.")
else:
   
    filtered_df = df[(df[date_column_name] >= start_datetime) & (df[date_column_name] <= end_datetime)]
    st.dataframe(filtered_df)
   
    chart_data = pd.DataFrame({
        "Fechas": filtered_df[date_column_name],
        "Temperatura": filtered_df['Temperatura (°C)'],
    })

 
    st.bar_chart(chart_data, x="Fechas", y="Temperatura")
   
with tab3:


    carpeta = os.path.dirname(__file__)


    ruta_excel = os.path.join(carpeta, 'Datos_climatologicos_Santa_Fe_2019.xlsx')


    df = pd.read_excel(ruta_excel, index_col=0)
    df['Potencia (KW)'] = N * df['Irradiancia (W/m²)']/1000 * Ppico * (1 + kp * (df['Temperatura (°C)'] - 25)) * eta * 1e-3 #(KW)

start_datetime = datetime.datetime.combine(d1, t1)


end_datetime = datetime.datetime.combine(d2, t2)


st.write("Nombre de las columnas:", df.columns)

date_column_name = 'Fecha'  
if date_column_name not in df.columns:
    st.error(f"Column '{date_column_name}' not found in DataFrame.")
else:
    
    filtro_df = df[(df[date_column_name] >= start_datetime) & (df[date_column_name] <= end_datetime)]
    st.dataframe(filtro_df)
    potencias_generadas = ['Potencia (KW)']
    fechas = []
    
    mu=2
    Gstd=1000
    Tr=25 
     
    Ncorr = N * (G / Gstd) * (1 + kp * ((Tc - Tr) / 100))

   
    Pmodelo = Ncorr * Ppico * (1 - mu * ((Tc - Tr) / 100)) * eta / 100

    potencias_generadas.append(Pmodelo)
    st.write("el valor es de : ", Ncorr)
    st.write("el valor es de : ", Pmodelo)
    st.write("el valor de las potencias es :", potencias_generadas, 'Potencia (KW)')
    
    chart_data = pd.DataFrame({
        "Fechas": filtro_df[date_column_name],
        "Potencia": filtro_df['Potencia (KW)'],
    })

    st.line_chart(chart_data, x="Fechas", y="Potencia")