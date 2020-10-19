#The Encoder for RA Code

#1-Take K source bits input U=(u_1,u_2, .. ,u_k)
uAsInput=[int(x) for x in input().split()]

#2-Repeat each bit three times
repeatBits=3 #times of repeat each bit
uRepeated=list()
for i in range(len(uAsInput)):
    for j in range(repeatBits):
        uRepeated.append(uAsInput[i])
#print(uRepeated)

#3-Permute these N=3k bits
import random
random.Random(4).shuffle(uRepeated)
#print(uRepeated)

#4-Transmit the accumulated sum output:V=(v_1, v_2, .. ,v_N)
vAsOutput=list()
for i in range(len(uRepeated)):
    if(i !=0):
        vAsOutput.append((uRepeated[i]+vAsOutput[i-1])%2)
    else:
        vAsOutput.append(uRepeated[i])

print("V:=", vAsOutput)

#5-Transmit with the Fibonanchi output:F=(f_1, f_2, .. ,f_N) 
fAsOutput=list()
for i in range(len(uRepeated)):
    if(i ==0):
        fAsOutput.append(uRepeated[i])
    if(i==1):
        fAsOutput.append(uRepeated[i])
    else:
        fAsOutput.append((uRepeated[i-1]+uRepeated[i-2])%2)

print("F:=", fAsOutput)
        
    
