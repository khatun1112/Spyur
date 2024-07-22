#Libraries
import pandas as pd
import streamlit as st 
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import folium.plugins as plugins


spyur_df = pd.read_pickle('spyur_df.pkl')

st.title('Gender Roles in Workplace')
st.subheader('Gender Distribution')

# Function to plot gender distribution based on filters
def compute_gender_distribution(df, company_size=None, form_of_ownership=None, year_established_range=None):
    filtered_df = df.copy()

    # Apply filters if selected
    if company_size and company_size != 'All':
        filtered_df = filtered_df[filtered_df['Number of employees'] == company_size]
    
    if form_of_ownership and form_of_ownership != 'All':
        filtered_df = filtered_df[filtered_df['Form of ownership'] == form_of_ownership]
    
    if year_established_range:
        start_year, end_year = year_established_range
        filtered_df = filtered_df[(filtered_df['Year established'] >= start_year) & 
                                  (filtered_df['Year established'] <= end_year)]
    
    gender_counts = filtered_df['Gender'].value_counts()
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
forms_of_ownership = ['All'] + spyur_df['Form of ownership'].dropna().unique().tolist()
selected_ownership = st.sidebar.selectbox('Select Form of Ownership', forms_of_ownership)

# Filter by year established
max_year = int(spyur_df['Year established'].max())
min_year = int(spyur_df['Year established'].min())
selected_year_range = st.slider('Select Year Range', min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)

# Compute gender distribution based on selected filters
filtered_df, gender_counts, male_percent, female_percent, unknown_percent = compute_gender_distribution(spyur_df, selected_size, selected_ownership, selected_year_range)

colors = {'Female': '#f0aada',
          'Male': '#aac3f0',
          'Unknown': '#b4d4a3'}

male_counts = (gender_counts.get('Male', 0))
female_counts = (gender_counts.get('Female', 0))
unknown_counts = (gender_counts.get('Unknown', 0))

# Create a Plotly pie chart with custom colors and hover information
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

# Display the pie chart in Streamlit
st.plotly_chart(fig_pie)

## Line plot for executive counts over years with custom colors
fig_line = go.Figure()
exec_counts = filtered_df.groupby('Year established')['Gender'].value_counts().unstack().fillna(0)

for gender in exec_counts.columns:
    fig_line.add_trace(go.Scatter(x=exec_counts.index, y=exec_counts[gender], mode='lines+markers', name=gender, line=dict(color=colors.get(gender, '#000000'))))

fig_line.update_layout(
    title='Executive Counts Based On Year Established',
    xaxis_title='Year Established',
    yaxis_title='Count',
    legend_title='Gender',
    template='plotly_white'
)

# Display the line plot in Streamlit
st.plotly_chart(fig_line)


# Display main activities for males and females
def get_top_activities(df, gender, top_n=15):
    activities = df[df['Gender'] == gender]['Activity'].value_counts().head(top_n)
    return activities

male_activities = get_top_activities(filtered_df, 'Male')
female_activities = get_top_activities(filtered_df, 'Female')


col1, col2 = st.columns(2)
with col1:
    st.markdown("### Main Activities for Male Executives", unsafe_allow_html=True)
    st.table(male_activities)
    
with col2:
    st.markdown("### Main Activities for Female Executives", unsafe_allow_html=True)
    st.table(female_activities)


# Create a Streamlit map with Folium
st.subheader('Company Locations in Armenia')
map_center = [40.0691, 45.0382] 
m = folium.Map(location=map_center, zoom_start=7, control_scale=True)


def add_markers_to_map(map_obj, df):
    for idx, row in df.iterrows():
        try:
            lat, lon = row['Location']
            gender = row['Gender']
            color = colors.get(gender, '#000000')
            folium.CircleMarker(
                location=(lat, lon),
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"{row['Company Name']}\nGender: {gender}"
            ).add_to(map_obj)
        except Exception as e:
            pass


add_markers_to_map(m, filtered_df)
st_folium(m, width='100%', height=500)