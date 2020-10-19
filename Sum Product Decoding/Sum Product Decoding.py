#H=[[1,1,1,0,0,1,1,0,0,1],[1,0,1,0,1,1,0,1,1,0],[0,0,1,1,1,0,1,0,1,1],[0,1,0,1,1,1,0,1,0,1],[1,1,0,1,0,0,1,1,1,0]]
#sendword =    [0,0,0,1,0,1,0,1,0,1]
#recieveword = [0,0,0,1,1,1,0,1,0,1]
#F = [[0.78,0.22],[0.84,0.16],[0.81,0.19],[0.52,0.48],[0.45,0.55],[0.13,0.87],[0.82,0.18],[0.21,0.79],[0.75,0.25],[0.24,0.76]]

import numpy as np
from numpy import prod
from numpy import transpose, matmul
from sympy import Symbol, solve
from sympy.solvers import solve
k = Symbol('k')

input = np.loadtxt('ldpcSendRecieve.txt', dtype=int, delimiter=None)
R, C = 3, 7
H = [[0] * C for i in range(R)]
for i in range(R):
    for j in range(C):
        H[i][j] = input[i][j]

Hnp = np.array(H)

# sendword = list()
# for j in range(C):
#     sendword.append(input[R][j])

# recieveword = list()
# for j in range(C):
#     recieveword.append(input[R+1][j])

input = np.loadtxt('probability.txt', dtype=float, delimiter=None)
F = [[0] * 2 for i in range(C)]
for i in range(C):
    for j in range(2):
        F[i][j] = input[i][j]

#define Q
Q = {}
for i in range(0, R): 
    for j in range(0, C):
        Q[(i, j)] = [] # define type of values in tem

#put prob. of r in Q
for i in range(0, R):
    for j in range(0, C):
        if(H[i][j]==1):
            Q[(i, j)].append(F[j][0])
            Q[(i, j)].append(F[j][1])
        else:
            Q[(i, j)].append(0)
            Q[(i, j)].append(0)

# print("first Q:\n")
# for i in range(0, R):
#     for j in range(0, C):
#         print(i,j,":", Q[(i,j)])
#     print("\n")

#define r matrix as a  dictionary  
r = {}
for i in range(0, R): 
    for j in range(0, C):
        r[(i, j)] = [] # define type of values in tem

#calcute and put value of matrix r
for j in range(0, R): # in row j
        for i in range(0, C): # for variablles 0..i..C
            if (H[j][i] != 0):
                produce=1
                for ii in range(0, C): #except variable i-th
                    if(ii != i):
                        produce = produce*(1-2*Q[(j,ii)][1])        
                xx=0.5+(0.5*produce)
                r[(j, i)].append(round(xx, 6))
                r[(j, i)].append(round(1-xx,6))
            else:
                r[(j, i)].append(0)
                r[(j, i)].append(0)

#number of iterative for decoding
for p in range(50):
    if (p != 0):
        #calcute and put value of matrix r
        for j in range(0, R): # in row j
            for i in range(0, C): # for variablles 0..i..C
                if (H[j][i] != 0):
                    produce=1
                    for ii in range(0, C): #except variable i-th
                        if(ii != i):
                            produce = produce*(1-2*Q[(j,ii)][1])        
                    xx=0.5+(0.5*produce)
                    r[(j, i)][0] = round(xx, 6)
                    r[(j, i)][1] = round(1-xx,6)
                else:
                    r[(j, i)][0] = 0
                    r[(j, i)][1] = 0
    # print("first R:\n")
    # for i in range(0, R):
    #     for j in range(0, C):
    #         print(i,j,":", r[(i,j)])
    #     print("\n")
    codeword = list()
    QQ= list()
    for j in range(0, C):
        produce0=1
        produce1=1
        for i in range(0, R):
            if(r[(i,j)][0] != 0):
                produce0 = produce0*(r[(i,j)][0])
            if(r[(i,j)][1] != 0):
                produce1 = produce1*(r[(i,j)][1])
        x=F[j][0]*produce0
        y=F[j][1]*produce1
        t = solve(k*x + k*y - 1, k)
        Q0 = round(t[0]*x, 6)
        Q1 = round(t[0]*y, 6)
        QQ.append([Q0,Q1])
        if(Q1 > Q0):
            codeword.append(1)
        else:
            codeword.append(0)
    Cnp = np.array(codeword)
    x = np.matmul(Cnp,Hnp.transpose())
    if(set(x%2) == set([0]*R)):
        print("It is correct codeword:")
        print("The obtain codeword is:", codeword)
        #print(QQ)
        print("\nLoop stop in level(p) =",p+1)
        break
    else:
        print("It is wrong codeword:")
        print("The obtain codeword is:", codeword)
        #print(QQ)
    #reWrite the new Q
    for i in range(0, C): # in column ith
        for j in range(0, R): # for checknodes(rows) 0..j..R
            if(H[j][i] != 0):
                produce0 = 1
                produce1 = 1
                for jj in range(0, R): # except check j-th
                    if(jj != j):
                        if(r[(jj,i)][0] != 0):
                            produce0 = produce0*(r[(jj,i)][0])
                        if(r[(jj,i)][1] != 0):
                            produce1 = produce1*(r[(jj,i)][1])
                x = F[i][0]*produce0
                y = F[i][1]*produce1
                t = solve(k*x + k*y - 1, k)
                Q[(j,i)][0] = round(t[0]*x, 6)
                Q[(j,i)][1] = round(t[0]*y, 6)
    # print("new Q:\n")
    # for i in range(0,len(H)):
    #     for j in range(0, len(H[0])):
    #         print(i,j,":", Q[(i,j)])
    #     print("\n")
    #calcute the Q' and make hard desicion
    
        



