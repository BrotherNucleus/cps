import numpy as np
import noise
import impulse

eps = 6e-10
class Wave:
    def __init__(self, A, f, d, phi):
        self.amplitude = A
        self.frequency = f
        self.time = d
        self.phase = phi
        self.result = None
        self.probeNum = 0
    def __str__(self):
        return f'A = {self.amplitude}, freq = {self.frequency}, phi = {self.phase}'
    def __add__(self, other):
        if(other.result.shape == self.result.shape):
            wave = Wave(self.amplitude + other.amplitude, self.frequency, self.time, self.phase)
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] + other.result[i][1]
            wave.result = res
            return wave
        else:
            print(f"Error: cannot add two diffrently shaped arrays: ({self.result.shape}) + ({other.result.shape})")
    def __mul__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == noise.linearNoise or type(other) == noise.gaussianNoise or self.frequency > other.frequency):
                f = self.frequency
            else:
                f = other.frequency
            
            wave = Wave(self.amplitude*other.amplitude, f, self.time, self.phase)
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] * other.result[i][1]
            wave.result = res
            return wave
    def __truediv__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == noise.linearNoise or type(other) == noise.gaussianNoise or self.frequency > other.frequency):
                f = self.frequency
            else:
                f = other.frequency
            
            wave = Wave(self.amplitude*other.amplitude, f, self.time, self.phase)
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                if abs(other.result[i][1]) > 0.2:
                    res[i][1] = self.result[i][1] / other.result[i][1]
                else:
                    res[i][1] = 0
            wave.result = res
            return wave


class SinWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        self.probeNum = p
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            test = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
            if(abs(test) < eps):
                result[t][1] = 0
            else:
                result[t][1] = test
        self.result = result
        return result
    def __str__(self):
        return f'{self.amplitude} * sin(2*PI*{self.frequency} * (t - {self.phase})'

class SinHalfWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        self.probeNum = p
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            test = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
            result[t][0] = probeTime * t
            if(test < 0 or abs(test) < eps):
                result[t][1] = 0
            else:
                result[t][1] = test
        self.result = result
        return result
    def __str__(self):
        return f'{self.amplitude} * sin(2*PI*{self.frequency} * (t - {self.phase})'

class SinModWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        self.probeNum = p
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            test = abs(self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase)))
            if(test < eps):
                result[t][1] = 0
            else:
                result[t][1] = test
        self.result = result
        return result

class SquareWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        self.probeNum = p
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
        self.result = result
        return result

class SymSquareWave(Wave):
    def __init__(self, A, f, d, phi):
        super().__init__(A, f, d, phi)
    def calculate(self, p):
        self.probeNum = p
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            test = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
            if(test > 0):
                result[t][1] = self.amplitude
            else:
                result[t][1] = -self.amplitude
        self.result = result
        return result    

class TriangleWave(Wave):
    def __init__(self, A, f, d, phi, k):
        self.coeff = k
        super().__init__(A, f, d, phi)
    def __str__(self):
        return super().__str__() + f' Coefficient: {self.coeff}'
    def calculate(self, p):
        self.probeNum = p
        T = 1 / self.frequency
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            currT = np.floor((probeTime * t - self.phase) / T)
            up = np.logical_and(currT * T + self.phase <= probeTime*t, 
                                probeTime*t < self.coeff * T + currT * T + self.phase)
            
            down = np.logical_and(self.coeff * T + currT * T + self.phase <= probeTime*t,
                                               probeTime*t < T + currT*T + self.phase)

            if up:
                result[t][1] = (self.amplitude / (self.coeff * T)) * (probeTime*t - currT*T - self.phase)
            elif down:
                result[t][1] = ((-self.amplitude / (T*(1 - self.coeff))) * (t*probeTime - currT*T - self.phase)) + (self.amplitude / (1 - self.coeff))
            else:
                result[t][1] = 0
        self.result = result
        return result    
