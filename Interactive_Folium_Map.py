"""
import piplite
await piplite.install(['folium'])
await piplite.install(['pandas'])
"""

import folium
import pandas as pd
# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon


from js import fetch
import io
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
resp = await fetch(URL)
spacex_csv_file = io.BytesIO((await resp.arrayBuffer()).to_py())
spacex_df=pd.read_csv(spacex_csv_file)

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first() #return only first occurence of unique elements
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
#in case want rename something
launch_sites_df.rename(columns={'Launch Site': 'LaunchSite'}, inplace=True)


#NasaMap
#create folium map
nasa_coordinate = [29.559684888503615, -95.0830971930759] #centre
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)
# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)


#add marker (spaceX)
# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
incidents = folium.map.FeatureGroup()

for lat, lng, in zip(launch_sites_df.Lat, launch_sites_df.Long):
    incidents.add_child(
        folium.vector_layers.CircleMarker(
            [lat, lng],
            radius=5, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )
# add pop-up text to each marker on the map
latitudes = list(launch_sites_df.Lat)
longitudes = list(launch_sites_df.Long)
#create labelss list
labelss = []
for i in launch_sites_df['Launch Site']:
    labelss.append(i)

labels = list(labelss)
for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(site_map)    
# add incidents to map
site_map.add_child(incidents)
# show map
site_map



#make clusters (need frequency thus original spacex_df)
#label
label2 = []
for i in spacex_df['Launch Site']:
    label2.append(i)
#color for each class
# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
color_list = []
for i in spacex_df['class']:
    if (i==0):
        color_list.append('red')
    else:
        color_list.append('green')
spacex_df['marker_color'] = color_list
#make clusters
from folium import plugins
# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(site_map)
# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, color_s in zip(spacex_df.Lat, spacex_df.Long, label2, color_list):
    folium.Marker(
        location=[lat, lng],
        icon=folium.Icon(color=color_s), #no specified icon, thus default blue pin icon is used
        popup=label,
    ).add_to(incidents)
#show map
site_map





# mouse position, when you hover your mouse over the map, it will show coordinate
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
site_map.add_child(mouse_position)
#show map
site_map


#calculate distance function
from math import sin, cos, sqrt, atan2, radians
def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


#label distance and [new coordinates (using mouse position)]
#find distance and coordinates
l_lat = 28.563197
l_long = -80.576820
c_lat = 28.56289
c_long = -80.56783
distance_coastline = calculate_distance(l_lat, l_long, c_lat, c_long)
coastline_coords = [c_lat, c_long]  
launch_site_coords = [l_lat, l_long]  
#distance marker (add label '0.88km' onto the line)
distance_marker = folium.Marker(
    [c_lat, c_long],
    icon = DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
            )
)
#add the line onto the map
locations = [coastline_coords, launch_site_coords]
lines = folium.PolyLine(locations=locations, weight=1)
#add to the map
#'site_map.add_child(lines)' and 'lines.add_to(site_map)' are the same
site_map.add_child(lines)
site_map.add_child(distance_marker)

