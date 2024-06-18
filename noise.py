import numpy as np
import random
import waves as w
import impulse as im

class noise:
    '''
    Default noise function \n
    A - amplitude of the impulse\n
    d - time\n
    \n
    This function is only used for inheritance do not use it for anything else\n
    Note that no derivative of this function will have an additional argument(s)\n
    '''
    def __init__(self, A, d, id):
        self.amplitude = A
        self.time = d
        self.result = None
        self.id = id
        self.noquant = None
        self.filed = False
        self.calculated = False
    def __str__(self):
        return f'amplitude = {self.amplitude}; phase = {self.phase}; time = {self.time}'
    def __add__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == gaussianNoise or type(other) == linearNoise):
                wave = noise(self.amplitude + other.amplitude, self.time, 0)
            elif(type(other) == im.jump or type(other) == im.randomImpulse or type(other) == im.singleImpulse):
                wave = noise(self.amplitude + other.amplitude, self.time, 0)
            else:
                wave = w.Wave(self.amplitude + other.amplitude, other.frequency, self.time, other.phase, 0)
                wave.probeNum = other.probeNum
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] + other.result[i][1]
                res[i][2] = self.result[i][2] + other.result[i][2]
            wave.result = res
            return wave
        else:
            print(f"Error: cannot add two diffrently shaped arrays: ({self.result.shape}) + ({other.result.shape})")
    def __sub__(self, other):
        if(other.result.shape == self.result.shape):
            if self.amplitude > other.amplitude:
                A = self.amplitude
            else:
                A = other.amplitude
            if(type(other) == gaussianNoise or type(other) == linearNoise):
                wave = noise(A, self.time, 0)
            elif(type(other) == im.jump or type(other) == im.randomImpulse or type(other) == im.singleImpulse):
                wave = noise(A, self.time, 0)
            else:
                wave = w.Wave(A, other.frequency, self.time, other.phase, 0)
                wave.probeNum = other.probeNum
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] - other.result[i][1]
                res[i][2] = self.result[i][2] - other.result[i][2]
            wave.result = res
            return wave
        else:
            print(f"Error: cannot sub two diffrently shaped arrays: ({self.result.shape}) - ({other.result.shape})")
    def __mul__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == gaussianNoise or type(other) == linearNoise):
                wave = noise(self.amplitude * other.amplitude, self.time, 0)
            elif(type(other) == im.jump or type(other) == im.randomImpulse or type(other) == im.singleImpulse):
                wave = noise(self.amplitude * other.amplitude, self.time, 0)
            else:
                wave = w.Wave(self.amplitude * other.amplitude, other.frequency, self.time, other.phase, 0)
                wave.probeNum = other.probeNum
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] * other.result[i][1] - self.result[i][2] * other.result[i][2]
                res[i][2] = self.result[i][1] * other.result[i][2] + self.result[i][2] * other.result[i][1]
            wave.result = res
            return wave
    def __truediv__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == gaussianNoise or type(other) == linearNoise):
                wave = noise(self.amplitude / other.amplitude, self.time, 0)
            elif(type(other) == im.jump or type(other) == im.randomImpulse or type(other) == im.singleImpulse):
                wave = noise(self.amplitude / other.amplitude, self.time, 0)
            else:
                wave = w.Wave(self.amplitude / other.amplitude, other.frequency, self.time, other.phase, 0)
                wave.probeNum = other.probeNum
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                if abs(other.result[i][1]) > 0.2:
                    res[i][1] = (self.result[i][1] * other.result[i][1] + self.result[i][2] * other.result[i][2]) / (other.result[i][1]**2 + other.result[i][2]**2)
                else:
                    res[i][1] = 0
                if abs(other.result[i][2]) > 0.2:
                    res[i][2] = (self.result[i][2] * other.result[i][1] - self.result[i][1] * other.result[i][2]) / (other.result[i][1]**2 + other.result[i][2]**2)
                else:
                    res[i][2] = 0
            wave.result = res
            return wave

class linearNoise(noise):
    '''
    linear noise - extends noise \n
    A - amplitude of the impulse\n
    d - time\n
    \n
    This class simulates linear noise with a specified amplitude over a specified time\n
    '''
    def __init__(self, A, d, id):
        super().__init__(A, d, id)
    def __str__(self):
        return super().__str__()
    def random(self):
        return random.uniform(-self.amplitude, self.amplitude)
    def calculate(self, p):
        '''
        this function calculates the values for the noise in format\n
        [[time, value],\n
         [time1, value1],\n
         [time2, value2],\n
         ...\n
         [timeN-1, valueN-1]]\n
        this function takes an argument p which corresponds to number of probes\n
        '''
        self.probeNum = p
        probeTime = self.time / (p-1)
        result = np.empty((p, 3))
        for t in range(p):
            result[t][0] = t*probeTime
            result[t][1] = self.random()
            result[t][2] = 0
        self.result = result
        return result
    
class gaussianNoise(noise):
    '''
    gaussian noise - extends noise \n
    A - amplitude of the impulse\n
    d - time\n
    \n
    This class simulates gaussian noise (normal distribusion) with a specified amplitude over a specified time\n
    '''
    def __init__(self, A, d, id):
        super().__init__(A, d, id)
    def calculate(self, p):
        '''
        this function calculates the values for the noise in format\n
        [[time, value],\n
         [time1, value1],\n
         [time2, value2],\n
         ...\n
         [timeN-1, valueN-1]]\n
        this function takes an argument p which corresponds to number of probes\n
        '''
        self.probeNum = p
        probeTime = self.time / (p-1)
        result = np.empty((p, 3))
        for t in range(p):
            result[t][0] = t*probeTime
            result[t][1] = self.amplitude*np.random.normal()
            result[t][2] = 0
        self.result = result
        return result