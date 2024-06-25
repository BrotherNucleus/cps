import numpy as np
import waves as w
import graph as g
import impulse as i
import noise as n
import fileManager as f
import analitics as a
import gui as gui

# cam = g.graph()


# print("1. linear noise")
# print("2. gaussian noise")
# print("3. sin wave")
# print("4. sin one-sided wave")
# print("5. sin two-sided wave")
# print("6. square signal")
# print("7. symmetric square signal")
# print("8. triangle signal")
# print("9. jump")
# print("10. single impulse")
# print("11. impulse noise")

# Type = input("choose a signal type:")
# Type = int(Type)

# if(Type > 2 and Type < 9):
#     A = float(input("Amplitude: "))
#     f = float(input("frequency: "))
#     t = float(input("time: "))
#     d = float(input("phase: "))
# elif Type == 1 or Type == 2:
#     A = float(input("Amplitude: "))
#     t = float(input("time: "))
#     d = float(input("phase: "))
# elif Type == 9:
#     A = float(input("Amplitude: "))
#     t = float(input("time: "))
#     ts = float(input("jump time: "))  
# elif Type == 10:
#     A = float(input("Amplitude: "))
#     t = float(input("time: "))
#     ns = float(input("impulse probe: "))
# elif Type == 11:
#     A = float(input("Amplitude: "))
#     t = float(input("time: "))
#     pr = float(input("probability [0.0-1.0]: "))  

# if Type != 0 and Type < 12 and Type > 2:
#     p = int(input("Number of probes: "))
# else:
#     p = 300

# wave = None

# match Type:
#     case 1:
#         wave = n.linearNoise(A, t, 0)
#     case 2:
#         wave = n.gaussianNoise(A, t, 0)
#     case 3:
#         wave = w.SinWave(A, f, t, d, 0)
#     case 4:
#         wave = w.SinHalfWave(A, f, t, d, 0)
#     case 5:
#         wave = w.SinModWave(A, f, t, d, 0)
#     case 6:
#         wave = w.SquareWave(A, f, t, d, 0)
#     case 7:
#         wave = w.SymSquareWave(A, f, t, d, 0)
#     case 8:
#         k = float(input("Coefficient: "))
#         wave = w.TriangleWave(A, f, t, d, k, 0)
#     case 9:
#         wave = i.jump(A, p, t, ts, 0)
#     case 10:
#         wave = i.singleImpulse(A, p, t, ns, 0)
#     case 11:
#         wave = i.randomImpulse(A, p, t, pr, 0)
#     case 0:
#         A = 0.2
#         t = 30
#         wave1 = w.SinWave(2, 0.5, t, 0.2, 0)
#         #
#         wave2 = n.gaussianNoise(A, t, 0)
# print(wave)

# values1 = wave1.calculate(p)
# values2 = wave2.calculate(p)
# wave3 = wave1 + wave2
# vl = wave3.result
# A = wave1.amplitude
# cam.displayGraph(values1, A, t)
# cam.displayHist(values1, 20)
# an = a.analizer(wave1)
# print(an.mean())
# print(an.meanAbs())
# print(an.rms())
# print(an.variance())
# print(an.power())
t = 10
wave1 = w.SinWave(2, 1, t, 0.2, 0)
N = 512
res = wave1.calculate(N)
wave2 = w.SinWave(1, 3, t, 0, 1)
res = wave2.calculate(N)
wave3 = w.SinWave(0.5, 5, t, 0, 1)
res = wave3.calculate(N)
wave4 = wave1 + wave2
wave4 += wave3
res = wave4.result
res2 = np.delete(res, -1, axis=1)
print(res2)
gg = g.graph()
gg.displayGraph(res2, max(res2[:, 1]), 10)

# resy = res[:, 1]
# resz = res[:, 2]
# resc = np.zeros(len(res[:, 0]), complex)
# for h in range(len(res[:, 0])):
#     resc[h] = complex(resy[h], resz[h])

# check2 = np.fft.fft(resc)
# print(check2)

# xs = np.zeros(N, float)
# for bb in range(len(xs)):
#      xs[bb] = (bb)*Fs/N

check = a.calculate_FFT(res, t)
res2 = np.delete(check, -1, axis=1)
res3 = np.delete(check, 1, axis=1)
# gg.displayGraph(res2, max(res2[:, 1]), res2[len(res2)- 1][0])
# gg.displayGraph(res3, max(res3[:, 1]), res2[len(res2)- 1][0])
print(res2)


result = a.calculate_ifft(check, t)
# gg.displayGraph(result, max(result[:, 1]), result[len(result)-1][0])

result = a.calculate_dct(res, t)
gg.displayGraph(result, max(result[:, 1]), result[len(result[:, 0])-1][0])

k = a.calculate_idct(result, t)
gg.displayGraph(k, max(k[:,1]), t)

#gui.startGui()