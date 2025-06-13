import cv2
import numpy as np
import streamlit as st

class ImageDisplay:
    def __init__(self, img):
        self.original_img = img
        self.img = cv2.resize(img, (0, 0), fx=0.7, fy=0.5)
        self.ft_magnitude = None
        self.ft_phase = None

    def displayImg(self):
        i = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        st.image(i, use_container_width=True)

    def displayComponents(self, component, mode="Grayscale"):
        image = self.img.copy()

        if mode == "Grayscale":
            norm_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
            fft = np.fft.fftshift(np.fft.fft2(norm_img))
            magnitude = np.abs(fft)
            phase = np.angle(fft)
            magnitude = np.log1p(magnitude)
            mag_img = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            phase_img = cv2.normalize(phase, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            self.ft_magnitude = mag_img
            self.ft_phase = phase_img

        elif mode in ["Red", "Green", "Blue"]:
            channel_index = {"Blue": 0, "Green": 1, "Red": 2}[mode]
            single_channel = image[:, :, channel_index].astype(np.float32) / 255.0
            fft = np.fft.fftshift(np.fft.fft2(single_channel))
            magnitude = np.abs(fft)
            phase = np.angle(fft)
            magnitude = np.log1p(magnitude)
            mag_img = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            phase_img = cv2.normalize(phase, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            self.ft_magnitude = mag_img
            self.ft_phase = phase_img

        elif mode == "All Channels":
            mags = []
            phases = []
            for i in range(3):
                channel = image[:, :, i].astype(np.float32) / 255.0
                fft = np.fft.fftshift(np.fft.fft2(channel))
                mag = np.log1p(np.abs(fft))
                pha = np.angle(fft)
                mags.append(cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8))
                phases.append(cv2.normalize(pha, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8))
            self.ft_magnitude = cv2.merge(mags)
            self.ft_phase = cv2.merge(phases)

        if component == "FT Magnitude":
            st.image(self.ft_magnitude, use_container_width=True, clamp=True)
        elif component == "FT Phase":
            st.image(self.ft_phase, use_container_width=True, clamp=True)
