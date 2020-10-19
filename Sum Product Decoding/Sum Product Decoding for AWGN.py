from math import exp, expm1

y=list()
y = [0.7, -1.2, 0.3, 1.1, -0.1, -0.8]
N0=0.1
R=4
C=6
F=list()

for j in range(C):
    t=(1+exp(-2*y[j]/N0))**(-1)
    F.append([round(1-t, 5), round(t, 5)])

print(F)