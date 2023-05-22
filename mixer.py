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
            self.image1 = cv2.resize(self.image1, (0, 0), fx=1, fy=1.2)
        if self.img2:
            self.size = self.image2.shape[:2]
            self.image2 = cv2.resize(self.image2, (0, 0), fx=1, fy=1.2)
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
            component1 = self.calculate(component_selector_1, self.image1)
            component2 = self.calculate(component_selector_2, self.image2)
        
        elif image_selector_1 == "image 1" and image_selector_2 == "image 1":
            # Calculate the selected components of the Fourier transforms of the images
            component1 = self.calculate(component_selector_1, self.image1)
            component2 = self.calculate(component_selector_2, self.image1)
        
        elif image_selector_1 == "image 2" and image_selector_2 == "image 2":
            # Calculate the selected components of the Fourier transforms of the images
            component1 = self.calculate(component_selector_1, self.image2)
            component2 = self.calculate(component_selector_2, self.image2)

        elif image_selector_1 == "image 2" and image_selector_2 == "image 1":
            component1 = self.calculate(component_selector_1, self.image2)
            component2 = self.calculate(component_selector_2, self.image1)


        magComponent = np.fft.fftshift(np.zeros_like(np.fft.fft2(self.image1)))
        phaseComponent = np.fft.fftshift(np.zeros_like(np.fft.fft2(self.image1)))
        mixed_component_imag_inverse = np.fft.fftshift(np.zeros_like(np.fft.fft2(self.image1)))
        mixed_component_real_inverse = np.fft.fftshift(np.zeros_like(np.fft.fft2(self.image1))) 

        if component_selector_1 == "mag":
            magComponent = component1
            magComponent = (ratio1 / 100) * magComponent 
        if component_selector_2 == "mag":
            magComponent = component2
            magComponent = (ratio2 / 100) * magComponent
        if component_selector_1 == "phase" or component_selector_1 =="uniformPhase":
            phaseComponent = component1
            phaseComponent = (ratio1 / 100) * phaseComponent
        if component_selector_2 == "phase" or component_selector_2 =="uniformPhase":
            phaseComponent = component2
            phaseComponent = (ratio2 / 100) * phaseComponent
        if component_selector_1 =="uniformMag":
            magComponent = component1
        if  component_selector_2 =="uniformMag":
            magComponent = component2



        if component_selector_1 == "real" :
            mixed_component_real_inverse = component1
            mixed_component_real_inverse = (ratio1 / 100) * mixed_component_real_inverse 
        if component_selector_2 == "real":
            mixed_component_real_inverse = component2
            mixed_component_real_inverse = (ratio2 / 100) * mixed_component_real_inverse
        if component_selector_1 == "imag":
            mixed_component_imag_inverse = component1
            mixed_component_imag_inverse = (ratio1 / 100) * mixed_component_imag_inverse  
        if component_selector_2 == "imag":
            mixed_component_imag_inverse = component2
            mixed_component_imag_inverse = (ratio2 / 100) * mixed_component_imag_inverse

            
        if (component_selector_1 == "real" and component_selector_2 == "imag") or (component_selector_2 == "real" and component_selector_1 == "imag") or (component_selector_1 == "real" and component_selector_2 == "real") or (component_selector_1 == "imag" and component_selector_2 == "imag"):
            # Combine the real and imaginary parts to obtain the reconstructed image
            mixed_component = mixed_component_real_inverse + 1j *( mixed_component_imag_inverse)
            reconstructed_image = np.fft.ifft2(np.fft.ifftshift(mixed_component))
            output_image = np.uint8(np.real(reconstructed_image)) # cast the real part of the resulting array to an 8-bit unsigned integer
            output_image = cv2.resize(output_image, (output_width, output_height))
            return output_image
        
        else:
            # Mix the components based on the selected mix ratio
            mixed_component = np.multiply(( magComponent), np.exp(1j *( phaseComponent)))
            # Convert the mixed component back to an image and display it
            mixed_component_shifted = np.fft.ifftshift(mixed_component) # shift the zero-frequency component to the center of the array
            mixed_component_inverse = np.fft.ifft2(mixed_component_shifted) # perform the inverse Fourier transform
            output_image = np.uint8(np.real(mixed_component_inverse)) # cast the real part of the resulting array to an 8-bit unsigned integer
            output_image = cv2.resize(output_image, (output_width, output_height))
            return output_image


    def calculate(self, component_name, image):
        # Calculate the selected component of the Fourier transform of the image
        if component_name == "mag":
            component = np.fft.fftshift(np.abs(np.fft.fft2(image)))
        elif component_name == "phase":
            component = np.fft.fftshift(np.angle(np.fft.fft2(image)))
        elif component_name == "real":
            component = np.fft.fftshift(np.real(np.fft.fft2(image)))
        elif component_name == "imag":
            component = np.fft.fftshift(np.imag(np.fft.fft2(image)))
        elif component_name == "uniformMag":
            component = np.fft.fftshift(np.abs(np.fft.fft2(image)))
        elif component_name == "uniformPhase":
            component = np.fft.fftshift(np.zeros_like(np.fft.fft2(image)))

        return component


   
