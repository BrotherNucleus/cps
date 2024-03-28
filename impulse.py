import numpy as np
import random
import waves as w
import noise as n

class impulse:
    '''
    Default impulse function \n
    A - amplitude of the impulse\n
    p - number of probes\n
    d - time\n
    \n
    This function is only used for inheritance do not use it for anything else\n
    Note that every derivative of this function will have an additional argument
    depending on the usage \n
    '''
    def __init__(self, A, p, d, id):
        self.amplitude = A
        self.frequency = p / d
        self.probeNum = p
        self.time = d
        self.result = None
    def __str__(self):
        return f'Amplitude = {self.amplitude}; freqency = {self.frequency}; time = {self.time}; '
    def __add__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == n.gaussianNoise or type(other) == n.linearNoise):
                wave = n.noise(self.amplitude + other.amplitude, self.time, 0)
            elif(type(other) == jump or type(other) == randomImpulse or type(other) == singleImpulse):
                wave = impulse(self.amplitude + other.amplitude, self.probeNum, self.time, 0)
            else:
                wave = w.Wave(self.amplitude + other.amplitude, other.frequency, self.time, other.phase, 0)
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] + other.result[i][1]
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
            if(type(other) == n.gaussianNoise or type(other) == n.linearNoise, 0):
                wave = n.noise(A, self.time)
            elif(type(other) == jump or type(other) == randomImpulse or type(other) == singleImpulse):
                wave = impulse(A, self.probeNum, self.time, 0)
            else:
                wave = w.Wave(A, other.frequency, self.time, other.phase, 0)
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] - other.result[i][1]
            wave.result = res
            return wave
        else:
            print(f"Error: cannot sub two diffrently shaped arrays: ({self.result.shape}) - ({other.result.shape})")
    def __mul__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == n.gaussianNoise or type(other) == n.linearNoise):
                wave = n.noise(self.amplitude * other.amplitude, self.time, 0)
            elif(type(other) == jump or type(other) == randomImpulse or type(other) == singleImpulse):
                wave = impulse(self.amplitude * other.amplitude, self.probeNum, self.time, 0)
            else:
                wave = w.Wave(self.amplitude * other.amplitude, other.frequency, self.time, other.phase, 0)
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                res[i][1] = self.result[i][1] * other.result[i][1]
            wave.result = res
            return wave
    def __truediv__(self, other):
        if(other.result.shape == self.result.shape):
            if(type(other) == n.gaussianNoise or type(other) == n.linearNoise):
                wave = n.noise(self.amplitude / other.amplitude, self.time, 0)
            elif(type(other) == jump or type(other) == randomImpulse or type(other) == singleImpulse):
                wave = impulse(self.amplitude / other.amplitude, self.probeNum, self.time, 0)
            else:
                wave = w.Wave(self.amplitude / other.amplitude, other.frequency, self.time, other.phase, 0)
            res = np.zeros((self.result.shape))
            for i in range(len(res)):
                res[i][0] = self.result[i][0]
                if abs(other.result[i][1]) > 0.02:
                    res[i][1] = self.result[i][1] / other.result[i][1]
                else:
                    res[i][1] = 0
            wave.result = res
            return wave

class singleImpulse(impulse):
    '''
    single Impulse - extends impulse\n
    A - amplitude\n
    pr - number of probes\n
    d - time\n
    ns - probe on which the impulse happens\n
    class that simulates a singular impulse on a signal which otherwise has constant value of 0\n
    '''
    def __init__(self, A, pr, d, ns, id):
        self.imProbe = ns
        super().__init__(A, pr, d, id)
    def __str__(self):
        return super().__str__() + f'impulse Probe = {self.imProbe}; '
    def calculate(self, redundant):
        '''
        this function calculates the values for the impulse in format\n
        [[time, value],\n
         [time1, value1],\n
         [time2, value2],\n
         ...\n
         [timeN-1, valueN-1]]\n
        this function takes an argument "redundant"\n
        it is used so that whenever you're calling this function while using wave or noise class 
        there is no issue with the usual format of "calculate(p)"\n
        this is NOT a good coding practice, in fact I should be crucified for it\n
        by no means do that ever in your programs\n
        '''
        n = self.probeNum
        T = 1 / self.frequency
        ret = np.zeros([n, 2])
        for i in range(n):
            ret[i][0] = i*T
            if(i == self.imProbe):
                ret[i][1] = self.amplitude
        self.result = ret
        return ret
    
class randomImpulse(impulse):
    '''
    random Impulse - extends impulse\n
    A - amplitude\n
    pr - number of probes\n
    d - time\n
    p - probability [0-1] of a probe being an impulse probe\n
    class that simulates random occuring impulse on a signal which otherwise has constant value of 0\n
    '''
    def __init__(self, A, pr, d, p, id):
        self.chance = p
        super().__init__(A, pr, d, id)
    def __str__(self):
        return super().__str__() + f'probability of an impulse: {self.chance}'
    def random(self):
        rand = random.uniform(0.0, 1.0)
        if rand > self.chance:
            return False
        else:
            return True
    def calculate(self, redundant):
        '''
        this function calculates the values for the impulse in format\n
        [[time, value],\n
         [time1, value1],\n
         [time2, value2],\n
         ...\n
         [timeN-1, valueN-1]]\n
        this function takes an argument "redundant"\n
        it is used so that whenever you're calling this function while using wave or noise class 
        there is no issue with the usual format of "calculate(p)"\n
        this is NOT a good coding practice, in fact I should be crucified for it\n
        by no means do that ever in your programs\n
        '''
        n = self.probeNum
        T = 1 / self.frequency
        ret = np.zeros([n, 2])
        for i in range(n):
            ret[i][0] = i*T
            if(self.random()):
                ret[i][1] = self.amplitude
        self.result = ret
        return ret
    
class jump(impulse):
    '''
    jump - extends impulse\n
    A - amplitude\n
    p - number of probes\n
    d - time\n
    ts - probability [0-1] of a probe being an impulse probe\n
    class that simulates a jump from value of 0 to constant value of amplitude after a specified time\n
    '''
    def __init__(self, A, p, d, ts, id):
        self.jumpTime = ts
        super().__init__(A, p, d, id)
    def __str__(self):
        return super().__str__() + f'jump time: {self.jumpTime}'
    def calculate(self, redundant):
        '''
        this function calculates the values for the impulse in format\n
        [[time, value],\n
         [time1, value1],\n
         [time2, value2],\n
         ...\n
         [timeN-1, valueN-1]]\n
        this function takes an argument "redundant"\n
        it is used so that whenever you're calling this function while using wave or noise class 
        there is no issue with the usual format of "calculate(p)"\n
        this is NOT a good coding practice, in fact I should be crucified for it\n
        by no means do that ever in your programs\n
        '''
        p = self.probeNum
        probeTime = self.time / (p-1)
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = t*probeTime
            if(t*probeTime < self.jumpTime):
                result[t][1] = 0
            elif (t*probeTime == self.jumpTime):
                result[t][1] = self.amplitude / 2
            else:
                result[t][1] = self.amplitude
        self.result = result
        return result