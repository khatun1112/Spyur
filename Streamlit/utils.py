import pickle
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Load the DataFrame
def load_data(file_path):
    with open(file_path, 'rb') as f:
        final_df = pickle.load(f)
    return final_df

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

# Compute gender distribution
def compute_gender_distribution(df):
        aggregated_df = df.drop_duplicates(subset='url_id')
        gender_counts = aggregated_df['gender'].value_counts()
        total_count = gender_counts.sum()
        
        male_percent = round((gender_counts.get('Male', 0) / total_count) * 100, 2)
        female_percent = round((gender_counts.get('Female', 0) / total_count) * 100, 2)
        return gender_counts, male_percent, female_percent

# Get top activities
def get_top_activities(df, gender, top_n=15):
    activities = df[df['gender'] == gender]['cluster'].value_counts(normalize=True).head(top_n)
    return activities

# Get top products
def get_top_products(df, gender, top_n=15):
    filtered_df = df[(df['gender'] == gender) & (df['label'].notna()) & (df['label'] != 'N/A')]
    products = filtered_df['label'].value_counts(normalize=True).head(top_n)
    return products

# Get roles
def get_roles(df, gender, top_n=10):
    aggregated_df = df.drop_duplicates(subset='full_name')
    roles = aggregated_df[aggregated_df['gender'] == gender]['role'].value_counts().head(top_n)
    total = roles.sum()
    roles_percentage = round((roles / total) * 100, 2)
    return roles_percentage

#Pieplot
def pie(gender_counts, male_percent, female_percent):
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
    return fig_pie, male_counts, female_counts

#Timeseries
def timeseries(final_df):

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

#Sidebar filters
def filters():
    # Filter by company size
    employees_list = ['From 16 to 50', 'Up to 15', 'From 51 to 250', 'From 251 to 1000', 'From 1001 to 2000', 'Over 2000']
    company_sizes = ['All'] + employees_list
    selected_size = st.sidebar.selectbox('Select Company Size', company_sizes)

    # Filter by form of ownership
    forms = ['Non-governmental', 'State', 'International', 'Foreign', 'Mixed (non-governmental/state)']
    forms_of_ownership = ['All'] + forms
    selected_ownership = st.sidebar.selectbox('Select Form of Ownership', forms_of_ownership) 

    return selected_size, selected_ownership       

#Activities
def act(male_activities_pct, female_activities_pct):
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

#Products
def prod(male_products_pct, female_products_pct):
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

#Roles
def roles(male_roles_percentage, female_roles_percentage):
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
