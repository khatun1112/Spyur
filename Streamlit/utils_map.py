import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

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
