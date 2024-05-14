import numpy as np
import wave as w
import math
import matplotlib.pyplot as plt

def reconstruct(res, type):
    N = 1
    xDiff = res[1][0] - res[0][0]
    xJump = xDiff/N
    l = (len(res[:, [1]])-1)*N + 1
    print(l)
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
        Len = round(x[len(x) - 1])
        L = Len / len(res[:, [1]])
        zeros=np.zeros(Len,float)
        v = np.zeros(Len, float)
        x = np.zeros(Len, float)
        for i in range(len(res[:, [1]]) - 1):
            v[i*L] = res[i][1]
            x[i*L] = res[i][0]
        v[len(v)-1] = res[len(res[:, [1]]) - 1][1]
        x[len(x)-1] = res[len(res[:, [1]]) - 1][0]
        #print(v)
        for i in range(len(x)):
            if i == 0:
                continue
            else:
                x[i] = x[i-1] + L
        for i in range(0,Len):
            t=(Len//2-i)/L
            if (t==0):
                z=1
            else:
                z=math.sin(np.pi*t)/(np.pi*t)
                print(z)
            zeros[i]=z
    result = np.convolve(v, zeros, 'same')
    print(len(zeros))
    #result = zeros
    plt.plot(zeros)
    plt.show()
    end = np.zeros((len(result), 2))
    # x = np.linspace(0, xDiff, Len)
    for i in range(0, len(result)):
        end[i][0] = x[i]
        end[i][1] = result[i]
    return end


# vs = np.empty((32, 2))
# j = 1024 / 32
# curr = 0
# for i in range(len(vs)):

#     vs[i][0] = curr
#     vs[i][1] = curr
#     curr += j

# vals = np.array(vs)

# reconstruct(vals, 3)
