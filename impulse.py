import numpy as np
import random

class impulse:
    def __init__(self, A, f, d):
        self.amplitude = A
        self.frequency = f
        self.time = d
    def __str__(self):
        return f'Amplitude = {self.amplitude}; freqency = {self.frequency}; time = {self.time}; '

class singleImpulse(impulse):
    def __init__(self, A, f, d, n1, ns):
        self.firstProbe = n1
        if(ns < n1):
            print(f'ERROR: impulse probe value must be higher or equal to first probe value <first probe: {self.firstProbe}; impulse probe {ns}>')
            print(f'new impulse probe value set to first probe value ({self.firstProbe})')
            self.imProbe = self.firstProbe
        else:
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
        return ret