## Repository for article "A Data Driven Approach to Study the Social and Political Statuses of Urban Communities in Kunming"

It includes:

1. Data collection for Gaode, Baidu, Tencent, and Google POIs
2. Data collection for Tencent street view and Baidu panorama images
3. Data collection for geotagged Weibo posts (which Sina deprecated in 2017)
4. Coordinate System transformation from BD09 (Baidu), GCJ02 (国测局坐标系), to WGS84
5. Sklean to classify land uses
6. Keras to classify street images

# Getting Started
Data collections are provided for POI collections, which requires API keys. 

Classification algorithms do not require other files 

# Prerequisites
Python 2.X for data collection
Python 3.X for classification
API keys for Gaode, Baidu, Tencent, and Google
PostgreSQL and PostGIS are used in some data collections

# License
This project is licensed under the MIT License
