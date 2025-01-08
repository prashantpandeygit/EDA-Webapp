import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import requests
import threading
import time
from datetime import datetime

# Keep-alive function
def keep_alive():
    while True:
        try:
            url = "https://eda-webapp-603r.onrender.com"
            response = requests.get(url)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Keep-alive ping sent. Status: {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] Ping failed: {str(e)}")
        time.sleep(840)  # 14 minutes

# Start keep-alive thread
keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
keep_alive_thread.start()

# Page configuration
st.set_page_config(
    page_title="Automated EDA Web-App",
    page_icon="📊",
    layout="wide"
)

# Background image and styling
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.hdqwalls.com/wallpapers/dark-abstract-black-minimal-4k-q0.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0);
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 5px;
    border: none;
    padding: 10px 20px;
}
.stButton > button:hover {
    background-color: #45a049;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title with custom styling
st.markdown(
    """
    <style>
    .title {
        color: #FFFFFF; 
        font-size: 36px;
        text-align: center;
        padding: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    </style>
    <div class="title">
        Automated EDA Web-App
    </div>
    """,
    unsafe_allow_html=True
)

# File upload section with progress bar
with st.header('1. Upload your CSV data'):
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# Main application logic
if uploaded_file is not None:
    try:
        with st.spinner('Loading and analyzing your data...'):
            # Load CSV with progress bar
            @st.cache_data  # Cache the data loading
            def load_csv():
                return pd.read_csv(uploaded_file)
            
            df = load_csv()
            
            # Generate profile report with progress bar
            progress_bar = st.progress(0)
            pr = ProfileReport(df, explorative=True)
            progress_bar.progress(100)
            
            # Display DataFrame preview with styling
            st.header('**DataFrame Preview**')
            st.dataframe(df.style.highlight_null(null_color='red'))
            
            st.write('---')
            
            # Display profile report
            st.header('**Profiling Report**')
            st_profile_report(pr)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info('📤 Please upload a CSV file to begin the analysis.')

# Bottom text with enhanced styling
bottom_text = """
    <div style='
        width: 100%;
        color: white;
        text-align: center;
        padding: 20px;
        margin-top: 20px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
    '>
        <p style='font-size: 16px; line-height: 1.6;'>
            This is an automated exploratory data analysis web application. 
            Use the "Browse File" button to upload a data file in CSV format. 
            The application will quickly generate a comprehensive summary of the data, 
            providing key insights and detailed analysis in a minimal amount of time.
        </p>
    </div>
    """
st.markdown(bottom_text, unsafe_allow_html=True)

# Add a health check endpoint
def health_check():
    return {"status": "healthy"}

# Error handling for the main thread
if __name__ == "__main__":
    try:
        st.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")

