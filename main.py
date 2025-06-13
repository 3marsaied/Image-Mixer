import streamlit as st
import logging
from UI.DFT import DFT_UI
from UI.harris_UI import Harris_UI
from harris import *



st.set_page_config(
    page_title="Harris Corner Detector and DFT",
    page_icon="./icons/picture.png",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
#MainMenu
{
    visibility: hidden;
}
.css-10pw50.egzxvld1 
{
    visibility: hidden;
}
 </style>
""", unsafe_allow_html=True)

# Divide the page into two columns
col, col_= st.columns((1, 1), gap="small")
with col:
    col1, col2 = st.columns((1, 1), gap="small")
with col_:
    col3, col4 = st.columns((1, 1), gap="small")

def main():

    # Initialize session state if it doesn't exist
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = "Harris"

    # Create horizontal radio buttons that look like a switch
    st.sidebar.radio(
        "Select detection method:",
        options=["Harris", "DFT"],
        key="selected_option",
        horizontal=True,
        label_visibility="visible"
    )

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %I:%M:%S", filename="logs.log", filemode="w")
    logging.info('Application started.')

    if st.session_state.selected_option == "DFT":
        DFT_UI(col, col_)
    else:
        Harris_UI(col, col_)

if __name__ == "__main__":
    main()
