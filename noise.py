import numpy as np
import random

class noise:
    def __init__(self, A, d):
        self.amplitude = A
        self.time = d
        self.result = None
    def __str__(self):
        return f'amplitude = {self.amplitude}; phase = {self.phase}; time = {self.time}'

class linearNoise(noise):
    def __init__(self, A, d):
        super().__init__(A, d)
    def __str__(self):
        return super().__str__()
    def random(self):
        return random.uniform(-self.amplitude, self.amplitude)
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = t*probeTime
            result[t][1] = self.random()
        self.result = result
        return result
    
class gaussianNoise(noise):
    def __init__(self, A, d):
        super().__init__(A, d)
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = t*probeTime
            result[t][1] = self.amplitude*np.random.normal()
        self.result = result
        return result