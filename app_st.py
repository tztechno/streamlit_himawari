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
import cv2
import requests
from io import BytesIO
import math

data = gpd.read_file('./data/gadm41_JPN_0.shx')
d0=data.iloc[0,0]

image_url0='https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/7/3.jpg'
image_url1='https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/7/2.jpg'
image_url2='https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/6/2.jpg'
image_url3='https://www.jma.go.jp/bosai/himawari/data/satimg/20240505000000/fd/20240505000000/B03/ALBD/3/6/3.jpg'

def num2deg(xtile, ytile, zoom):
    n = 1 << zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg

lat1,lon1=num2deg(7,3,3)
lat2,lon2=num2deg(8,4,3)
extent0=(min(lon1,lon2),max(lon1,lon2),min(lat1,lat2),max(lat1,lat2))

lat1,lon1=num2deg(7,2,3)
lat2,lon2=num2deg(8,3,3)
extent1=(min(lon1,lon2),max(lon1,lon2),min(lat1,lat2),max(lat1,lat2))

lat1,lon1=num2deg(6,2,3)
lat2,lon2=num2deg(7,3,3)
extent2=(min(lon1,lon2),max(lon1,lon2),min(lat1,lat2),max(lat1,lat2))

lat1,lon1=num2deg(6,3,3)
lat2,lon2=num2deg(7,4,3)
extent3=(min(lon1,lon2),max(lon1,lon2),min(lat1,lat2),max(lat1,lat2))

response = requests.get(image_url0, stream=True)
img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
himawari_img0 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

response = requests.get(image_url1, stream=True)
img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
himawari_img1 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

response = requests.get(image_url2, stream=True)
img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
himawari_img2 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

response = requests.get(image_url3, stream=True)
img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
himawari_img3 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)


gdf = gpd.GeoDataFrame(geometry=[d0])
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, alpha=0.5)

def main():
    data = gpd.read_file('./data/gadm41_JPN_0.shx')
    d0 = data.iloc[0, 0]

    # Your image URL and other code...

    gdf = gpd.GeoDataFrame(geometry=[d0])
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, alpha=0.5)

    # Set the extent of the plot to cover your focus area
    ax.set_xlim(125, 150)
    ax.set_ylim(25, 50)
    ax.imshow(himawari_img0, extent=extent0, alpha=0.8)
    ax.imshow(himawari_img1, extent=extent1, alpha=0.8)
    ax.imshow(himawari_img2, extent=extent2, alpha=0.8)
    ax.imshow(himawari_img3, extent=extent3, alpha=0.8)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
