import numpy as np

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
        n = self.frequency*self.time
        ret = np.zeros(n)
        for i in range(n):
            if(i == self.imProbe):
                ret[i] = self.amplitude
        return ret