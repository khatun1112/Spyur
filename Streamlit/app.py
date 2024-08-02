import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import geopandas as gpd
from utils_map import map_df, style_function
from streamlit_folium import st_folium


# Load the DataFrame
with open('comp_and_ex.pkl', 'rb') as f:
    final_df = pd.read_pickle(f)

# Sidebar paths
sidebar_path = '/Users/copa/Desktop/Top2Vec/Spyur/Streamlit/download-1-removebg-preview.png'
logo = '/Users/copa/Desktop/Top2Vec/Spyur/Streamlit/[removal.ai]_916c7b22-1390-4e8f-b8a3-45ad4baf38ab-images-1.png'

# Streamlit configuration
st.set_page_config(
    page_title="SDG5",
    page_icon=logo, 
    layout="wide",
    initial_sidebar_state="expanded",
)

# Loading the sidebar image
sidebar_logo = Image.open(sidebar_path)
st.sidebar.image(sidebar_logo, use_column_width=False, width=220) 


# Navigation menu
menu_option = st.sidebar.radio("Go to", ["Gender Distribution", "Main Activities", "Main Products", "Roles", "Map"])

# Sidebar filters
st.sidebar.header("Filters")

# Filter by company size
employees_list = ['From 16 to 50', 'Up to 15', 'From 51 to 250', 'From 251 to 1000', 'From 1001 to 2000', 'Over 2000']
company_sizes = ['All'] + employees_list
selected_size = st.sidebar.selectbox('Select Company Size', company_sizes)

# Filter by form of ownership
forms = ['Non-governmental', 'State', 'International', 'Foreign', 'Mixed (non-governmental/state)']
forms_of_ownership = ['All'] + forms
selected_ownership = st.sidebar.selectbox('Select Form of Ownership', forms_of_ownership)

# Filter by year established
max_year = int(final_df['year_established'].max())
min_year = 1832
selected_year_range = st.sidebar.slider('Select Year Range', min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)

# Applying filters
def apply_filters(df, company_size, form_of_ownership, year_range):
    filtered_df = df.copy()
    
    # Filtering based on company size
    if company_size and company_size != 'All':
        filtered_df = filtered_df[filtered_df['number_of_employees'] == company_size]
    
    # Filtering based on form of ownership
    if form_of_ownership and form_of_ownership != 'All':
        filtered_df = filtered_df[filtered_df['form_of_ownership'] == form_of_ownership]
    
    # Filtering based on year established range
    if year_range:
        start_year, end_year = year_range
        filtered_df = filtered_df[(filtered_df['year_established'] >= start_year) & 
                                  (filtered_df['year_established'] <= end_year)]
    
    return filtered_df

# Appling filters
filtered_df = apply_filters(final_df, selected_size, selected_ownership, selected_year_range)

# Headers
st.title('Gender Roles in Workplace')

if menu_option == "Gender Distribution":
    st.subheader('Gender Distribution')

    # Computing gender distribution
    def compute_gender_distribution(df):
        aggregated_df = df.drop_duplicates(subset='url_id')
        gender_counts = aggregated_df['gender'].value_counts()
        total_count = gender_counts.sum()
        
        male_percent = round((gender_counts.get('Male', 0) / total_count) * 100, 2)
        female_percent = round((gender_counts.get('Female', 0) / total_count) * 100, 2)
        return gender_counts, male_percent, female_percent, 

    gender_counts, male_percent, female_percent = compute_gender_distribution(filtered_df)

    colors = {'Female': '#e22e1f', 'Male': '#4788c8'}
    male_counts = (gender_counts.get('Male', 0))
    female_counts = (gender_counts.get('Female', 0))

    # Pie chart with hover information
    fig_pie = go.Figure(data=[go.Pie(labels=['Male', 'Female', 'Unknown'], 
                                    values=[male_counts, female_counts], 
                                    customdata=[male_percent, female_percent],
                                    hoverinfo='text', textinfo='percent',
                                    text=[f'Male count: {male_counts}', f'Female count: {female_counts}'],
                                    marker=dict(colors=[colors.get(gender, '#000000') for gender in ['Male', 'Female', 'Unknown']]))])

    fig_pie.update_layout(
        title='Gender Distribution',
        template='plotly_white'
    )

    # Line plot for executive counts over years 
    fig_line = go.Figure()
    aggregated_df = filtered_df.drop_duplicates(subset='url_id')
    exec_counts = aggregated_df.groupby('year_established')['gender'].value_counts().unstack().fillna(0)

    for gender in exec_counts.columns:
        fig_line.add_trace(go.Scatter(x=exec_counts.index, y=exec_counts[gender], mode='lines+markers', name=gender, line=dict(color=colors.get(gender, '#000000'))))

    fig_line.update_layout(
        title='Executive Counts Based On Year Established',
        xaxis_title='Year Established',
        yaxis_title='Count',
        legend_title='Gender',
        template='plotly_white'
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_pie)

    with col2:
        st.plotly_chart(fig_line)

elif menu_option == "Main Activities":
    st.subheader('Main Activities')

    def get_top_activities(df, gender, top_n=15):
        activities = df[df['gender'] == gender]['cluster'].value_counts(normalize=True).head(top_n)
        return activities

    male_activities = get_top_activities(filtered_df, 'Male').sort_values(ascending=False)
    female_activities = get_top_activities(filtered_df, 'Female').sort_values(ascending=False)

    male_activities_pct = round(male_activities * 100, 2)
    female_activities_pct = round(female_activities * 100, 2)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Male")
        fig_male = px.bar(male_activities_pct, x=male_activities_pct.values, y=male_activities_pct.index, orientation='h',
                        labels={'x': 'Percentage'})
        st.plotly_chart(fig_male, use_container_width=True)

    with col2:
        st.write("Female")
        fig_female = px.bar(female_activities_pct, x=female_activities_pct.values, y=female_activities_pct.index, orientation='h',
                            labels={'x': 'Percentage'})
        st.plotly_chart(fig_female, use_container_width=True)

# elif menu_option == "Main Products":
#     st.subheader('Main Products')

#     def get_top_products(df, gender, top_n=15):
#         products = df[df['gender'] == gender]['product_name'].value_counts(normalize=True).head(top_n)
#         return products

#     male_products = get_top_products(filtered_df, 'Male').sort_values(ascending=False)
#     female_products = get_top_products(filtered_df, 'Female').sort_values(ascending=False)

#     male_products_pct = round(male_products * 100, 2)
#     female_products_pct = round(female_products * 100, 2)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("Male")
#         st.bar_chart(male_products_pct)

#     with col2:
#         st.write("Female")
#         st.bar_chart(female_products_pct)

elif menu_option == "Roles":
    st.subheader('Top 10 Roles for Executives')

    def get_roles(df, gender, top_n=10):
        aggregated_df = df.drop_duplicates(subset='full_name')
        roles = aggregated_df[aggregated_df['gender'] == gender]['role'].value_counts().head(top_n)
        total = roles.sum()
        roles_percentage = round((roles / total) * 100, 2)  
        return roles_percentage

    male_roles_percentage = get_roles(filtered_df, 'Male')
    female_roles_percentage = get_roles(filtered_df, 'Female')

    col1, col2 = st.columns(2)
    with col1:
        st.write("Male")
        fig_male = px.bar(male_roles_percentage, x=male_roles_percentage.values, y=male_roles_percentage.index, orientation='h',
                          labels={'x': 'Percentage', 'y': 'Role'}, title="Male Executive Roles")
        st.plotly_chart(fig_male, use_container_width=True)

    with col2:
        st.write("Female")
        fig_female = px.bar(female_roles_percentage, x=female_roles_percentage.values, y=female_roles_percentage.index, orientation='h',
                            labels={'x': 'Percentage', 'y': 'Role'}, title="Female Executive Roles")
        st.plotly_chart(fig_female, use_container_width=True)


elif menu_option == "Map":
    st.subheader('Female Executives On Map')
    try:
        shapefile_path = '/Users/copa/Desktop/Top2Vec/Spyur/Streamlit/Map/arm.shp'
        
        @st.cache_data
        def load_data(filepath):
            return gpd.read_file(filepath)

        gdf = map_df(filtered_df, shapefile_path)
        gdf['geometry_wkt'] = gdf.geometry.apply(lambda x: x.wkt)
        
        map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
        m = folium.Map(location=map_center, zoom_start=10)
        
        folium.GeoJson(
            gdf.__geo_interface__,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(fields=['women_count', 'women_perc'],
                                        aliases=['Count:', 'Percentage:'],
                                        localize=True)
        ).add_to(m)
        
        for _, row in gdf.iterrows():
            geom = row['geometry']
            if geom.geom_type == 'Point':
                folium.Marker(
                    location=[geom.y, geom.x],
                    popup=f"Count: {row['women_count']}"
                ).add_to(m)

        st_folium(m, width='100%', height=500)

    except Exception as e:
        m = folium.Map(location=[40.0691, 45.0382])
        st_folium(m, width='100%', height=500)