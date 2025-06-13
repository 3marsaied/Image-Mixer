import cv2
import numpy as np

class Mixer:
    def __init__(self, image1, image2, use_img1, use_img2):
        self.image1 = cv2.resize(image1, (0, 0), fx=1, fy=1.2) if use_img1 else image1
        self.image2 = cv2.resize(image2, (0, 0), fx=1, fy=1.2) if use_img2 else image2
        self.size = self.image1.shape[:2] if use_img1 else self.image2.shape[:2]

    def execute(self, imgSel1, imgSel2, compSel1, compSel2, ratio1, ratio2):
        # Select source images
        img_map = {"image 1": self.image1, "image 2": self.image2}
        img1 = img_map[imgSel1]
        img2 = img_map[imgSel2]

        # Compute components
        comp1 = self._compute_component(compSel1, img1)
        comp2 = self._compute_component(compSel2, img2)

        # Initialize magnitude and phase
        fft_shape = np.fft.fft2(self.image1).shape
        mag = np.zeros(fft_shape)
        phase = np.zeros(fft_shape)

        # Mix components
        if compSel1 == "mag":
            mag = (ratio1 / 100) * comp1
        elif compSel1 == "phase":
            phase = (ratio1 / 100) * comp1

        if compSel2 == "mag":
            mag = (ratio2 / 100) * comp2
        elif compSel2 == "phase":
            phase = (ratio2 / 100) * comp2

        # Construct mixed FFT and inverse transform
        mixed_fft = np.multiply(mag, np.exp(1j * phase))
        img_out = np.fft.ifft2(np.fft.ifftshift(mixed_fft))
        img_out = np.uint8(np.clip(np.real(img_out), 0, 255))

        # Resize output image
        out_h, out_w = self._get_output_dimensions()
        return cv2.resize(img_out, (out_w, out_h))

    def _compute_component(self, name, image):
        fft = np.fft.fftshift(np.fft.fft2(image))
        if name == "mag":
            return np.abs(fft)
        elif name == "phase":
            return np.angle(fft)

    def _get_output_dimensions(self):
        h, w = self.size
        aspect_ratio = w / h
        if aspect_ratio >= 1:
            return h, int(h * aspect_ratio)
        else:
            return int(w / aspect_ratio), w
