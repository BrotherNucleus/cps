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
    def squareDiff(self, wave):
        retsum = 0
        for i in range(len(wave)):
            # print(self.values[i*N])
            # print(wave.func(self.xs[i]))
            # print(np.square(self.values[i*N] + res2[i]))
            retsum += np.square(self.values[i*N] - wave[i])
        return retsum
    def MSE(self, wave):
        res2 = wave.result[:, [1]]
        retsum = self.squareDiff(res2)
        retsum /= (len(res2))
        print(retsum)
        return retsum[0]
    def SNR(self, wave):
        res2 = wave.result[:, [1]]
        nop = self.squareDiff(res2)
        sip = np.sum(np.square(res2))
        snr = 10 * np.log10(sip/nop)
        return snr[0]
    def MD(self, wave):
        res2 = wave.result[:, [1]]
        vals = np.zeros(len(res2))
        for i in range(len(res2)):
            vals[i]=self.values[i*N]
        diff = np.zeros(len(res2))
        for i in range(len(diff)):
            diff[i] = abs(res2[i] - vals[i])
        return np.max(diff)



