#!/usr/bin/python3

from rtlsdr import *
import matplotlib.pyplot as plt
import numpy as np
    
class Radio:
    def __init__(self) -> None:
        self.client = RtlSdrTcpClient(hostname='192.168.30.169', port=12345)
        self.client.center_freq = 1038000000  # astra 1m
        self.client.sample_rate = 1500000  # 1e6
        self.client.bandwidth = 500e3

    def average_power(self):
        data = self.client.read_samples(1024*256)
        #data = np.fft.fft(data)
        power = sum(np.abs(data)**2)
        power = 20*np.log10(power)
        return power
        
        