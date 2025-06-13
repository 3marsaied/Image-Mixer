import streamlit as st
import logging
from mixer import *
from imagDisplay import *
from stSpace import newLines
import cv2
from utils import resize_by_height

def DFT_UI(col, col_):
    with col:
        col1, col2 = st.columns((1, 1), gap="small")
    with col_:
        col3, col4 = st.columns((1, 1), gap="small")

    image1 = st.sidebar.file_uploader("Upload Image 1", type=["jpg", "jpeg", "png"])
    image2 = st.sidebar.file_uploader("Upload Image 2", type=["jpg", "jpeg", "png"])
    options = ["FT Magnitude", "FT Phase"]
    selectionOptions = ["image 1", "image 2"]
    img1 = None
    img2 = None
    component_mode = st.sidebar.selectbox(
        "Component mode",
        ["Grayscale", "All Channels", "Red", "Green", "Blue"],
        key="component_mode"
    )

    output_mode = st.sidebar.selectbox(
        "Output mode",
        ["Grayscale", "Colored"],
        key="output_mode"
    )

    if image1:
        logging.info("image 1 uploaded.")
        file_bytes = np.asarray(bytearray(image1.read()), dtype=np.uint8)
        image1 = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img1Display = ImageDisplay(image1)

        with col1:
            st.write("<p style='font-size:45px; text-align: center;'><b>Image1</b></p>", unsafe_allow_html=True)
            img1Display.displayImg()
            logging.info("image 1 displayed.")

        with col2:
            component1 = st.selectbox(
                f"Select component to display (Image 1)",
                options,
                key=f"{image1}_component"
            )
            logging.info(f"{component1} is selected.")
            img1Display.displayComponents(component1, component_mode)
            logging.info(f"image with component {component1} is displayed.")
            img1 = True

    if image2:
        logging.info("image 2 uploaded.")
        file_bytes = np.asarray(bytearray(image2.read()), dtype=np.uint8)
        image2 = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img2Display = ImageDisplay(image2)

        with col3:
            if img1Display.img.shape != img2Display.img.shape:
                st.error("Images have different sizes")
            else:
                st.write("<p style='font-size:45px; text-align: center;'><b>Image2</b></p>", unsafe_allow_html=True)
                img2Display.displayImg()
                logging.info("image 2 displayed.")

        with col4:
            if img1Display.img.shape != img2Display.img.shape:
                st.error("Images have different sizes")
            else:
                component2 = st.selectbox(
                    f"Select component to display (Image 2)",
                    options,
                    key=f"{image2}_component"
                )
                logging.info(f"{component2} is selected.")
                img2Display.displayComponents(component2, component_mode)
                logging.info(f"image with component {component2} is displayed.")
                img2 = True

    if img1 or img2:
        with col2:
            st.write("<p style='font-size:45px; text-align: center; padding: 45px;'><b></b></p>", unsafe_allow_html=True)

            slider1 = st.slider("", min_value=0, max_value=100, step=1, value=50,
                                format="%d%%", help="Progress bar slider", key="slider1")
            logging.info(f"slider 1 value is {slider1}")
        with col1:
            st.write("<p style='font-size:45px; text-align: center;'><b>Mixer output to:</b></p>", unsafe_allow_html=True)
            st.write("<p style='font-size:21px; text-align: center; padding: 15px'><b></b></p>", unsafe_allow_html=True)
            st.write("<p style='font-size:21px; text-align: center;'><b>Component 1</b></p>", unsafe_allow_html=True)
            st.write("")
            mixerImgSelection1 = st.selectbox(
                f"Select which image to use",
                selectionOptions,
                key=f"selection1"
            )
            logging.info(f"{mixerImgSelection1} selected to be modified in component 1")
            st.write("")
            with col2:
                option1 = st.selectbox("", ["mag", "phase"], key="option1")
                logging.info(f"component '{option1}' is selected to be modified.")
        with col2:
            slider2 = st.slider("", min_value=0, max_value=100, step=1, value=50,
                                format="%d%%", help="Progress bar slider", key="slider2")
            logging.info(f"slider 2 value is {slider2}")

        with col1:
            st.write("<p style='font-size:21px; text-align: center; padding: 15px;'><b>Component 2</b></p>", unsafe_allow_html=True)
            mixerImgSelection2 = st.selectbox(
                f"Select which image to use",
                selectionOptions,
                key=f"selection2"
            )
            logging.info(f"{mixerImgSelection2} selected to be modified in component 2")
            with col2:
                option2 = st.selectbox("", ["mag", "phase"], key="option2")
                logging.info(f"component '{option2}' is selected to be modified.")

        mixer = Mixer(image1, image2, img1, img2)
        outputImage = mixer.execute(mixerImgSelection1, mixerImgSelection2, option1, option2, slider1, slider2)
        logging.info("Mixer execute function called.")
        with col_:
            if output_mode == "Colored":
                st.write("<p style='font-size:45px; text-align: center;'><b>Mixer Output</b></p>", unsafe_allow_html=True)
                
                # Convert from BGR to RGB (if needed)
                rgb_output = cv2.cvtColor(outputImage, cv2.COLOR_BGR2RGB)

                # Resize (example: limit height to 400px)
                resized_output = resize_by_height(rgb_output, 400)

                st.image(resized_output, caption="Mixer Output")
            else:
                st.write("<p style='font-size:45px; text-align: center;'><b>Mixer Output</b></p>", unsafe_allow_html=True)

                # Convert to Grayscale
                gray_output = cv2.cvtColor(outputImage, cv2.COLOR_BGR2GRAY)

                # Resize (limit height to 400px)
                resized_output = resize_by_height(gray_output, 400)

                # Display grayscale image
                st.image(resized_output, caption="Mixer Output", use_container_width=True, clamp=True)
