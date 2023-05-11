import cv2
import numpy as np
import streamlit as st

class ImageDisplay:
    def __init__(self, img):
        self.img = img
        self.ft_magnitude = None
        self.ft_phase = None
        self.ft_real = None
        self.ft_imaginary = None
        self.size = self.img.shape[:2]
        # Resize the image to a smaller size
        self.img = cv2.resize(self.img, (0, 0), fx=0.7, fy=0.5)

    def displayImg(self):
        st.image(self.img, use_column_width=True)

    def displayComponents(self, component):
        # Normalize pixel values
        self.img = self.img / np.max(self.img)
        if self.ft_magnitude is None:
            self.ft_magnitude = np.fft.fftshift(np.abs(np.fft.fft2(self.img)))
        if self.ft_phase is None:
            self.ft_phase = np.fft.fftshift(np.angle(np.fft.fft2(self.img)))
        if self.ft_real is None:
            self.ft_real = np.fft.fftshift(np.real(np.fft.fft2(self.img)))
        if self.ft_imaginary is None:
            self.ft_imaginary = np.fft.fftshift(np.imag(np.fft.fft2(self.img)))
        if component == "FT Magnitude":
            st.image(self.ft_magnitude, use_column_width=True, clamp=True)
        elif component == "FT Phase":
            st.image(self.ft_phase, use_column_width=True, clamp=True)
        elif component == "FT Real component":
            st.image(self.ft_real, use_column_width=True, clamp=True)
        elif component == "FT Imaginary component":
            st.image(self.ft_imaginary, use_column_width=True, clamp=True)

