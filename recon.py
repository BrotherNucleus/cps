import numpy as np
import wave as w
import math
import matplotlib.pyplot as plt

N = 5

def reconstruct(res, type):
    xDiff = res[1][0] - res[0][0]
    xJump = xDiff/N
    l = (len(res[:, [1]])-1)*N + 1
    #print(l)
    v = np.zeros(l, float)
    x = np.zeros(l, float)
    for i in range(len(res[:, [1]]) - 1):
        v[i*N] = res[i][1]
        x[i*N] = res[i][0]
    v[len(v)-1] = res[len(res[:, [1]]) - 1][1]
    x[len(x)-1] = res[len(res[:, [1]]) - 1][0]
    #print(v)
    for i in range(len(x)):
        if i == 0:
            continue
        else:
            x[i] = x[i-1] + xJump
    #print(x)
    if(type == 1):
        zeros = np.zeros(N, float)
        for z in range(len(zeros)):
            zeros[z] = 1
    elif type == 2:
        zeros = np.zeros(N*2, float)
        r = len(zeros) // 2
        for z in range(0, r):
            zeros[z] = (1 / r)*z
            zeros[z + r] = 1 - (1/r)*z           
    elif type == 3:
        Len = round(x[len(x) - 1])*1000
        L = Len / len(res[:, [1]])
        zeros=np.zeros(Len,float)
        for i in range(0,Len):
            t=(Len//2-i)/L
            if (t==0):
                z=1
            else:
                z=math.sin(np.pi*t)/(np.pi*t)
                #print(z)
            zeros[i]=z
        rl = int(round(len(zeros) / l))
        tres = []
        for k in range(l - 1):
            print(k*rl)
            if(k*rl < len(zeros)):
                tres.append(zeros[k*rl])
        zeros = tres
    result = np.convolve(v, zeros, 'same')
    print(result)
    plt.plot(zeros)
    plt.show()
    #print(len(result))
    #print(len(zeros))
    #result = zeros
    # plt.plot(result)
    # plt.show()
    end = np.zeros((len(result), 2))
    # x = np.linspace(0, xDiff, Len)
    for i in range(0, len(result)):
        end[i][0] = x[i]
        end[i][1] = result[i]
    return end

def highPassFilter(wave, cutoff_freq, sampling_freq, filter_order):
    y = wave[:, 1]
    x = wave[:, 0]
    print(sampling_freq)
    M = filter_order
    K = sampling_freq / cutoff_freq
    h = np.zeros(M)

    for n in range(M):
        if n == ((M-1)/2):
            h[n] = 2 / K
        else:
            h[n] = np.sin((2 * np.pi * (n - ((M-1)/2))) / K) / (np.pi * (n - ((M-1)/2)))
    
    h_highpass = h * np.array([(-1) ** n for n in range(filter_order)])

    window = np.ones(M)

    h_highpass *= window

    filtered = np.convolve(y, h)

    xJump = x[len(x) - 1] / len(filtered)
    t = 0
    result = np.zeros((len(filtered), 2), float)
    for i in range(len(filtered)):
        result[i][0] = t
        result[i][1] = filtered[i]
        t += xJump
    return result

def highPassFilterHan(wave, cutoff_freq, sampling_freq, filter_order):
    y = wave[:, 1]
    x = wave[:, 0]
    print(sampling_freq)
    M = filter_order
    K = sampling_freq / cutoff_freq
    h = np.zeros(M)

    for n in range(M):
        if n == ((M-1)/2):
            h[n] = 2 / K
        else:
            h[n] = np.sin((2 * np.pi * (n - ((M-1)/2))) / K) / (np.pi * (n - ((M-1)/2)))
    
    h_highpass = h * np.array([(-1) ** n for n in range(filter_order)])

    window = np.zeros(M)
    for n in range(M):
        window[n] = 0.5 - 0.5 * np.cos((2 * np.pi * n) / M)

    h_highpass *= window

    filtered = np.convolve(y, h)

    xJump = x[len(x) - 1] / len(filtered)
    t = 0
    result = np.zeros((len(filtered), 2), float)
    for i in range(len(filtered)):
        result[i][0] = t
        result[i][1] = filtered[i]
        t += xJump
    return result

def lowPassFilter(wave, cutoff_freq, sampling_freq, filter_order):
    y = wave[:, 1]
    x = wave[:, 0]
    print(sampling_freq)
    M = filter_order
    K = sampling_freq / cutoff_freq
    h = np.zeros(M)

    for n in range(M):
        if n == ((M-1)/2):
            h[n] = 2 / K
        else:
            h[n] = np.sin((2 * np.pi * (n - ((M-1)/2))) / K) / (np.pi * (n - ((M-1)/2)))
        
    window = np.ones(M)

    h *= window

    filtered = np.convolve(y, h)

    xJump = x[len(x) - 1] / len(filtered)
    t = 0
    result = np.zeros((len(filtered), 2), float)
    for i in range(len(filtered)):
        result[i][0] = t
        result[i][1] = filtered[i]
        t += xJump
    return result

def lowPassFilterHan(wave, cutoff_freq, sampling_freq, filter_order):
    y = wave[:, 1]
    x = wave[:, 0]
    print(sampling_freq)
    M = filter_order
    K = sampling_freq / cutoff_freq
    h = np.zeros(M)

    for n in range(M):
        if n == ((M-1)/2):
            h[n] = 2 / K
        else:
            h[n] = np.sin((2 * np.pi * (n - ((M-1)/2))) / K) / (np.pi * (n - ((M-1)/2)))
    
    window = np.zeros(M)
    for n in range(M):
        window[n] = 0.5 - 0.5 * np.cos((2 * np.pi * n) / M)

    h *= window

    filtered = np.convolve(y, h)

    xJump = x[len(x) - 1] / len(filtered)
    t = 0
    result = np.zeros((len(filtered), 2), float)
    for i in range(len(filtered)):
        result[i][0] = t
        result[i][1] = filtered[i]
        t += xJump
    return result

def corelate(wave, other):
    y1 = wave[:,1]
    x1 = wave[:,0]
    y2 = other[:,1]
    x2 = other[:,0]

    y1 = y1 - np.mean(y1)
    y2 = y2 - np.mean(y2)

    y2 = y2[::-1]

    cor = np.convolve(y2, y1, 'same')
    xJump = x1[len(x1) - 1] / len(cor)
    result = np.zeros((len(cor), 2), float)
    t = 0
    for i in range(len(cor)):
        result[i][0] = t
        result[i][1] = cor[i]
        t += xJump
    return result
# vs = np.empty((32, 2))
# j = 1024 / 32
# curr = 0
# for i in range(len(vs)):

#     vs[i][0] = curr
#     vs[i][1] = curr
#     curr += j

# vals = np.array(vs)

# reconstruct(vals, 3)
