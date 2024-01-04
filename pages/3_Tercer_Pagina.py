import streamlit as st
import pandas as pd
from datetime import time

class DatosClimatologicos:
    def __init__(self, ruta_archivo):
        self.df = pd.read_excel(ruta_archivo)

    def buscar_irradiancia_temperatura(self, fecha_hora_str):
        try:
            fila = self.df.loc[self.df['Fecha'] == fecha_hora_str, ['Temperatura (°C)', 'Irradiancia (W/m²)']].iloc[0]
            temperatura = fila['Temperatura (°C)']
            irradiancia = fila['Irradiancia (W/m²)']
            return irradiancia, temperatura
        except IndexError:
            print(f'No se encontraron datos de temperatura para {fecha_hora_str}')


ruta_archivo = 'Datos_climatologicos_Santa_Fe_2019.xlsx'
datos_climatologicos = DatosClimatologicos(ruta_archivo)

st.title("Consulta de Datos Climatológicos")

intervalo = 10
opciones_tiempo = [time(h, m) for h in range(24) for m in range(0, 60, intervalo)]


fecha = st.date_input("Seleccione la fecha", pd.to_datetime('2019-07-20'))
hora = st.selectbox("Seleccione la Hora", opciones_tiempo, format_func=lambda x: x.strftime("%H:%M"))


fecha_hora_str = f'{fecha.strftime("%d-%m-%Y")} {hora.strftime("%H:%M")}'


resultado = datos_climatologicos.buscar_irradiancia_temperatura(fecha_hora_str)


if resultado:
    irradiancia, temperatura = resultado
    st.info(f"Irradiancia: {irradiancia} W/m²")
    st.info(f"Temperatura: {temperatura} °C")
else:
    st.warning(f"No se encontraron datos para la fecha y hora seleccionadas.")

