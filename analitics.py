import numpy as np
import math

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

def splot(x, h, N, M):
    '''
    x - dyskretny sygnał 1\n
    h - dyskretny sygnał 2\n
    N - liczba elementów sygnału x\n
    M - liczba elementów sygnału h
    '''
    y = np.zeros(N+M-1, float)
    for n in range(0, N+M-1):
        t = 0
        for k in range(0, N):
            if(n-k >= 0 and n-k<=M-1):
                t=t+x[k]*h[n-k]
        y[n]=t
    return y


def DFT(xr,xi):
    '''
    xr - real, xi - imaginary
    '''
    N=len(xr)
    Xr=np.zeros(N,float)
    Xi=np.zeros(N,float)
    for k in range(0,N):
        for n in range(0,N):
            a=2*math.pi/N*k*n
            c=math.cos(a)
            s=math.sin(a)
            Xr[k]=Xr[k]+(c*xr[n]+s*xi[n])
            Xi[k]=Xi[k]+(c*xi[n]-s*xr[n])
    return (Xr,Xi)

def IDFT(Xr,Xi):
    N=len(Xr)
    xr=np.zeros(N,float)
    xi=np.zeros(N,float)
    for n in range(0,N):
        for k in range(0,N):
            a=-2*math.pi/N*k*n
            c=math.cos(a)
            s=math.sin(a)
            xr[n]=xr[n]+(c*Xr[k]+s*Xi[k])
            xi[n]=xi[n]+(c*Xi[k]-s*Xr[k])
    return (xr/N,xi/N)

def FFT(wave):
    # signal = np.zeros(len(wave[:,1]), complex)
    # for i in range(len(wave[:,1])):
    #     signal[i] = complex(wave[i][1], wave[i][2])
    # print(signal)
    N = len(wave)
    if N <= 1:
        return wave
    even = FFT(wave[0::2])
    odd = FFT(wave[1::2])
    T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]

def calculate_FFT(wave, t):
    check = FFT(wave)
    # check = [x / len(check) for x in check]
    # check = [check[0]] + [2 * x for x in check[1:len(check)//2]] + check[len(check)//2:]
    
    N = len(check)
    Fs = N / t
    
    xs = np.zeros(N, float)
    for bb in range(len(xs)):
        xs[bb] = (bb)*Fs/N
    res = np.zeros((int(len(xs)), 3))

    ys = [y[1] for y in check]
    
    for ff in range(int(len(xs))):
        res[ff][0] = xs[ff]
        res[ff][1] = ys[ff].real
        res[ff][2] = ys[ff].imag

    
    return res

def ifft(spectrum):
    N = len(spectrum)
    if N <= 1:
        return spectrum
    even = ifft(spectrum[0::2])
    odd = ifft(spectrum[1::2])
    T = [np.exp(2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
    return [(even[k] + T[k]) / 2 for k in range(N // 2)] + [(even[k] - T[k]) / 2 for k in range(N // 2)]

def calculate_ifft(wave, t):
    cm = np.zeros(len(wave[:, 1]), complex)
    for ii in range (len(cm)):
        cm[ii] = complex(wave[ii][1], wave[ii][2])
    ch = ifft(cm)
    ys = ch
    x = np.linspace(0, t, len(ys))
    result = np.zeros((len(ys), 3))
    for kk in range(len(ys)):
        result[kk][0] = x[kk]
        result[kk][1] = ys[kk].real
        result[kk][2] = ys[kk].imag
    
    return result

def dct(signal):
    N = len(signal)
    result = []
    factor = np.pi / N
    for k in range(N):
        sum_val = 0
        for n in range(N):
            sum_val += signal[n] * np.cos(factor * (n + 0.5) * k)
        if k == 0:
            sum_val *= np.sqrt(1 / N)
        else:
            sum_val *= np.sqrt(2 / N)
        result.append(sum_val)
    return result

def calculate_dct(wave, t):
    check = dct(wave[:, 1])
    N = len(check)
    xs = np.zeros(N, float)
    Fs = N / t
    res = np.zeros((int(len(xs)), 3))
    for bb in range(len(xs)):
        xs[bb] = (bb)*Fs/(2*N)
    for ff in range(int(len(xs))):
        res[ff][0] = xs[ff]
        res[ff][1] = check[ff]
        res[ff][2] = 0
    return res

def idct(spectrum):
    N = len(spectrum)
    result = []
    factor = np.pi / N
    normalization_factor = np.sqrt(2 / N)  # Normalization factor for IDCT Type-II
    
    for n in range(N):
        sum_val = 0.5 * spectrum[0] * np.sqrt(1 / N)  # Adjust the first term
        for k in range(1, N):
            sum_val += spectrum[k] * np.cos(factor * k * (n + 0.5)) * normalization_factor
        result.append(sum_val)
    
    return result

def calculate_idct(wave, t):
    rr = idct(wave[:, 1])
    xs = np.linspace(0, t, len(rr))
    res = np.zeros((len(rr), 3))
    for oo in range(len(rr)):
        res[oo][0] = xs[oo]
        res[oo][1] = rr[oo]
        res[oo][2] = 0
    return res