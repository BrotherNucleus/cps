import numpy as np
import waves as w

class FileM:
    def __init__(self, p):
        self.path = p
    def serialize(self, name):
        np.save(self.path + '/' + name, self.value)
    def load(self, name):
        return np.load(self.path + '/' + name)
    def interpret(self, arr):
        A = 0
        for v in arr:
            if v[1] > A:
                A = v[1]
        n = len(arr)
        t = arr[n-1][0]
        f = n / t
        wave = w.Wave(A, f, t, 0)
        wave.probeNum = n
        wave.result = arr
        return wave