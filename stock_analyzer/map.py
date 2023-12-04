import requests
import folium.plugins
import branca.colormap as cm


class Map:
    def __init__(self, dicto):
        self.linear = cm.linear.Spectral_07
        self.step = cm.linear.Spectral_07.to_step(12)
        self.m = folium.Map(tiles=folium.TileLayer(name="World Map", no_wrap=True),
                            zoom_control=True,
                            control_scale=True,
                            zoom_start=20,
                            max_zoom=20,
                            )
        self.geojson_data = requests.get(
            "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
        ).json()
        self.dict = dicto
        self.geoJson1 = folium.GeoJson(self.geojson_data,
                                       style_function=lambda feature: {
                                           "fillColor": self.nanFunc(feature, self.dicto),
                                           "fillOpacity": 0.5,
                                           "color": "black",
                                           "weight": 2,
                                           "dashArray": "5, 5",
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
                                       ).add_to(self.m)

        self.geoJson2 = folium.GeoJson(self.geojson_data,
                                       style_function=lambda feature: {
                                           "fillColor": self.nanFunc(feature, self.dicto),
                                           "fillOpacity": 0.5,
                                           "color": "black",
                                           "weight": 2,
                                           "dashArray": "5, 5",
                                       },
                                       highlight_function=lambda feature: {
                                           "color": "black",
                                           "weight": 4,
                                       },
                                       name="Low",
                                       highlight=True,
                                       show=False,
                                       zoom_on_click=True,
                                       ).add_to(self.m)

        self.geoJson3 = folium.GeoJson(self.geojson_data,
                                       style_function=lambda feature: {
                                           "fillColor": self.nanFunc(feature, self.dicto),
                                           "fillOpacity": 0.5,
                                           "color": "black",
                                           "weight": 2,
                                           "dashArray": "5, 5",
                                       },
                                       highlight_function=lambda feature: {
                                           "color": "black",
                                           "weight": 4,
                                       },
                                       name="Volatility",
                                       highlight=True,
                                       show=False,
                                       zoom_on_click=True,
                                       ).add_to(self.m)

        self.geoJson4 = folium.GeoJson(self.geojson_data,
                                       style_function=lambda feature: {
                                           "fillColor": self.nanFunc(feature, self.dicto),
                                           "fillOpacity": 0.5,
                                           "color": "black",
                                           "weight": 2,
                                           "dashArray": "5, 5",
                                       },
                                       highlight_function=lambda feature: {
                                           "color": "black",
                                           "weight": 4,
                                       },
                                       name="Volume",
                                       highlight=True,
                                       show=False,
                                       zoom_on_click=True,
                                       ).add_to(self.m)

        folium.LayerControl().add_to(self.m)

        self.m.save("index.html")

    def nanFunc(self, feat):

        if self.dicto.get(feat["properties"]["name"].lower(), -1) != -1:
            return self.linear(self.dicto.get(feat["properties"]["name"].lower()))
        else:
            return "#D3D3D3"
