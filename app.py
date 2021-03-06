import streamlit as st
from streamlit_folium import folium_static

'''
# TaxiFareModel :taxi:
'''

st.markdown('''
## Create your journey below
''')

import datetime

'### Journey Date :calendar:'
d = st.date_input(
    "",
    datetime.date(2019, 7, 6))

'### Journey Time :watch:'
t = st.time_input('', datetime.time(8, 45))

dt = f'{d} {t} UTC'

'### Pickup Longitude'
pickup_long = st.number_input('')
st.markdown("""
    #### Unsure about coordinates? Click [here](https://www.latlong.net/) for help!
""")
'### Pickup Latitude'
pickup_lat = st.number_input(' ')
'### Dropoff Longitude'
dropoff_long = st.number_input('  ')
'### Dropoff Latitude'
dropoff_lat = st.number_input('   ')
'### Number of Passengers'
passengers = st.number_input('    ',min_value=1, max_value=8, step=1)


from PIL import Image
image = Image.open('ny_map.PNG')
st.image(image, use_column_width=True)

import folium

m = folium.Map(location=[pickup_lat, pickup_long])
folium.Marker([pickup_lat, pickup_long], popup='Pickup location').add_to(m)
folium.Marker([dropoff_lat, dropoff_long], popup='Dropoff location').add_to(m)

folium_static(m)

import requests

#url = 'http://taxifare.lewagon.ai/predict_fare/'
url = 'https://wagon-exo-z7fyqqvx3a-ew.a.run.app/predict_fare'

params = dict(
    key='2012-10-06 12:10:20.0000001',
    pickup_datetime=dt,
    pickup_longitude=pickup_long,
    pickup_latitude=pickup_lat,
    dropoff_longitude=dropoff_long,
    dropoff_latitude=dropoff_lat,
    passenger_count=passengers)

response = requests.get(url, params=params)

if response.status_code == 200:
    response = response.json()
else:
    response = requests.get(url, params=params).json()

prediction = response['pred']

f'## Fare Estimate: ${round(prediction,2)}'