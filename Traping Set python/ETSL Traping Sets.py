R = 3
C = 3
aMAXX = 3
bMAXX = 3

import numpy as np
input = np.loadtxt('example.txt', dtype=int, delimiter=None)
adjmatrix = [[0] * C for i in range(R)] # n list each contains m element matrix n*m

counter=0
for i in range(R):
    for j in range(len(input[i])):
        x=input[i][j]
        if(x-1 < 0):
            pass
        else:
            adjmatrix[i][x-1]=1
            counter+=1

counter
import networkx as nx # define the graph
from networkx.algorithms import bipartite
G=nx.Graph()

import numpy, scipy.sparse # define the adj. matrix as scipy matrix for input graph
A = numpy.array(adjmatrix)
Asp = scipy.sparse.csr_matrix(A)

from networkx.algorithms.bipartite import from_biadjacency_matrix
G = from_biadjacency_matrix(Asp, create_using=None, edge_attribute=None)#scipy sparse matrix
X, Y = bipartite.sets(G)
XX = list(X)
YY = list(Y)

import matplotlib.pyplot as plt
import numpy as np

nx.draw(G)
plt.savefig("simple_path.png") # save as png
plt.show() # display

# Define I_tem dictionary
tem = {}
for i in range(1, aMAXX+1): 
    for j in range(1, bMAXX+1):
        tem[(i, j)] = [] # define type of values in tem

# making I_tem(1,b) for only one variable   G.degree(i)
for i in range(0, R):
    for j in range(1, bMAXX+1):
        if(G.degree(i) == j):
            tem[(1, j)].append([i])

def seprateDegree(gGraph): # seprate even ond odd degree of each list of variables
    checklistEEVN = []
    checklistOODD = []
    B = list(n for n,d in gGraph.nodes(data=True) if d['bipartite'] == 1)
    for i in range(len(B)):
        if(gGraph.degree(B[i]) == 0):
            pass
        elif((gGraph.degree(B[i]))%2 == 0):
            checklistEEVN.append(B[i])
        else:
            checklistOODD.append(B[i])
    return checklistEEVN, checklistOODD

for a in range(1, aMAXX):
    for b in range(1, bMAXX+1):
        listofcharTem = tem[(a,b)][:]
        f = open("tem.txt","w")
        f.write( str(tem) )
        f.close()
        for i in range(len(listofcharTem)):
            oldStructure = listofcharTem[i][:]
            remainingVariables = XX[:]
            remainingVariables = [x for x in remainingVariables if x not in listofcharTem[i]] # count remain variables
            for j in range(len(remainingVariables)):
                variable = remainingVariables[j]
                G3 = nx.Graph()
                G3 = G.subgraph(list(Y.union(oldStructure)))
                eevnDegOldStructure = []
                ooddDegOldStructure = []
                eevnDegOldStructure, ooddDegOldStructure = seprateDegree(G3)
                degVariable = len(G.neighbors(variable))
                bNew = b + degVariable - 2
                if((bNew != 0) & (degVariable <= bMAXX + 2 - b) & (len(list(set(eevnDegOldStructure) & set(G.neighbors(variable)))) == 0) & (len(list(set(ooddDegOldStructure) & set(G.neighbors(variable)))) == 1)): # the 3 condition for new variable
                    newStructure = listofcharTem[i][:]
                    newStructure.append(variable) # new structure
                    newStructure.sort()
                    flagg = 1
                    lisssttt = tem[(a+1, bNew)][:]
                    for kk in range(len(lisssttt)):
                        if((newStructure == lisssttt[kk])):
                            flagg=0
                            break   
                    if(flagg == 1):
                        tem[(a+1, bNew)].append(newStructure) # add new structure to I_tem
                        print("new tem", newStructure)


print("\n\nThe last I_temp:\n",tem)

for a in range(1, aMAXX+1):
    for b in range(1, bMAXX+1):
        if(len(tem[(a,b)]) != 0):
            print("I_tem(",a,",",b,")=",len(tem[(a,b)]))

f = open("tem.txt","w")
f.write( str(tem) )
f.close()