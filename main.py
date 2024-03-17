import numpy as np
import waves as w

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

if(Type > 2 and Type < 9):
    A = input("Amplitude: ")
    f = input("frequency: ")
    t = input("time: ")
    d = input("phase: ")

match Type:
    case 1:
        print("bomba")
    case 2:
        print("bomba")
    case 3:
        w.SinWave(A, f, t, d)
    case 4:
        print("bomba")
    case 5:
        print("bomba")
    case 6:
        print("bomba")
    case 7:
        print("bomba")
    case 8:
        print("bomba")
    case 9:
        print("bomba")
    case 10:
        print("bomba")
    case 11:
        print("bomba")
print(Type)