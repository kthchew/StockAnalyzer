import folium
import requests
import random


# Maps low values to green and high values to red.
# We can change this to varying shades depending on how successful stocks are doing later
def my_color_function():
    if random.random() > .5:
        return "#ff0000"
    else:
        return "#008000"


m = folium.Map(tiles=folium.TileLayer(no_wrap=True),
               zoom_control=True,
               control_scale=True,
               zoom_start=20,
               max_zoom=20,
               )

geojson_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
).json()

geoJson = folium.GeoJson(geojson_data,
                         style_function=lambda feature: {
                             "fillColor": my_color_function(),
                             "color": "black",
                             "weight": 2,
                             "dashArray": "5, 5",
                         },
                         name="Stock Analysis",
                         legend_name="Stonks",
                         highlight=True,
                         show=True,
                         zoom_on_click=True,
                         ).add_to(m)

folium.LayerControl().add_to(m)

m.save("index.html")
