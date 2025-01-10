import streamlit as st
import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')
from PIL import Image
import os


# Import the dataset
image = "PWC.jpg"


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
    st.markdown('<div class="title">Power BI Dashboard</div>', unsafe_allow_html=True)

    #st.markdown("### Mapping Dashboard")
    

    # Folder where your slides are saved
    slide_folder = 'Slides'

    # Custom sorting function to ensure slides are ordered numerically
    def sorted_nicely(l):
        """Sort the given list in the way that humans expect."""
        import re
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)

    # Collect slide paths and ensure they are sorted correctly
    slides = sorted_nicely([os.path.join(slide_folder, f) for f in os.listdir(slide_folder) if f.endswith('.png')])

    # Initialize session state to track the current slide index
    if 'slide_index' not in st.session_state:
        st.session_state.slide_index = 0

    # Function to update the slide index
    def next_slide():
        if st.session_state.slide_index < len(slides) - 1:
            st.session_state.slide_index += 1

    def previous_slide():
        if st.session_state.slide_index > 0:
            st.session_state.slide_index -= 1

    # Add navigation buttons
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("Previous"):
            previous_slide()

    with col3:
        if st.button("Next"):
            next_slide()

    # Ensure slide index is properly displayed and updated in the center
    current_slide_number = st.session_state.slide_index + 1
    total_slides = len(slides)
    with col2:
        st.markdown(f"<h3 style='text-align: center;'>Slide {current_slide_number} of {total_slides}</h3>", unsafe_allow_html=True)

    # Display the current slide
    slide = Image.open(slides[st.session_state.slide_index])
    st.image(slide, use_container_width=True)


    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <a href="http://imtw-doitbi-01/PBIReports/powerbi/Executive%20Management/Mapping_Dashboard" target="_blank" style="text-decoration: none; font-size: 18px; color: blue;">
                Check the interactive Power BI Dashboard
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    



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

    
