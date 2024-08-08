import streamlit as st

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

# Include Font Awesome CDN for icons
def include_font_awesome():
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)

# Logos
def load_sidebar_logo(sidebar_path, width=220):
    from PIL import Image
    sidebar_logo = Image.open(sidebar_path)
    st.sidebar.image(sidebar_logo, use_column_width=False, width=width)

# About Us section
def about_us():
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
                We invite you to explore our dashboard, delve into the data, and join us in our mission to drive positive change and create a more inclusive and balanced workforce.
            <p> Thank you for your interest in our work and for being a part of this important journey.</p>
        </div>
    """, unsafe_allow_html=True)

# Contact Us section
def contact_us():
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


#Distribution Boxes
def dist_box(gender_counts, male_counts, male_percent, female_counts, female_percent):
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

#Activities box
def act_box():
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

#Streamlit config
def config(logo):
     st.set_page_config(
    page_title="SDG 5",
    page_icon=logo, 
    layout="wide",
    initial_sidebar_state="expanded",
)
     
