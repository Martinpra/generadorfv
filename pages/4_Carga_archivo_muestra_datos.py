import streamlit as st
import pandas as pd
import datetime
from datetime import datetime, time

class DatosClimatologicos:
    def __init__(self):
        self.df = None

    def cargar_datos(self, ruta_archivo):
        self.df = pd.read_excel(ruta_archivo)

    def buscar_irradiancia_temperatura(self, tupla):
        fecha_hora_str = f'{tupla[0]:02d}-{tupla[1]:02d}-2019 {tupla[2]:02d}:{tupla[3]:02d}'
        try:
            fila = self.df.loc[self.df['Fecha'] == fecha_hora_str, ['Temperatura (°C)', 'Irradiancia (W/m²)']].iloc[0]
            temperatura = fila['Temperatura (°C)']
            irradiancia = fila['Irradiancia (W/m²)']
            return irradiancia, temperatura
        except IndexError:
            st.warning(f'No se encontraron datos de temperatura para {fecha_hora_str}')

    def buscar_irradiancia_temperatura_rango(self, tupla_inicio, tupla_fin):
        fecha_hora1_str = f'{tupla_inicio[0]:02d}-{tupla_inicio[1]:02d}-2019 {tupla_inicio[2]:02d}:{tupla_inicio[3]:02d}'
        fecha_hora2_str = f'{tupla_fin[0]:02d}-{tupla_fin[1]:02d}-2019 {tupla_fin[2]:02d}:{tupla_fin[3]:02d}'
        try:
            datos_rango = self.df[(self.df['Fecha'] >= fecha_hora1_str) & (self.df['Fecha'] <= fecha_hora2_str)]
            resultados = []
            for _, fila in datos_rango.iterrows():
                temperatura = fila['Temperatura (°C)']
                irradiancia = fila['Irradiancia (W/m²)']
                tupla_irrad_temp = (irradiancia, temperatura)
                resultados.append(tupla_irrad_temp)

            return resultados
        except IndexError:
            st.warning('No se encontraron datos en el rango de fechas proporcionado')


st.title("Consulta de Datos Climatológicos")
uploaded_file = st.sidebar.file_uploader("Cargar archivo de datos", type=["xlsx", "xls"])

if uploaded_file is not None:
    
        datos_climatologicos = DatosClimatologicos()
    

        datos_climatologicos.cargar_datos(uploaded_file)

    
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

    
            st.write("Nombre de Columnas:", datos_climatologicos.df.columns)

  
        fecha_column_name = 'Fecha' 
        if fecha_column_name not in datos_climatologicos.df.columns:
            st.error(f"Columna '{fecha_column_name}' no encontrada en el DataFrame.")
        else:
        
            filtered_df = datos_climatologicos.df[(datos_climatologicos.df[fecha_column_name] >= fecha_hora_inicio_1) & (datos_climatologicos.df[fecha_column_name] <= fecha_hora_inicio_2)]

        
    
        st.title("Fecha Específica")
        tupla_fecha = start_datetime = datetime.combine(fecha_seleccionada_1, hora_inicio_1)
        resultado_fecha = datos_climatologicos.buscar_irradiancia_temperatura((tupla_fecha.day, tupla_fecha.month, tupla_fecha.hour, tupla_fecha.minute))
        st.write("Resultados para la Fecha Específica")
        if resultado_fecha:
            irradiancia, temperatura = resultado_fecha
            st.write(f"Irradiancia: {irradiancia} W/m²")
            st.write(f"Temperatura: {temperatura} °C")

    
        st.title("Rango de Fechas")
        st.dataframe(filtered_df)


