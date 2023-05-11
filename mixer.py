import streamlit as st
import cv2
import numpy as np

class mixer:
    
    def __init__(self, image1, image2, img1, img2):
        self.image1 = image1
        self.image2 = image2
        self.img1 = img1
        self.img2 = img2
        if self.img1:
            self.size = self.image1.shape[:2]
            self.image1 = cv2.resize(self.image1, (0, 0), fx=0.7, fy=0.51)
        if self.img2:
            self.size = self.image2.shape[:2]
            self.image2 = cv2.resize(self.image2, (0, 0), fx=0.7, fy=0.51)
        self.output_images = [None, None]

    def excute(self, imgSelector1, imgSelector2, componentSelector1, componentSelector2, ratio1, ratio2):
        # Load the selected images
        image_selector_1 = imgSelector1
        image_selector_2 = imgSelector2
        component_selector_1 = componentSelector1
        component_selector_2 = componentSelector2
        ratio_1 = ratio1
        ratio_2 = ratio2
        aspect_ratio_1 = 0.0
        aspect_ratio_2 = 0.0
        # Calculate the aspect ratio of the images
        if self.img1:
            aspect_ratio_1 = self.image1.shape[1] / self.image1.shape[0]
        if self.img2:
            aspect_ratio_2 = self.image2.shape[1] / self.image2.shape[0]

        # Calculate the dimensions of the output image
        if aspect_ratio_1 > aspect_ratio_2:
            output_height = int(self.size[0] / aspect_ratio_1)
            output_width = self.size[0]
        else:
            output_height = self.size[1]
            output_width = int(self.size[1] * aspect_ratio_2)

        # Mix the images and display the output
        if image_selector_1 == "image 1" and image_selector_2 == "image 2":
            # Calculate the selected components of the Fourier transforms of the images
            component1 = self.calculate(component_selector_1, self.image1,ratio1)
            component2 = self.calculate(component_selector_2, self.image2,ratio2)
        elif image_selector_1 == "image 1" and image_selector_2 == "image 1":
            # Calculate the selected components of the Fourier transforms of the images
            component1 = self.calculate(component_selector_1, self.image1,ratio1)
            component2 = self.calculate(component_selector_2, self.image1,ratio1)
        elif image_selector_2 == "image 2" and image_selector_2 == "image 2":
            # Calculate the selected components of the Fourier transforms of the images
            component1 = self.calculate(component_selector_1, self.image2,ratio2)
            component2 = self.calculate(component_selector_2, self.image2,ratio2)

        # Mix the components based on the selected mix ratio
        mixed_component = (ratio_1 / 100) * component1 + (ratio_2 / 100) * component2

        # Convert the mixed component back to an image and display it
        output_image = np.uint8(np.fft.ifft2(np.fft.ifftshift(mixed_component)).real)
        output_image = cv2.resize(output_image, (output_width, output_height))
        return output_image



    def calculate(self, component_name, image, ratio):
        # Calculate the selected component of the Fourier transform of the image
        if component_name == "mag":
            component = np.fft.fftshift(np.fft.fft2(image))
            component = np.abs(component)
        elif component_name == "phase":
            component = np.fft.fftshift(np.fft.fft2(image))
            component = np.angle(component)
        elif component_name == "real":
            component = np.fft.fftshift(np.fft.fft2(image))
            component = np.real(component)
        elif component_name == "imag":
            component = np.fft.fftshift(np.fft.fft2(image))
            component = np.imag(component)
        elif component_name == "unformMag":
            component = np.ones_like(image)
        elif component_name == "unformPhase":
            component = np.zeros_like(image)

        # Modify the component based on the ratio
        if ratio < 0:
            ratio = 0
        elif ratio > 100:
            ratio = 100
        ratio = ratio / 100
        if component_name in ["mag", "real"]:
            component *= ratio
        elif component_name in ["phase", "imag"]:
            component *= (1 - ratio)
        
        return component

