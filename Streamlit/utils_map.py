import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
from streamlit_folium import st_folium
import folium
import streamlit as st

os.environ['SHAPE_RESTORE_SHX'] = 'YES'

def map_df(filtered_df, shapefile_path):
    polygon_gdf = gpd.read_file(shapefile_path)
    if polygon_gdf.crs is None:
        polygon_gdf.set_crs(epsg=4326, inplace=True)

    all_data = filtered_df[['url_id', 'location', 'gender']]
    loc_dir_unique = all_data.drop_duplicates(subset=['url_id'])
    loc_dir = loc_dir_unique.dropna(subset=['gender'])
    loc_df = loc_dir.reset_index(drop=True)
    loc_df[['latitude', 'longitude']] = pd.DataFrame(loc_df['location'].tolist(), index=loc_df.index)
    loc_df['geometry'] = loc_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
    loc_gdf = gpd.GeoDataFrame(loc_df, geometry='geometry')
    loc_gdf.set_crs(polygon_gdf.crs, inplace=True)

    joined_gdf = gpd.sjoin(loc_gdf, polygon_gdf, predicate='within')
    women_gdf = joined_gdf[joined_gdf['gender'] == 'Female']
    men_gdf = joined_gdf[joined_gdf['gender'] == 'Male']
    women_counts = women_gdf.groupby('index_right').size()
    men_counts = men_gdf.groupby('index_right').size()
    polygon_gdf['women_count'] = polygon_gdf.index.map(women_counts).fillna(0).astype(int)
    polygon_gdf['men_count'] = polygon_gdf.index.map(men_counts).fillna(0).astype(int)
    polygon_gdf['women_perc'] = ((polygon_gdf['women_count'] / (polygon_gdf['women_count'] + polygon_gdf['men_count'])) * 100).round()
    polygon_gdf['point_count'] = polygon_gdf['women_count'] + polygon_gdf['men_count']
    return polygon_gdf

def style_function(feature):
    opacity_percentage = feature['properties']['women_perc']
    opacity_percentage = int(opacity_percentage)

    if opacity_percentage == 0:
        rgba_color = '#FFFFFF00'  
    else:
        alpha_value = int((opacity_percentage / 100) * 255)
        alpha_hex = format(alpha_value, '02X')
        rgba_color = '#e22e1f' + alpha_hex

    return {
        'fillColor': rgba_color,
        'color': 'black',
        'weight': 2,
        'fillOpacity': opacity_percentage / 100 if opacity_percentage != 0 else 0,
    }

#Map
def map(filtered_df, shapefile_path):
    try:
        gdf = map_df(filtered_df, shapefile_path)
        if gdf.empty:
            st.warning("No data to display on the map.")
        else:
            gdf['geometry_wkt'] = gdf.geometry.apply(lambda x: x.wkt)

            map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
            m = folium.Map(location=map_center, zoom_start=10)

            folium.GeoJson(
                gdf.__geo_interface__,
                style_function=style_function,
                tooltip=folium.GeoJsonTooltip(fields=['point_count', 'women_perc'],
                                                aliases=['Total Count:', 'Female Percentage:'],
                                                localize=True)
            ).add_to(m)

            for _, row in gdf.iterrows():
                geom = row['geometry']
                if geom.geom_type == 'Point':
                    folium.Marker(
                        location=[geom.y, geom.x],
                        popup=f"Count: {row['women_count']}"
                    ).add_to(m)

            st_folium(m, width='100%', height=500, key="map_display")
    except Exception as e:
        st.error(f"An error occurred while generating the map: {e}")
        m = folium.Map(location=[40.0691, 45.0382])
        st_folium(m, width='100%', height=500, key="map_error")