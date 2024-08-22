import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

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
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
import streamlit as st

# Use HTML and CSS to customize the title
st.markdown(
    """
    <style>
    .title {
        color: #FFFFFF; 
        font-size: 36px; 
    }
    </style>
    <div class="title">
        Automated EDA Web-App
    </div>
    """,
    unsafe_allow_html=True
)

with st.header('1. Upload your CSV data'):
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    def load_csv():
        csv = pd.read_csv(uploaded_file)
        return csv
    df = load_csv()
    pr = ProfileReport(df, explorative=True)
    st.header('**DataFrame Preview**')
    st.write(df)
    st.write('---')
    st.header('**Profiling Report**')
    st_profile_report(pr)
else:
    st.info('File Not Uploaded Yet!.')
    
bottom_text = """
    <div style='width: 100%; color: white; text-align: center; padding: 10px; margin-top: 20px;'>
        <p>This is an automated exploratory data analysis web application. Use the "Browse File" button to upload a data file in CSV format. The application will quickly generate a comprehensive summary of the data, providing key insights and detailed analysis in a minimal amount of time.</p>
    </div>
    """
st.markdown(bottom_text, unsafe_allow_html=True)