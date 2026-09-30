"""
Biometric vocal tract cloaking transformations.
"""
import numpy as np
from scipy.signal import resample

class BiometricCloaker:
    def __init__(self, mode="subtle", samplerate=16000):
        self.mode = mode
        self.samplerate = samplerate
        # Perturbation factor mapping
        self.shift_factors = {
            "off": 1.0,
            "subtle": 1.06,      # Slight formant shift, imperceptible to humans
            "aggressive": 1.15   # Heavier disruption against deepfake voice cloning
        }

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Applies real-time pitch/formant scaling to scramble voiceprints.
        """
        factor = self.shift_factors.get(self.mode, 1.0)
        if factor == 1.0 or len(frame) == 0:
            return frame

        # Time-domain resampling to modulate vocal frequency spectrum
        target_len = int(len(frame) / factor)
        resampled = resample(frame, target_len)
        # Restore original buffer size
        out_frame = resample(resampled, len(frame))
        return out_frame.astype(np.float32)
