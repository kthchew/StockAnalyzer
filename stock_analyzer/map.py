import math

import requests
import folium.plugins
import branca.colormap as cm


class Map:
    def __init__(self, highDict, lowDict, volDict, feature):
        self.m = folium.Map(tiles=folium.TileLayer(name="World Map", no_wrap=True),
                            zoom_control=True,
                            control_scale=True,
                            zoom_start=20,
                            max_zoom=20,
                            )

        # loads all countries as features
        self.geojson_data = requests.get(
            "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
        ).json()

        # saves {county: value} dictionary for each metric
        self.highDict = highDict
        self.lowDict = lowDict
        self.volDict = volDict

        # establishes map layers for each metric
        if feature == 0:  # highs
            colormap = self.colormap(highDict)
            self.geoJson = folium.GeoJson(self.geojson_data,
                                          style_function=lambda feature: {
                                              "fillColor": self.nanFunc(feature, self.highDict, colormap),
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
        elif feature == 1:  # lows
            colormap = self.colormap(lowDict)
            self.geoJson = folium.GeoJson(self.geojson_data,
                                          style_function=lambda feature: {
                                              "fillColor": self.nanFunc(feature, self.lowDict, colormap),
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
                                          show=True,
                                          zoom_on_click=True,
                                          ).add_to(self.m)
            # self.addScale(self.lowDict)
        else:  # volumes
            colormap = self.colormap(volDict)
            self.geoJson = folium.GeoJson(self.geojson_data,
                                          style_function=lambda feature: {
                                              "fillColor": self.nanFunc(feature, self.volDict, colormap),
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
                                          show=True,
                                          zoom_on_click=True,
                                          ).add_to(self.m)

        self.m.save("index.html")

    def colormap(self, dicto: dict):
        maximum = max(dicto.values())
        minimum = min(dicto.values())
        colormap = cm.linear.RdYlGn_11.scale(math.log(minimum), math.log(maximum))
        unscaledColormap = cm.linear.RdYlGn_11.scale(minimum, maximum)
        unscaledColormap.caption = "Color Scale"
        unscaledColormap.add_to(self.m)
        return colormap

    # calculates the color of countries based on data from dictionaries
    def nanFunc(self, feat, dicto, colormap):
        temp = feat["properties"]["name"]
        if temp == "United States of America":
            temp = "usa"
        if dicto.get(temp.lower(), -1) != -1:
            return colormap(math.log(dicto.get(temp.lower())))
        else:
            return "#D3D3D3"
