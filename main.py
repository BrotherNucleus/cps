import numpy as np
import waves as w
import graph as g
import impulse as i
import noise as n

cam = g.graph()


print("1. linear noise")
print("2. gaussian noise")
print("3. sin wave")
print("4. sin one-sided wave")
print("5. sin two-sided wave")
print("6. square signal")
print("7. symmetric square signal")
print("8. triangle signal")
print("9. jump")
print("10. single impulse")
print("11. impulse noise")

Type = input("choose a signal type:")
Type = int(Type)

if(Type > 2 and Type < 9):
    A = float(input("Amplitude: "))
    f = float(input("frequency: "))
    t = float(input("time: "))
    d = float(input("phase: "))
elif Type == 1 or Type == 2:
    A = float(input("Amplitude: "))
    t = float(input("time: "))
    d = float(input("phase: "))
elif Type == 9:
    A = float(input("Amplitude: "))
    t = float(input("time: "))
    ts = float(input("jump time: "))  
elif Type == 10:
    A = float(input("Amplitude: "))
    t = float(input("time: "))
    ns = float(input("impulse probe: "))
elif Type == 11:
    A = float(input("Amplitude: "))
    t = float(input("time: "))
    pr = float(input("probability [0.0-1.0]: "))  

if Type != 0 and Type < 12 and Type > 2:
    p = int(input("Number of probes: "))
else:
    p = 300

wave = None

match Type:
    case 1:
        wave = n.linearNoise(A, t)
    case 2:
        wave = n.gaussianNoise(A, t)
    case 3:
        wave = w.SinWave(A, f, t, d)
    case 4:
        wave = w.SinHalfWave(A, f, t, d)
    case 5:
        wave = w.SinModWave(A, f, t, d)
    case 6:
        wave = w.SquareWave(A, f, t, d)
    case 7:
        wave = w.SymSquareWave(A, f, t, d)
    case 8:
        k = float(input("Coefficient: "))
        wave = w.TriangleWave(A, f, t, d, k)
    case 9:
        wave = i.jump(A, p, t, ts)
    case 10:
        wave = i.singleImpulse(A, p, t, ns)
    case 11:
        wave = i.randomImpulse(A, p, t, pr)
    case 0:
        A = 0.2
        t = 30
        wave1 = n.gaussianNoise(A, t)
        #
        wave2 = i.singleImpulse(10, p, t, 100)
print(wave)
if(type(wave) == i.singleImpulse or type(wave) == i.randomImpulse or type(wave) == i.jump):
    values = wave.calculate(p)
else:
    values1 = wave1.calculate(p)
    values2 = wave2.calculate(p)
    wave = wave2 / wave1
    A = wave.amplitude
    t = wave.time
    values = wave.result

print(wave2.result)
cam.displayGraph(wave2.result, 10, t)

print(wave1.result)
cam.displayGraph(wave1.result, 10, t)

print(values)
cam.displayGraph(values, 10, t)
