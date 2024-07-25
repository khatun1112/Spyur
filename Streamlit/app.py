import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px

with open('final_df.pkl', 'rb') as f:
    final_df = pd.read_pickle(f)

#Streamlit configuration
st.set_page_config(
    page_title="Gender Roles in the Workplace",
    page_icon=":bar_chart:", 
    layout="wide",
    initial_sidebar_state="expanded",

)

#streamlit headers
st.title('Gender Roles in Workplace')
st.subheader('Gender Distribution')

# Function to plot gender distribution based on filters
def compute_gender_distribution(df, company_size=None, form_of_ownership=None, year_established_range=None):
    filtered_df = df.copy()

    # Filter based on company size
    if company_size and company_size != 'All':
        filtered_df = filtered_df[filtered_df['number_of_employees'] == company_size]
    
    # Filter based on form of ownership
    if form_of_ownership and form_of_ownership != 'All':
        filtered_df = filtered_df[filtered_df['form_of_ownership'] == form_of_ownership]
    
    # Filter based on year established range
    if year_established_range:
        start_year, end_year = year_established_range
        filtered_df = filtered_df[(filtered_df['year_established'] >= start_year) & 
                                  (filtered_df['year_established'] <= end_year)]

    # Remove duplicate rows based on company_name and aggregate gender counts
    aggregated_df = filtered_df.drop_duplicates(subset=['company_name', 'gender'])
    gender_counts = aggregated_df['gender'].value_counts()
    total_count = gender_counts.sum()

    male_percent = round((gender_counts.get('Male', 0) / total_count) * 100, 2)
    female_percent = round((gender_counts.get('Female', 0) / total_count) * 100, 2)
    unknown_percent = round((gender_counts.get('Unknown', 0) / total_count) * 100, 2)
    
    return filtered_df, gender_counts, male_percent, female_percent, unknown_percent


st.sidebar.subheader('Selecta a Filter')

# Filter by company size
employees_list = ['From 16 to 50', 'Up to 15', 'From 51 to 250',
       'From 251 to 1000', 'From 1001 to 2000', 'Over 2000']
company_sizes = ['All'] + employees_list
selected_size = st.sidebar.selectbox('Select Company Size', company_sizes)

# Filter by form of ownership
forms_of_ownership = ['All'] + final_df['form_of_ownership'].dropna().unique().tolist()
selected_ownership = st.sidebar.selectbox('Select Form of Ownership', forms_of_ownership)

# Filter by year established
max_year = int(final_df['year_established'].max())
min_year = int(final_df['year_established'].min())
selected_year_range = st.slider('Select Year Range', min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)

# Gender distribution based on selected filters
filtered_df, gender_counts, male_percent, female_percent, unknown_percent = compute_gender_distribution(final_df, selected_size, selected_ownership, selected_year_range)

colors = {'Female': '#f0aada',
          'Male': '#aac3f0',
          'Unknown': '#b4d4a3'}

male_counts = (gender_counts.get('Male', 0))
female_counts = (gender_counts.get('Female', 0))
unknown_counts = (gender_counts.get('Unknown', 0))

# Pie chart with hover information
fig_pie = go.Figure(data=[go.Pie(labels=['Male', 'Female', 'Unknown'], 
                                 values=[male_counts, female_counts, unknown_counts], 
                                 customdata=[male_percent, female_percent, unknown_percent],
                                 hoverinfo='text', textinfo='percent',
                                 text=[f'Male count: {male_counts}', f'Female count: {female_counts}', f'Unknown count: {unknown_counts}'],
                                 marker=dict(colors=[colors.get(gender, '#000000') for gender in ['Male', 'Female', 'Unknown']]))])

fig_pie.update_layout(
    title='Gender Distribution',
    template='plotly_white'
)

# Line plot for executive counts over years 
fig_line = go.Figure()
aggregated_df = filtered_df.drop_duplicates(subset=['company_name', 'gender'])
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


# Display main activities for males and females in pct
def get_top_activities(df, gender, top_n=15):
    activities = df[df['gender'] == gender]['act_second_level_cluster'].value_counts(normalize=True).head(top_n)
    return activities

st.subheader(' Main Activities')
male_activities = get_top_activities(filtered_df, 'Male').sort_values(ascending=False)
female_activities = get_top_activities(filtered_df, 'Female').sort_values(ascending=False)

male_activities_pct = round(male_activities * 100, 2)
female_activities_pct = round(female_activities * 100, 2)

with col1:
    st.write("Male")
    fig_male = px.bar(male_activities_pct, x=male_activities_pct.values, y=male_activities_pct.index, orientation='h',
                      labels={'x': 'Percentage', 'y': 'Activity'})
    st.plotly_chart(fig_male, use_container_width=True)

with col2:
    st.write("Female")
    fig_female = px.bar(female_activities_pct, x=female_activities_pct.values, y=female_activities_pct.index, orientation='h',
                        labels={'x': 'Percentage', 'y': 'Activity'})
    st.plotly_chart(fig_female, use_container_width=True)


# Display main products for males and females
def get_top_products(df, gender, top_n=15):
    products = df[df['gender'] == gender]['prod_second_level_cluster'].value_counts(normalize=True).head(top_n)
    return products

st.subheader('Main products')
male_products = get_top_products(filtered_df, 'Male').sort_values(ascending=False)
female_products = get_top_products(filtered_df, 'Female').sort_values(ascending=False)

male_products_pct = round(male_products * 100, 2)
female_products_pct = round(female_products * 100, 2)

col1, col2 = st.columns(2)
with col1:
    st.write("Male", unsafe_allow_html=True)
    st.bar_chart(male_products_pct)
    
with col2:
    st.markdown("Female", unsafe_allow_html=True)
    st.bar_chart(female_products_pct)    

#Display Roles for males and females
def get_roles(df, gender,):
    roles = df[df['gender'] == gender]['role'].value_counts()
    return roles

st.subheader('Roles for Executives')
male_roles = get_roles(filtered_df, 'Male')
female_roles = get_roles(filtered_df, 'Female')

col1, col2 = st.columns(2)
with col1:
    st.markdown("Male", unsafe_allow_html=True)
    st.table(male_roles)
    
with col2:
    st.markdown("Female", unsafe_allow_html=True)
    st.table(female_roles)


# Create a Streamlit map with Folium
st.subheader('Company Locations in Armenia')
map_center = [40.0691, 45.0382] 
m = folium.Map(location=map_center, zoom_start=7, control_scale=True)
filtered_df_unique = filtered_df.drop_duplicates(subset=['location'])


def add_markers_to_map(map_obj, df):
    for idx, row in df.iterrows():
        try:
            lat, lon = row['location']
            
            gender = row['gender']
            color = colors.get(gender, '#000000')
            
            folium.CircleMarker(
                location=(lat, lon),
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"{row['company_name']}\nGender: {gender}"
            ).add_to(map_obj)
        except Exception as e:
            st.error(f"Error processing row {idx}: {e}")

add_markers_to_map(m, filtered_df)
st_folium(m, width='100%', height=500)
