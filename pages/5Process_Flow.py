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
image1 = 'PWC_Process.jpg'

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
    worksheet1 = spreadsheet1.worksheet('Comments')
    sheet = pd.DataFrame(worksheet1.get_all_records())
    #st.write(sheet)
except Exception as e:
    st.error(f"Error fetching data from Google Sheets: {str(e)}")


# Streamlit application
def app():
    # Set up the Streamlit page
    #st.set_page_config(page_title='PWC Mapping Dashboard', page_icon='', layout='wide')

    # Use columns for side-by-side layout    
    col1, col2, col3 = st.columns([1,3,1])

    with col1:
        st.write(' ')

    with col2:
        st.image(image, width=450)

    with col3:
        st.write(' ')


    # Set up custom CSS for styling
    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                margin-top: 0px;
                margin-bottom: 20px;
            }
            .content {
                font-size: 18px;
                line-height: 1.6;
                text-align: justify;
                margin: 0 auto;
                max-width: 800px;
            }
            footer {
                text-align: center;
                margin-top: 50px;
                font-size: 14px;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)
    # Centered title
    st.markdown('<div class="title">Process Flow Map</div>', unsafe_allow_html=True)

    st.write("")
    
    st.image(image1)


    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://miro.com/app/board/uXjVLycezdo=/?share_link_id=611706343038" target="_blank" style="text-decoration: none; font-size: 18px; color: blue;">
                Check it in Miro Board
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")

    # Contact Information
    with st.expander("Contact Information"):
        name = st.text_area("What is your name?", key="name")
        agency = st.text_area("What is your agency/department?", key="agency")

    # Submit Your Response
    with st.expander("Submit Your Response"):
        comment1 = st.text_area("Do you have any comments/suggestions on the map?", key="comment1")
    

    # Submit button
    submit_comment = st.button("Submit Comment", key="submit_comment")

    if submit_comment:
        # Prepare the new row
        new_row = {
            'Name': name,
            'Agency': agency,
            'Do you have any comments/suggestions on the map?': comment1
        }
        new_data = pd.DataFrame([new_row])

        try:
            # Append new data to Google Sheet
            updated_sheet = pd.concat([sheet, new_data], ignore_index=True)
            worksheet1.update([updated_sheet.columns.values.tolist()] + updated_sheet.values.tolist())
            st.success("Your comment has been submitted and Google Sheets updated.")
        except Exception as e:
            st.error(f"Error updating Google Sheets: {str(e)}")

    st.write("")        
    st.write("")   

    with st.expander("See the Results Below"):
        if not sheet.empty:
            col1, col2 = st.columns(2)
            col1.metric("Total Submissions", len(sheet))
            col2.metric("Unique Agencies", sheet['Agency'].nunique())
        
        st.table(sheet)

    # Footer Section
    st.markdown("""
        <footer>
            <p>Thank you once again for your participation and attendance!</p>
            <p>Developed by Jiaqin Wu (<a href="mailto:JWu@pwcgov.org">JWu@pwcgov.org</a>) and Dr. Tauheeda Yasin (<a href="mailto:tyasin1@pwcgov.org">tyasin1@pwcgov.org</a>)<br>
            The Office of Community Safety</p>
        </footer>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    app()

    
