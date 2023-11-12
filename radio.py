#!/usr/bin/python3

from rtlsdr import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class Radio:

    def __init__(self) -> None:

        self.client = RtlSdrTcpClient(hostname='192.168.30.169', port=12345)
        self.client.center_freq = 618829000   # Radiofyr                
        self.client.sample_rate = 1000000  #1e6
        self.client.bandwidth = 100e3
        self.client.gain = 0
        self._decimation = 64
        self._sample_size = 65536
        self._sample_averages = 5
        self._dec_samples = int(self._sample_size / self._decimation)
        self._butt_b, self._butt_a = signal.butter(6, 0.006)
        self._butt_filter = signal.lfilter_zi(self._butt_b, self._butt_a)

    def average_power(self):
        data_samples = np.ones([self._sample_averages])
        for i in range(self._sample_averages):
            data = self.client.read_samples(self._sample_size)
            data, _ = signal.lfilter(self._butt_b, self._butt_a, data, zi=self._butt_filter * data[0])
            data_dec = signal.decimate(data, self._decimation)
            power = sum(np.abs(data_dec) ** 2)
            data_samples[i] = 10 * np.log10(power)
        return np.mean(data_samples)