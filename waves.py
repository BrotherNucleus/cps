import numpy as np
class Wave:
    def __init__(self, A, f, t, d):
        self.amplitude = A
        self.frequency = f
        self.time = t
        self.phase = d

class SinWave(Wave):
    def __init__(self, A, f, t, d):
        Wave.__init__(self, A, f, t, d)
    def calculate(self, p):
        probeTime = self.time / p
        result = np.empty((p, 2))
        for t in range(p):
            result[t][0] = probeTime * t
            result[t][1] = self.amplitude * np.sin(2*np.pi*self.frequency * (probeTime*t - self.phase))
        self.res = result
        return result
    def __str__(self):
        return f''

sin = SinWave(5, 1.5, 6, 0)

print(sin.frequency)

m = sin.calculate(3)
print(m)