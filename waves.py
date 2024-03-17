import numpy as np
import matplotlib.pyplot as plt

eps = 6e-10
class Wave:
    def __init__(self, A, f, d, phi):
        self.amplitude = A
        self.frequency = f
        self.time = d
        self.phase = phi
    def __str__(self):
        return f'A = {self.amplitude}, freq = {self.frequency}, phi = {self.phase}'
class SinWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            test = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
            if(abs(test) < eps):
                result[t][1] = 0
            else:
                result[t][1] = test
        self.res = result
        return result
    def __str__(self):
        return f'{self.amplitude} * sin(2*PI*{self.frequency} * (t - {self.phase})'

class SinHalfWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            test = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
            result[t][0] = probeTime * t
            if(test < 0 or abs(test) < eps):
                result[t][1] = 0
            else:
                result[t][1] = test
        self.res = result
        return result
    def __str__(self):
        return f'{self.amplitude} * sin(2*PI*{self.frequency} * (t - {self.phase})'

class SinModWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            test = abs(self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase)))
            if(test < eps):
                result[t][1] = 0
            else:
                result[t][1] = test
        self.res = result
        return result

class SquareWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            test = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
            if(test < eps):
                result[t][1] = 0
            elif(test > 0):
                result[t][1] = self.amplitude
            else:
                result[t][1] = 0
        self.res = result
        return result

class SymSquareWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            test = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
            if(test > 0):
                result[t][1] = self.amplitude
            else:
                result[t][1] = -self.amplitude
        self.res = result
        return result    

class TriangleWave(Wave):
    def __init__(self, A, f, d, phi, k):
        self.coeff = k
        super().__init__(A, f, d, phi)
    def __str__(self):
        return super().__str__() + f' Coefficient: {self.coeff}'
    def calculate(self, p):
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            currT = np.floor(probeTime * t * self.frequency)
            up = np.logical_and(currT / self.frequency + self.phase <= probeTime*t, 
                                probeTime*t < self.coeff / self.frequency + currT /self.frequency + self.phase)
            
            down = np.logical_and(self.coeff / self.frequency + currT / self.frequency + self.phase <= t,
                                               t <= (currT + 1) / self.frequency + self.phase)

            if up:
                result[t][1] = (self.amplitude*self.frequency) / self.coeff * (probeTime*t - currT / self.frequency - self.phase)
            elif down:
                result[t][1] = (-self.amplitude * self.frequency) / (1 - self.coeff) * (probeTime*t - currT / self.frequency - self.phase) + (self.amplitude/(1 - self.coeff))
            else:
                result[t][1] = 0
        self.res = result
        plt.style.use('_mpl-gallery')

        # make data
        x = result[:, [0]]
        y = result[:, [1]]

        # plot
        fig, ax = plt.subplots()

        ax.plot(x, y, linewidth=2.0)

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 8), yticks=np.arange(1, 8))

        plt.show()
        return result    