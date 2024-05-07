from lib import OpenSSL
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from shapely.wkt import loads
from shapely.geometry import Point
from branca.colormap import linear
import requests
from io import BytesIO
import math
from PIL import Image

def num2deg(xtile, ytile, zoom):
    n = 1 << zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg

lat1, lon1 = num2deg(7, 3, 3)
lat2, lon2 = num2deg(8, 4, 3)
extent0 = (min(lon1, lon2), max(lon1, lon2), min(lat1, lat2), max(lat1, lat2))

lat1, lon1 = num2deg(7, 2, 3)
lat2, lon2 = num2deg(8, 3, 3)
extent1 = (min(lon1, lon2), max(lon1, lon2), min(lat1, lat2), max(lat1, lat2))

lat1, lon1 = num2deg(6, 2, 3)
lat2, lon2 = num2deg(7, 3, 3)
extent2 = (min(lon1, lon2), max(lon1, lon2), min(lat1, lat2), max(lat1, lat2))

lat1, lon1 = num2deg(6, 3, 3)
lat2, lon2 = num2deg(7, 4, 3)
extent3 = (min(lon1, lon2), max(lon1, lon2), min(lat1, lat2), max(lat1, lat2))

data = gpd.read_file('./data/gadm41_JPN_0.shx')
d0 = data.iloc[0, 0]

image_urls = [
    'https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/7/3.jpg',
    'https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/7/2.jpg',
    'https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/6/2.jpg',
    'https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/6/3.jpg'
]

himawari_images = []

for url in image_urls:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    himawari_images.append(img)

def main():
    gdf = gpd.GeoDataFrame(geometry=[d0])
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, alpha=0.5)

    # Set the extent of the plot to cover your focus area
    ax.set_xlim(125, 150)
    ax.set_ylim(25, 50)
    
    for img, extent in zip(himawari_images, [extent0, extent1, extent2, extent3]):
        ax.imshow(np.array(img), extent=extent, alpha=0.8)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
