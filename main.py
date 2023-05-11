import streamlit as st
import logging
from mixer import *
from imagDisplay import *
from stSpace import *


st.set_page_config(
    page_title="FT Magnitude & phase Mixer",
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
col1, col2, col3, col4 = st.columns((1, 1, 1, 1), gap="small")

def main():

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %I:%M:%S", filename="logs.log", filemode="w")
    logging.info('Application started.')

    image1 = st.sidebar.file_uploader("Upload Image 1", type=["jpg", "jpeg", "png"])
    image2 = st.sidebar.file_uploader("Upload Image 2", type=["jpg", "jpeg", "png"])
    options = ["FT Magnitude", "FT Phase", "FT Real component", "FT Imaginary component"]
    selectionOptions = ["image 1","image 2"]
    img1 = None
    img2 = None
    if image1:
        logging.info("image 1 uploaded.")
        image1 = cv2.imdecode(np.fromstring(image1.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
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
            img1Display.displayComponents(component1)
            logging.info(f"image with component {component1} is desplayed.")
            img1 = True

    if image2:
        logging.info("image 2 uploaded.")
        image2 = cv2.imdecode(np.fromstring(image2.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        img2Display = ImageDisplay(image2)

        with col1:
            newLines(5)
            st.write("<p style='font-size:45px; text-align: center;'><b>Image2</b></p>", unsafe_allow_html=True)
            img2Display.displayImg()
            logging.info("image 2 displayed.")

        with col2:
            newLines(5)
            # if img1_display.img.shape != img2_display.img.shape:
            #     st.error("Images have different sizes")
            # else:
            component2 = st.selectbox(
                f"Select component to display (Image 2)", 
                options,
                key=f"{image2}_component"
            )
            logging.info(f"{component2} is selected.")
            img2Display.displayComponents(component2)
            logging.info(f"image with component {component2} is desplayed.")
            img2 = True

    if img1 or img2:
        with col3:
            st.write("<p style='font-size:45px; text-align: center;'><b>Mixer output to:</b></p>", unsafe_allow_html=True)
        with col4:
            outputSelection = st.selectbox("Select which output to use",["output 1","output 2"])
            logging.info(f"{outputSelection} is selected.")
        with col4:
            st.write("")
            slider1 = st.slider("", min_value=0, max_value=100, step=1, value=0, 
                     format="%d%%", help="Progress bar slider", key = "slider1")
            logging.info(f"slider 1 value is {slider1}")
        with col3:
            cl1,cl2 = st.columns((1, 1), gap="small")
            with cl1:
                newLines(3)
                st.write("<p style='font-size:21px; text-align: center;'><b>Component 1</b></p>", unsafe_allow_html=True)
            with cl2:
                st.write("")
                mixerImgSelection1 = st.selectbox(
                    f"Select which image to use", 
                    selectionOptions,
                    key=f"selection1"
                )
                logging.info(f"{mixerImgSelection1} selected to be modified in component 1")
                st.write("")
                with cl2, col4:
                    option1 = st.selectbox("",["mag","phase","real","imag","unformMag","unformPhase"], key = "option1" )
                    logging.info(f"component '{option1}' is selected to be modified.")
        with col4:
            slider2 = st.slider("", min_value=0, max_value=100, step=1, value=0, 
                     format="%d%%", help="Progress bar slider",key="slider2")
            logging.info(f"slider 2 value is {slider2}")
            with cl1:
                newLines(8)
                st.write("<p style='font-size:21px; text-align: center;'><b>Component 2</b></p>", unsafe_allow_html=True)
            with cl2:
                newLines(5)
                mixerImgSelection2 = st.selectbox(
                    f"Select which image to use", 
                    selectionOptions,
                    key=f"selection2"  
                )
                logging.info(f"{mixerImgSelection2} selected to be modified in component 2")
                with cl2, col4:
                    option2 = st.selectbox("",["mag","phase","real","imag","unformMag","unformPhase"], key = "option2")
                    logging.info(f"component '{option2}' is selected to be modified.")

        Mixer = mixer(image1,image2,img1,img2)               
        outputImage = Mixer.excute(mixerImgSelection1,mixerImgSelection2,option1,option2,slider1,slider2)
        logging.info("Mixer excutable function called.")
        with col3:
            newLines(9)
            if outputSelection == "output 1":
                st.image(outputImage, use_column_width=True)
                out1 = outputImage
                logging.info("output 1 displayed")        
        with col4:
            newLines(2)
            if outputSelection == "output 2":
                st.image(outputImage, use_column_width=True)
                out2 = outputImage
                logging.info("output 2 displayed.")

        

if __name__ == "__main__":
    main()
