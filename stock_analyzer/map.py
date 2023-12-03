import folium
import requests
import folium.plugins
import branca
import branca.colormap as cm


def nanFunc(feat, Dict):

    if Dict.get(feat["properties"]["name"].lower(), -1) != -1:
        return linear(Dict[feat["properties"]["name"].lower()])
    else:
        return "white"


linear = cm.linear.Spectral_07
step = cm.linear.Spectral_07.to_step(12)

m = folium.Map(tiles=folium.TileLayer(name="World Map", no_wrap=True),
               zoom_control=True,
               control_scale=True,
               zoom_start=20,
               max_zoom=20,
               )

geojson_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
).json()

Dict = {"france": .05, "usa": .2, "japan": .9}

geoJson1 = folium.GeoJson(geojson_data,
                          style_function=lambda feature: {
                              "fillColor": nanFunc(feature, Dict),
                              "color": "black",
                              "weight": 2,
                              "dashArray": "5, 5",
                              "nan_fill_color": "white",
                              "nan_fill_opacity": 0.4,
                          },
                          highlight_function=lambda feature: {
                              "color": "black",
                              "weight": 3,
                              "dashArray": "0, 0",
                          },
                          name="High",
                          highlight=True,
                          show=True,
                          zoom_on_click=True,
                          ).add_to(m)

geoJson2 = folium.GeoJson(geojson_data,
                          style_function=lambda feature: {
                              "fillColor": nanFunc(feature, Dict),
                              "color": "black",
                              "weight": 2,
                              "dashArray": "5, 5",
                              "nan_fill_color": "white",
                              "nan_fill_opacity": 0.4,
                          },
                          highlight_function=lambda feature: {
                              "color": "black",
                              "weight": 4,
                          },
                          name="Low",
                          highlight=True,
                          show=False,
                          zoom_on_click=True,
                          ).add_to(m)

geoJson3 = folium.GeoJson(geojson_data,
                          style_function=lambda feature: {
                              "fillColor": nanFunc(feature, Dict),
                              "color": "black",
                              "weight": 2,
                              "dashArray": "5, 5",
                              "nan_fill_color": "white",
                              "nan_fill_opacity": 0.4,
                          },
                          highlight_function=lambda feature: {
                              "color": "black",
                              "weight": 4,
                          },
                          name="Volatility",
                          highlight=True,
                          show=False,
                          zoom_on_click=True,
                          ).add_to(m)

geoJson4 = folium.GeoJson(geojson_data,
                          style_function=lambda feature: {
                              "fillColor": nanFunc(feature, Dict),
                              "color": "black",
                              "weight": 2,
                              "dashArray": "5, 5",
                              "nan_fill_color": "white",
                              "nan_fill_opacity": 0.4,
                          },
                          highlight_function=lambda feature: {
                              "color": "black",
                              "weight": 4,
                          },
                          name="Volume",
                          highlight=True,
                          show=False,
                          zoom_on_click=True,
                          ).add_to(m)

folium.LayerControl().add_to(m)

m.save("index.html")
