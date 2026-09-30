"""
Audio stream management and WASAPI device interception.
"""
import sounddevice as sd
import numpy as np

class AudioStreamManager:
    def __init__(self, samplerate=16000, blocksize=160, channels=1):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.stream = None

    def list_devices(self):
        """Prints available input and output devices."""
        print(sd.query_devices())

    def start_stream(self, callback):
        """
        Starts full-duplex low-latency audio stream.
        Calls `callback(indata, outdata, frames, time, status)` per frame block.
        """
        self.stream = sd.Stream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            channels=self.channels,
            dtype="float32",
            callback=callback
        )
        self.stream.start()
        return self.stream

    def stop_stream(self):
        """Stops and cleans up the active audio stream."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
