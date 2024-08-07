import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from utils_map import map_df, style_function
from streamlit_folium import st_folium
import pickle
from streamlit_option_menu import option_menu

# Function to set the background image with transparency and margin
def set_background(image_url):
    background_image = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("{image_url}");
        background-size: 100vw 100vh;  
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.8); /* Adjust the transparency here */
        margin-top: -35px; 
    }}
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)

# Load the DataFrame
file_path = '/home/copa/Spyur/Streamlit/spyur.pkl'
with open(file_path, 'rb') as f:
    final_df = pickle.load(f)
    
# Sidebar paths
logo = '/home/copa/Spyur/Streamlit/logo1.png'
sidebar_path = '/home/copa/Spyur/Streamlit/logo2.png'

# Streamlit configuration
st.set_page_config(
    page_title="SDG 5",
    page_icon=logo, 
    layout="wide",
    initial_sidebar_state="expanded",
)

# Loading the sidebar image
sidebar_logo = Image.open(sidebar_path)
st.sidebar.image(sidebar_logo, use_column_width=False, width=220) 

# Navigation menu
menu_option = option_menu(
    None,
    ["Home","Distribution", "Timeseries", "Main Activities", "Main Products", "Roles", "Map"],
    icons=["house","people", "clock", "activity", "box", "briefcase", "map"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

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

# Applying filters
def apply_filters(df, company_size, form_of_ownership):
    filtered_df = df.copy()
    
    # Filtering based on company size
    if company_size and company_size != 'All':
        filtered_df = filtered_df[filtered_df['number_of_employees'] == company_size]

    # Filtering based on form of ownership
    if form_of_ownership and form_of_ownership != 'All':
        filtered_df = filtered_df[filtered_df['form_of_ownership'] == form_of_ownership]    
    
    return filtered_df

# Appling filters
filtered_df = apply_filters(final_df, selected_size, selected_ownership)

# Include Font Awesome CDN for icons
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)

if menu_option == "Home":
    # Header
    # st.markdown('<h1 style="color:#e31f33;">Workplace Gender Roles</h1>', unsafe_allow_html=True)
    set_background('https://i.pinimg.com/736x/10/31/1b/10311bd91a872378712d17ed79435f5a.jpg')
    # About Us section
    st.markdown("""
        <div style="
            border: 2px;
            border-radius: 10px;
            padding: 20px;
            width: 70%;
            background-color: rgba(245, 251, 255, 0.7);
            margin-left: 0;
            margin-bottom: 40px;
            font-family: Arial, sans-serif; 
            font-size: 16px;
            line-height: 2;  
        ">
            <h2>About Us</h2>
            <p>Welcome to COPA, a forward-thinking data science company. </p>
            <p> Our team recently undertook an ambitious project focused on understanding gender roles within the Armenian workplace. Our research aimed to uncover and analyze the representation of 
                women in executive roles across various industries in Armenia.</p>
            <p> Through meticulous data collection and analysis, we have developed an intuitive and interactive dashboard that visualizes the percentage of women in leadership positions. 
                This tool is designed to provide valuable insights into gender diversity and highlight areas for improvement. Our goal is to shed light on the current state of gender representation 
                in high-level roles and promote discussions and strategies to enhance women's participation in leadership.</p>
            <p>  At COPA, we are committed to using our expertise to not only provide data-driven solutions but also to contribute to social progress.</p>
                We invite you to explore our dashboard, delve into the data, and join us in our mission to drive positive change and create a more inclusive and balanced workforce.
            <p> Thank you for your interest in our work and for being a part of this important journey.</p>
        </div>
    """, unsafe_allow_html=True)

    # Contact Us section
    st.markdown("""
        <div style="
            border: 2px;
            border-radius: 10px;
            padding: 20px;
            width: 70%;
            background-color: rgba(245, 251, 255, 0.7); 
            margin-left: 0;
            font-family: Arial, sans-serif; 
            font-size: 16px;
            line-height: 1.6; 
        ">
            <h2 style="font-size: 24px; margin-top: 0;">Contact Us</h2>
            <p>If you have any questions, feel free to reach out to us through the following channels:</p>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><i class="fab fa-github" style="color: #333; margin-right: 8px;"></i><a href="https://github.com/khatun1112/Spyur" target="_blank">GitHub</a></li>
                <li><i class="fas fa-globe" style="color: #333; margin-right: 8px;"></i><a href="https://www.copa.team/" target="_blank">Website</a></li>
                <li><i class="fas fa-envelope" style="color: #333; margin-right: 8px;"></i><a href="mailto:info@copa.team">Email Us</a></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


if menu_option == "Distribution":
    
    def compute_gender_distribution(df):
        aggregated_df = df.drop_duplicates(subset='url_id')
        gender_counts = aggregated_df['gender'].value_counts()
        total_count = gender_counts.sum()
        
        male_percent = round((gender_counts.get('Male', 0) / total_count) * 100, 2)
        female_percent = round((gender_counts.get('Female', 0) / total_count) * 100, 2)
        return gender_counts, male_percent, female_percent

    gender_counts, male_percent, female_percent = compute_gender_distribution(filtered_df)

    colors = {'Female': '#e22e1f', 'Male': '#4788c8'}
    male_counts = gender_counts.get('Male', 0)
    female_counts = gender_counts.get('Female', 0)

    fig_pie = go.Figure(data=[go.Pie(labels=['Male', 'Female'], 
                                    values=[male_counts, female_counts], 
                                    customdata=[male_percent, female_percent],
                                    hoverinfo='label+percent+value', textinfo='percent',
                                    text=[f'Male count: {male_counts}', f'Female count: {female_counts}'],
                                    marker=dict(colors=[colors['Male'], colors['Female']]))])

    fig_pie.update_layout(
        template='plotly_white',
        height=600,  
        width=600,  
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("          ")
        st.subheader('Gender Distribution')
        st.plotly_chart(fig_pie)

    with col2:
        st.markdown("""
        <style>
            .insight-box {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            .insight-title {
                font-size: 15px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .insight-list {
                margin: 0;
                padding: 0;
                list-style-type: none;
            }
            .insight-list li {
                margin-bottom: 8px;
            }
            .insight-list li::before {
                content: '•';
                color: #007bff;
                font-weight: bold;
                display: inline-block;
                width: 1em;
                margin-left: -1em;
            }
        </style>
        """, unsafe_allow_html=True)

        # Key Insights Column
        with st.expander("## Key Insights", expanded=True):
            st.markdown('<div class="insight-title">Main Info:</div>', unsafe_allow_html=True)
            st.markdown(f"<p>Total Companies: {gender_counts.sum()}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Male Executives: {male_counts} ({male_percent}%)</p>", unsafe_allow_html=True)
            st.markdown(f"<p>Female Executives: {female_counts} ({female_percent}%)</p>", unsafe_allow_html=True)
            st.markdown("<p>The Highest Pct of Female Executives Based on Company Size: Up to 15</p>", unsafe_allow_html=True)
            st.markdown("<p>The Lowest Pct of Female Executives Based on Company Size: From 1001 to 2000</p>", unsafe_allow_html=True)
            st.markdown("<p>The Highest Pct of Female Executives Based on Form of Ownership: State</p>", unsafe_allow_html=True)
            st.markdown("<p>The Lowest Pct of Female Executives Based on Form of Ownership: Non-governmental</p>", unsafe_allow_html=True)
            st.markdown("<p>The Pct of Female Executives in Capital City: Yerevan (33%)</p>", unsafe_allow_html=True)
            st.markdown("<p>State with the Highest Pct of Female Executives: Aragatsotn (47%)</p>", unsafe_allow_html=True)
            st.markdown("<p>State with the Lowest Pct of Female Executives: Vayoc Dzor (30%)</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        # Top Activities Column
        st.markdown("          ")
        with st.expander("Activities and Products", expanded=True):
            st.markdown('<div class="insight-title">Top 3 Activities for Women:</div>', unsafe_allow_html=True)
            st.markdown("""
            <ul class="insight-list">
                <li>Retail and E-commerce (13.58%)</li>
                <li>Hospitality and Tourism (10.52%)</li>
                <li>Education and Training Services (9.53%)</li>
            </ul>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="insight-title">Top 3 Activities for Men:</div>', unsafe_allow_html=True)
            st.markdown("""
            <ul class="insight-list">
                <li>Manufacturing (15.54%)</li>
                <li>Retail and E-commerce (13.43%)</li>
                <li>Construction and Real Estate (10.35%)</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown('<div class="insight-title">Top 3 Products for Women:</div>', unsafe_allow_html=True)
            st.markdown("""
            <ul class="insight-list">
                <li>Manufactoring and Industrial Equipment (10.54%)</li>
                <li>Retail and Consumer Goods (9.68%)</li>
                <li>Hospitality and Tourism (9.28%)</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="insight-title">Top 3 Products for Men:</div>', unsafe_allow_html=True)
            st.markdown("""
            <ul class="insight-list">
                <li>Manufactoring and Industrial Equipment (19.55%)</li>
                <li>Construction and Infrastructure (8.86%)</li>
                <li>Retail and Consumer Goods (7.77%)</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


        
if menu_option == "Timeseries":
    st.subheader('Timeseries')
    st.markdown('<p style="color:gray; font-size:12px;">This timeseries is based on founding year for companies who mentioned the date</p>', unsafe_allow_html=True)

    filtered_df = final_df[final_df['year_established'] >= 1991]

    max_year = int(filtered_df['year_established'].max())
    min_year = 1991
    selected_year_range = st.slider('Select Year Range', min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)

    filtered_df = filtered_df[(filtered_df['year_established'] >= selected_year_range[0]) & 
                              (filtered_df['year_established'] <= selected_year_range[1])]
    
    filtered_df = filtered_df[filtered_df['cluster'] != 'N/A']
    clusters = filtered_df['cluster'].unique()
    clusters_with_all = ['All'] + list(clusters)
    
    col1, col2 = st.columns([3, 1])  
    
    with col2:
        st.markdown("###           ")
        st.markdown("###           ")
        selected_clusters = st.selectbox('Select Industry', options=clusters_with_all)
    
    with col1:
        if selected_clusters == 'All':
             pass
        else:
            filtered_df = filtered_df[filtered_df['cluster'] == selected_clusters]


        # Line plot for executive percentages over years
        fig_line = go.Figure()
        aggregated_df = filtered_df.drop_duplicates(subset='url_id')
        exec_counts = aggregated_df.groupby('year_established')['gender'].value_counts().unstack().fillna(0)

        exec_totals = exec_counts.sum(axis=1)
        exec_pct = exec_counts.div(exec_totals, axis=0) * 100

        colors = {'Female': '#e22e1f', 'Male': '#4788c8'}
        for gender in exec_pct.columns:
            fig_line.add_trace(go.Scatter(
                x=exec_pct.index, 
                y=exec_pct[gender], 
                mode='lines+markers', 
                name=gender, 
                line=dict(color=colors.get(gender, '#000000')),
                text=[f"Count: {count}<br>Percentage: {pct:.1f}%" for count, pct in zip(exec_counts[gender].astype(int), exec_pct[gender])], 
                hoverinfo='x+text'  
            ))

        fig_line.update_layout(
            title='Executive Percentages Based On Year Established',
            xaxis_title='Year Established',
            yaxis_title='Percentage (%)',
            legend_title='Gender',
            template='plotly_white'
        )
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

elif menu_option == "Main Products":
    st.subheader('Main Products')

    def get_top_products(df, gender, top_n=15):
        filtered_df = df[(df['gender'] == gender) & (df['label'].notna()) & (df['label'] != 'N/A')]
        products = filtered_df['label'].value_counts(normalize=True).head(top_n)
        return products

    male_products = get_top_products(filtered_df, 'Male').sort_values(ascending=False)
    female_products = get_top_products(filtered_df, 'Female').sort_values(ascending=False)

    male_products_pct = round(male_products * 100, 2)
    female_products_pct = round(female_products * 100, 2)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Male")
        fig_male = px.bar(male_products_pct, x=male_products_pct.values, y=male_products_pct.index, orientation='h',
                        labels={'x': 'Percentage'})
        st.plotly_chart(fig_male, use_container_width=True)

    with col2:
        st.write("Female")
        fig_female = px.bar(female_products_pct, x=female_products_pct.values, y=female_products_pct.index, orientation='h',
                        labels={'x': 'Percentage'})
        st.plotly_chart(fig_female, use_container_width=True)

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
    shapefile_path = '/home/copa/Spyur/Streamlit/Map/arm.shp'

    
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