import numpy as np

N = 5

class analizer:
    def __init__(self, wave):
        self.values = wave.result[:, [1]]
        self.xs = wave.result[:,[0]]
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
    def MSE(self, wave):
        retsum = 0
        res2 = wave.result[:, [1]]
        for i in range(len(res2)):
            print(self.values[i*N])
            print(res2[i])
            print(np.square(self.values[i*N] + res2[i]))
            retsum += np.square(self.values[i*N] + res2[i])
        retsum /= (len(res2))
        print(retsum)
        return retsum[0]
