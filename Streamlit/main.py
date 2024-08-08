import streamlit as st
from streamlit_option_menu import option_menu
from utils_map import map
from utils import (
    load_data, 
    apply_filters, 
    compute_gender_distribution, 
    get_top_activities, 
    get_top_products, 
    get_roles,
    timeseries,
    pie,
    filters,
    act,
    prod,
    roles
)
from utils_style import (
    set_background, 
    include_font_awesome, 
    load_sidebar_logo, 
    about_us, 
    contact_us,
    dist_box,
    act_box,
    config
)


# Sidebar paths
logo = '/home/copa/Spyur/Streamlit/logo1.png'
sidebar_path = '/home/copa/Spyur/Streamlit/logo2.png'

# Streamlit configuration
config(logo)

# Loading the sidebar image
load_sidebar_logo(sidebar_path) 

# Navigation menu
menu_option = option_menu(
    None,
    ["Home", "Distribution", "Timeseries", "Main Activities", "Main Products", "Roles", "Map"],
    icons=["house", "people", "clock", "activity", "box", "briefcase", "map"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Sidebar filters
st.sidebar.header("Filters")

#Filters
selected_size, selected_ownership = filters()

# Load the DataFrame
file_path = '/home/copa/Spyur/Streamlit/spyur.pkl'
final_df = load_data(file_path)

# Apply filters
filtered_df = apply_filters(final_df, selected_size, selected_ownership)


# Home Page
if menu_option == "Home":
    include_font_awesome()
    set_background('https://i.pinimg.com/736x/10/31/1b/10311bd91a872378712d17ed79435f5a.jpg')
    about_us()
    contact_us()


# Distribution Page
elif menu_option == "Distribution":
    st.title("Gender Distribution")
    gender_counts, male_percent, female_percent = compute_gender_distribution(filtered_df)
    fig_pie, male_counts, female_counts = pie(gender_counts, male_percent, female_percent)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("          ")
        st.subheader('Gender Distribution')
        st.plotly_chart(fig_pie)
    with col2:
        dist_box(gender_counts, male_counts, male_percent, female_counts, female_percent)
    with col3:
        act_box()


# Timeseries Page
elif menu_option == "Timeseries":
    st.subheader('Timeseries')
    st.markdown('<p style="color:gray; font-size:12px;">This timeseries is based on founding year for companies who mentioned the date</p>', unsafe_allow_html=True)
    timeseries(final_df)


# Main Activities Page
elif menu_option == "Main Activities":
    st.title("Main Activities by Gender")
    male_activities = get_top_activities(filtered_df, 'Male')
    female_activities = get_top_activities(filtered_df, 'Female')

    male_activities_pct = round(male_activities * 100, 2)
    female_activities_pct = round(female_activities * 100, 2)

    act(male_activities_pct, female_activities_pct)


# Main Products Page
elif menu_option == "Main Products":
    st.title("Main Products by Gender")
    male_products = get_top_products(filtered_df, 'Male')
    female_products = get_top_products(filtered_df, 'Female')

    male_products_pct = round(male_products * 100, 2)
    female_products_pct = round(female_products * 100, 2)
 
    prod(male_products_pct, female_products_pct)


# Roles Page
elif menu_option == "Roles":
    st.title("Roles by Gender")
    male_roles = get_roles(filtered_df, 'Male')
    female_roles = get_roles(filtered_df, 'Female')

    male_roles_percentage = get_roles(filtered_df, 'Male')
    female_roles_percentage = get_roles(filtered_df, 'Female')

    roles(male_roles_percentage, female_roles_percentage)


# Map Page
elif menu_option == "Map":
    st.subheader('Female Executives On Map')
    shapefile_path = '/home/copa/Spyur/Streamlit/Map/arm.shp'
    map(filtered_df, shapefile_path)
