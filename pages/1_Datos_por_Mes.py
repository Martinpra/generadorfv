import os
import datetime 
import streamlit as st
import pandas as pd
import numpy as np
from datetime import time


with st.sidebar: 
    st.title('completar los datos para calcular la potencia')
    
    N = st.slider('Cantidad de paneles', min_value=1,  max_value =1000, value=250, step=1) 
 
    Ppico = st.number_input('Pot. pico del panel (W)', min_value=0,  max_value =500, value=240, step=10) 
  
    kp = st.number_input('Coef. de Pot - Temp (1/°C)', min_value=-0.01,  max_value=0., value=-0.0044, step=0.0001, format='%.4f')
      
    eta = st.number_input('Rendimiento General (p.u.)', min_value=0.1,  max_value=1., value=0.97, step=0.01, format='%.2f')


st.title('Realizar Graficos, seleccionando el mes que desea ver sus datos')
carpeta = os.path.dirname(__file__)
ruta_excel = os.path.join(carpeta, 'Datos_climatologicos_Santa_Fe_2019.xlsx')
df = pd.read_excel(ruta_excel, index_col=1)

month_selected = st.number_input("Select a month", min_value=1, max_value=12, step=1, value=1)
year_selected = st.number_input("Select a year", min_value=df.index.year.min(), max_value=df.index.year.max(), step=1, value=2019)

if month_selected and year_selected:
   
    df_selected_month = df[(df.index.month == month_selected) & (df.index.year == int(year_selected))]

    df_selected_month['Potencia (KW)'] = N * df_selected_month['Irradiancia (W/m²)'] / 1000 * Ppico * (
            1 + kp * (df_selected_month['Temperatura (°C)'] - 25)) * eta * 1e-3  # (KW)

    st.dataframe(df_selected_month)
    st.line_chart(df_selected_month[['Temperatura (°C)', 'Irradiancia (W/m²)', 'Potencia (KW)']])
else:
    st.dataframe(df)