import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

df = pd.read_csv('res/pubs_cleaned.csv')

def distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = np.deg2rad(lat2-lat1)
    d_lon = np.deg2rad(lon2-lon1)
    a = np.sin(d_lat/2) * np.sin(d_lat/2) + np.cos(np.deg2rad(lat1)) \
        * np.cos(np.deg2rad(lat2)) * np.sin(d_lon/2) * np.sin(d_lon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d

def find_nearest(df, lat, lon, k):
    distances = []
    for index, row in df.iterrows():
        dist = distance(lat, lon, row['latitude'], row['longitude'])
        distances.append((index, dist))
    distances.sort(key=lambda x: x[1])
    nearest = distances[:k]
    return nearest

st.title('Nearest Pubs')

lat = st.number_input('Latitude:', value=df['latitude'].mean())
lon = st.number_input('Longitude:', value=df['longitude'].mean())
k = st.slider('Number of pubs', min_value=1, max_value=100, value=5)

nearest = find_nearest(df, lat, lon, k)
nearest_indices = [x[0] for x in nearest]

m = folium.Map(location=[lat, lon + 0.05], zoom_start=12)

for index in nearest_indices:
    row = df.iloc[index]
    marker = folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name'])
    marker.add_to(m)
    folium.Marker(location=[lat, lon], popup='You', icon = folium.Icon(color='red')).add_to(m)

folium_static(m)
