import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

df = pd.read_csv('res/pubs_cleaned.csv')

postal_codes = df['postcode'].unique()
local_authorities = df['local_authority'].unique()


def filter(option):
    if option in postal_codes:
        return df[df['postcode'] == option]
    elif option in local_authorities:
        return df[df['local_authority'] == option]


def create_map(data):
    def_loc = [data['latitude'].median(), data['longitude'].median() + 0.25]
    def_zoom = 10
    m = folium.Map(location=def_loc, zoom_start=def_zoom)
    for index, row in data.iterrows():
        folium.Marker(
            location = [row['latitude'], row['longitude']],
            popup = row['name']
        ).add_to(m)
    return m


st.title('Pub Locations')
option = st.selectbox('Postal Code or Local Authority', list(local_authorities) + list(postal_codes))
data = filter(option)
st.write('Number of pubs found:', len(data))
folium_static(create_map(data))
