import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
from millify import millify # shortens values (10_000 ---> 10k)
from streamlit_extras.metric_cards import style_metric_cards # beautify metric card with css
import plotly.graph_objects as go
import altair as alt 
#import seaborn as sns
#import plotnine
#from plotnine import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import warnings 
warnings.filterwarnings('ignore')

# Import the dataset
image = "PWC.jpg"

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
#creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
# Use Streamlit's secrets management
creds_dict = st.secrets["gcp_service_account"]
# Extract individual attributes needed for ServiceAccountCredentials
credentials = {
    "type": creds_dict.type,
    "project_id": creds_dict.project_id,
    "private_key_id": creds_dict.private_key_id,
    "private_key": creds_dict.private_key,
    "client_email": creds_dict.client_email,
    "client_id": creds_dict.client_id,
    "auth_uri": creds_dict.auth_uri,
    "token_uri": creds_dict.token_uri,
    "auth_provider_x509_cert_url": creds_dict.auth_provider_x509_cert_url,
    "client_x509_cert_url": creds_dict.client_x509_cert_url,
}

# Create JSON string for credentials
creds_json = json.dumps(credentials)

# Load credentials and authorize gspread
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_json), scope)
client = gspread.authorize(creds)

# Example usage: Fetch data from Google Sheets
try:
    spreadsheet1 = client.open('PWC Mapping Activity_0110')
    worksheet1 = spreadsheet1.worksheet('Information_Sharing')
    sheet = pd.DataFrame(worksheet1.get_all_records())
    #st.write(sheet)
except Exception as e:
    st.error(f"Error fetching data from Google Sheets: {str(e)}")


# Streamlit application
def app():
    # Set up the Streamlit page
    #st.set_page_config(page_title='PWC Mapping Dashboard', page_icon='', layout='wide')

    # Custom CSS for centering and resizing
    st.markdown("""
        <style>
            .logo {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 20px;
            }
            .logo img {
                width: 300px; /* Adjust size of the logo */
            }
            .title {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 40px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Use columns for side-by-side layout    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(image, width=350)

    with col3:
        st.write(' ')
        
    # Centered title
    st.markdown('<div class="title">Information Sharing and Data Integration</div>', unsafe_allow_html=True)

    # User inputs
    with st.expander("Submit Your Response"):
        # User inputs
        name = st.text_area("What is your name?", key="name")
        agency = st.text_area("What is your agency/department?", key="agency")
        comment1 = st.text_area("How do we currently share information between agencies?", key="comment1")
        comment2 = st.text_area("What data needs to be shared across agencies to ensure a coordinated response? What are the limitations on that data sharing?", key="comment2")
        comment3 = st.text_area("How do we ensure that information is timely, secure, and relevant for all parties involved?", key="comment3")
        comment4 = st.text_area("How do we make sure that the information shared leads to actionable next steps, not just monitoring?", key="comment4")
        submit_comment = st.button("Submit Comment", key="submit_comment")

        if submit_comment:
            # Prepare the new row
            new_row = {
                'Name': name, 
                'Agency': agency, 
                'How do we currently share information between agencies?': comment1,
                'What data needs to be shared across agencies to ensure a coordinated response? What are the limitations on that data sharing?': comment2,
                'How do we ensure that information is timely, secure, and relevant for all parties involved?': comment3,
                "How do we make sure that the information shared leads to actionable next steps, not just monitoring?": comment4
            }
            new_data = pd.DataFrame([new_row])

            try:
                # Append new data to Google Sheet
                updated_sheet = pd.concat([sheet, new_data], ignore_index=True)
                worksheet1.update([updated_sheet.columns.values.tolist()] + updated_sheet.values.tolist())
                st.success("Your comment has been submitted and Google Sheets updated.")
            except Exception as e:
                st.error(f"Error updating Google Sheets: {str(e)}")

    with st.expander("Check the Results"):
        if not sheet.empty:
            st.write("Summary Metrics:")
            col1, col2 = st.columns(2)
            col1.metric("Total Submissions", len(sheet))
            col2.metric("Unique Agencies", sheet['Agency'].nunique())
        
        st.table(sheet)

    st.markdown("""
        <footer style="text-align: center; margin-top: 50px;">
            <p>Developed by Office of Commmunity Safety</p>
        </footer>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    app()