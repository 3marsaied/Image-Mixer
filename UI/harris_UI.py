import logging
import cv2
import numpy as np
import streamlit as st

from harris import harrisCornerDetector

def Harris_UI(col, col_):
    if 'harris_params' not in st.session_state:
        st.session_state.harris_params = {
            "threshold": 0.01,
            "window_size": 3,
            "k": 0.04,
            "nms_window": 3
        }

    image = st.sidebar.file_uploader("Upload Image 1", type=["jpg", "jpeg", "png"])
    
    if image is not None:
        logging.info("image 1 uploaded.")
        file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        with col:
            st.write("<p style='font-size:45px; text-align: center;'><b>Image1</b></p>", unsafe_allow_html=True)
            logging.info("image 1 displayed.")
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            st.image(image_rgb, caption="Uploaded Image", use_container_width=True)

        with st.sidebar.expander("Harris Parameters"):
            st.session_state.harris_params["threshold"] = st.slider("Threshold", 0.001, 0.1, 0.01, 0.001)
            st.session_state.harris_params["window_size"] = st.slider("Window Size", 3, 15, 3, 2)
            st.session_state.harris_params["k"] = st.slider("k value", 0.01, 0.2, 0.04, 0.01)
            st.session_state.harris_params["nms_window"] = st.slider("NMS Window", 3, 15, 3, 2)
        
        # Compute Harris corners (now using single return value)
        harris_result = harrisCornerDetector(
            image,
            st.session_state.harris_params["threshold"],
            st.session_state.harris_params["window_size"],
            st.session_state.harris_params["k"],
            st.session_state.harris_params["nms_window"]
        )
        
        # Convert to RGB for display
        harris_result_rgb = cv2.cvtColor(harris_result, cv2.COLOR_BGR2RGB)
    
        with col_:
            st.write("<p style='font-size:45px; text-align: center;'><b>Detected Corners</b></p>", unsafe_allow_html=True)
            st.image(harris_result_rgb, use_container_width=True, clamp=True)

    return None