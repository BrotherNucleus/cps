import numpy as np
import random

class impulse:
    def __init__(self, A, f, d):
        self.amplitude = A
        self.frequency = f
        self.time = d
        self.result = None
    def __str__(self):
        return f'Amplitude = {self.amplitude}; freqency = {self.frequency}; time = {self.time}; '

class singleImpulse(impulse):
    def __init__(self, A, f, d, ns):
        self.imProbe = ns
        super().__init__(A, f, d)
    def __str__(self):
        return super().__str__() + f'firstProbe = {self.firstProbe}; impulse Probe = {self.imProbe}; '
    def calculate(self):
        n = int(self.frequency*self.time)
        T = 1 / self.frequency
        ret = np.zeros([n, 2])
        for i in range(n):
            ret[i][0] = i*T
            if(i == self.imProbe):
                ret[i][1] = self.amplitude
        self.result = ret
        return ret
    
class randomImpulse(impulse):
    def __init__(self, A, f, d, p):
        self.chance = p
        super().__init__(A, f, d)
    def __str__(self):
        return super().__str__() + f'probability of an impulse: {self.chance}'
    def random(self):
        rand = random.uniform(0.0, 1.0)
        if rand > self.chance:
            return False
        else:
            return True
    def calculate(self):
        n = int(self.frequency*self.time)
        T = 1 / self.frequency
        ret = np.zeros([n, 2])
        for i in range(n):
            ret[i][0] = i*T
            if(self.random()):
                ret[i][1] = self.amplitude
        self.result = ret
        return ret
    
class jump(impulse):
    def __init__(self, A, d, ts):
        self.jumpTime = ts
        super().__init__(A, None, d)
    def __str__(self):
        return super().__str__() + f'jump time: {self.jumpTime}'
    def calculate(self, p):
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