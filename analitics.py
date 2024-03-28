import numpy as np


class analizer:
    def __init__(self, wave):
        self.values = wave.result[:, [1]]
        pass
    def mean(self):
        return np.mean(self.values)
    def meanAbs(self):
        return np.mean(abs(self.values))
    def rms(self):
        return np.sqrt(np.mean(self.values**2))
    def variance(self):
        var = 0
        m = self.mean()
        for val in self.values:
            var += (val - m)**2
        var /= len(self.values)
        return val[0]
    def power(self):
        return np.mean(self.values**2)