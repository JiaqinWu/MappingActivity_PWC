import streamlit as st
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Image file path
image = "PWC.jpg"

# Streamlit application
def app():
    # Use columns for side-by-side layout    
    col1, col2, col3 = st.columns([1,4,1])

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
                margin-top: 20px;
                margin-bottom: 40px;
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


    # Title Section
    st.markdown('<div class="title">Introduction</div>', unsafe_allow_html=True)

    # Content Section
    st.markdown("""
        <div class="content">
            This dashboard is based on the meeting held on December 4, 2024. During that meeting, we focused on developing a coordinated response mapping across multiple agencies within the county. 
            The primary goal was for each agency to provide an overview of their work, enabling the creation of a shared map of current resources and processes. Building on the responses from the last survey, 
            this follow-up meeting aims to identify pain points, explore areas for improvement, and enhance opportunities for collaboration between agencies. This dashboard is designed to gather input from 
            four key angles: framework, information sharing, referral processes, and next steps.
        </div>
    """, unsafe_allow_html=True)

    # Footer Section
    st.markdown("""
        <footer>
            <p>Thank you once again for your participation and attendance!</p>
            <p>Developed by Jiaqin Wu (<a href="mailto:JWu@pwcgov.org">JWu@pwcgov.org</a>) and Dr. Tauheeda Yasin (<a href="mailto:tyasin1@pwcgov.org">tyasin1@pwcgov.org</a>)<br>
            The Office of Community Safety</p>
        </footer>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    app()
