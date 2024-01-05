import random
import streamlit as st
import folium
from streamlit_folium import folium_static
# import streamlit.components.v1 as components
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import warnings
warnings.filterwarnings('ignore')

# Define city and amenity options
cities = ['Washington, District of Columbia, USA',
          'New York City, New York, USA']

amenities = ['bar', 'ice_cream', 'restaurant']

# Define city coordinates
DC_COORDS = (38.9072, -77.0369)
NYC_COORDS = (40.7128, -74.0060)


# Streamlit app
def main():
    # Set Streamlit page title
    st.set_page_config(page_title='Geo-spatial Web Application')

    # Render Streamlit app title
    st.title('Geo-spatial Web Application')

    # Select city and amenity
    city = st.selectbox('Which city would you like to focus on?', cities)
    amenity = st.selectbox('What would you like to find?', amenities)

    # Get city coordinates
    areaID = Nominatim().query(city).areaId()

    # Get amenity data
    query = overpassQueryBuilder(
        area=areaID, elementType='node', selector=f'"amenity"="{amenity}"', out='body')
    result = Overpass().query(query)

    # Create Folium map
    if city == cities[0]:
        m = folium.Map(location=DC_COORDS, zoom_start=12)
    else:
        m = folium.Map(location=NYC_COORDS, zoom_start=12)

    # Randomly Downsample to 5% of restaurants for NYC only
    if city == cities[1] and amenity == amenities[2]:

        for node in result.nodes()[0:600]:
            # Get the information about the restaurant
            name = node.tag('name')
            address = node.tag('addr:full')
            longitude = node.lon()
            latitude = node.lat()
            opening_hours = node.tag('opening_hours')
            phone = node.tag('phone')

            # Create a popup with the restaurant information
            popup_html = f'<b>{name}</b>'
            if address:
                popup_html += f'<br>{address}'
            popup_html += f'<br>Longitude: {longitude}, Latitude: {latitude}'
            if opening_hours:
                popup_html += f'<br>Opening Hours: {opening_hours}'
            if phone:
                popup_html += f'<br>Phone: {phone}'

            # Add a marker for the amenity to the map
            marker = folium.Marker(
                location=[latitude, longitude], tooltip=popup_html)
            marker.add_to(m)

    else:

        for node in result.nodes():
            # Get the information about the restaurant
            name = node.tag('name')
            address = node.tag('addr:full')
            longitude = node.lon()
            latitude = node.lat()
            opening_hours = node.tag('opening_hours')
            phone = node.tag('phone')

            # Create a popup with the restaurant information
            popup_html = f'<b>{name}</b>'
            if address:
                popup_html += f'<br>{address}'
            popup_html += f'<br>Longitude: {longitude}, Latitude: {latitude}'
            if opening_hours:
                popup_html += f'<br>Opening Hours: {opening_hours}'
            if phone:
                popup_html += f'<br>Phone: {phone}'

            # Add a marker for the amenity to the map
            marker = folium.Marker(
                location=[latitude, longitude], tooltip=popup_html)
            marker.add_to(m)

    # call to render Folium map in Streamlit
    # output of city and amenity selection
    st.write('User Inout (city): ', city)
    st.write('User Input (amenity): ', amenity)
    folium_static(m)


if __name__ == '__main__':
    main()
