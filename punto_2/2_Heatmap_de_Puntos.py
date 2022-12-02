import streamlit as st

import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt

# Se importan funcionalidades desde librería propia
from utils import atrac_data

# Obtener datos desde cache
data_puntos = atrac_data()

# Generar listado de ATRACTIVOS ordenados
atractivos_puntos = data_puntos["NOMBRE"].sort_values().unique()

# Generar listado de regiones ordenadas
region_puntos = data_puntos["REGION"].sort_values().unique()

with st.sidebar:
  st.write("##### Filtros de Información")
  st.write("---")

  # Multiselector de regiones
  region_sel = st.multiselect(
    label="Regiones con atractivos turísticos",
    options=region_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not region_sel:
    region_sel = region_puntos.tolist()

  # Multiselector de atractivos turisticos
  atractivo_sel = st.multiselect(
    label="Atractivos turisticos",
    options=atractivos_puntos,
    default=atractivos_puntos
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not atractivo_sel:
    atractivo_sel = atractivos_puntos.tolist()


col_bar, col_pie, col_line = st.columns(3, gap="small")

group_region = data_puntos.groupby(["TIPO"]).size()
# Se ordenan de mayor a menor, gracias al uso del parámetros "ascending=False"
group_region.sort_values(axis="index", ascending=False, inplace=True)

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"


with col_bar:
  bar = plt.figure()
  group_comuna.plot.bar(
    title="Cantidad de atractivos turísticos por tipo",
    label="Total de atractivos",
    xlabel="Tipo",
    ylabel="Atractivos turísticos",
    color="lightblue",
    grid=True,
  ).plot()
  st.pyplot(bar)

with col_pie:
  pie = plt.figure()
  group_comuna.plot.pie(
    y="index",
    title="Cantidad de atractivos turísticos por tipo",
    legend=None,
    autopct=formato_porciento
  ).plot()
  st.pyplot(pie)

with col_line:
  line = plt.figure()
  group_comuna.plot.line(
    title="Cantidad de atractivos turísticos por tipo",
    label="Total de atractivos",
    xlabel="Tipo",
    ylabel="Atractivos turísticos",
    color="lightblue",
    grid=True
  ).plot()
  st.pyplot(line)

# Aplicar Filtros
atrac_data = data_puntos.query("NOMBRE==@atractivo_sel and REGION==@region_sel ")

if atrac_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  avg_x = np.median(atrac_data["PUNTO_X"])
  avg_y = np.median(atrac_data["PUNTO_Y"])

  puntos_mapa = pdk.Deck(
      map_style=None,
      initial_view_state=pdk.ViewState(
          latitude=avg_x,
          longitude=avg_y,
          zoom=10,
          min_zoom=10,
          max_zoom=15,
          pitch=20,
      ),
      layers=[
        pdk.Layer(
          "HeatmapLayer",
          data=atrac_data,
          pickable=True,
          auto_highlight=True,
          get_position='[PUNTO_X, PUNTO_Y]',
          opacity=0.6,
        )      
      ],
      tooltip={
        "html": "<b>Nombre: </b> {NOMBRE} <br /> "
                "<b>Dirección: </b> {DIRECCION} <br /> "
                "<b>Comuna: </b> {COMUNA} <br /> "
                "<b>Región: </b> {REGION} <br /> "
                "<b>Tipo: </b> {TIPO} <br /> "
                "<b>Georeferencia (Lat, Lng): </b>[{PUNTO_X}, {PUNTO_Y}] <br /> ",
        "style": {
          "backgroundColor": "steelblue",
          "color": "white"
        }
      }
  )

  st.write(puntos_mapa)

