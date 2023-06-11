import math
import cmath
def create_matrix(file):
    fh=open(file,'r')
     #We use cmath module to handle complex numbers that arise when AC sources are handled
    s=(fh.read().splitlines()) #The file is opened in read mode and we read the entire data and split it everytime a newline character is detected. We use this instead of readlines to avoid \n
    a=s.index('.circuit')#We store the indices of '.circuit' and '.end' to choose the part of the file that lies in between them and that is required to generate the MNA matrix.
    b=s.index('.end')
    f={}#We create a dictionary to store the AC sources and their frequencies, dictionary comes in handy when multiple AC sources are to be used
    acflag=0#We create a flag to know whether or not AC sources are used in the given circuit
#When the size of the file, in terms of number of lines is greater than the line count of .end, we realise that ac sources are used and create a dictionary to hold all source and frequency pairs
    if b!=len(s)-1:
        if s[b+1][0:3]=='.ac':
            acflag=1
    r=v=t=c=l=0
    R=[]
    V=[]
    I=[]
    L=[]
    C=[]
    xx=[]
    for i in (s[a+1:b]):
        xx.append(i.split())
    #From the list that contains the netlist that lies between circuit and end, we select the ones with just resistors, capacitors, inductors, voltage sources, current sources and append them to separate lists that store these values separately
    for i in xx:
        if i[0][0]=='R':
            r+=1
            R.append(i)

        if i[0][0]=='V':
            v+=1
            V.append(i)
        if i[0][0]=='I':
            t+=1
            I.append(i)
        if i[0][0]=='L':
            l+=1
            L.append(i)
        if i[0][0]=='C':
            c+=1
            C.append(i)
#Since the AC data consists of nodes 'n' specified in addition to the node number, we write a separate code that neglects these n strings to give just the number of the given node
    if acflag==1:
        for i in range(b+1, len(s)):
            yy=s[i].split()

            f[yy[1]]=yy[2]
            w=yy[2]
        for i in range(t):
            for j in range(1,3):
                if I[i][j][0]=="n":
                    I[i][j]=I[i][j][1]
        for i in range(r):
            for j in range(1,3):
                if R[i][j][0]=="n":
                    R[i][j]=R[i][j][1]
        for i in range(c):
            for j in range(1,3):
              
                if C[i][j][0]=="n":
                    C[i][j]=C[i][j][1]
        for i in range(v):
            for j in range(1,3):
                if V[i][j][0]=="n":
                    V[i][j]=V[i][j][1]
        for i in range(l):
            for j in range(1,3):
                if L[i][j][0]=="n":
                    L[i][j]=L[i][j][1]

#All the matrices may also contain GND instead of 0. In order to facilitate numeric handling, we replace all the grounds with zeroes
    for i in range(r):
        for j in range(1,3):
            if R[i][j]=="GND":
                R[i][j]='0'
    for i in range(v):
        for j in range(1,3):
            if V[i][j]=="GND":
                V[i][j]='0'
    for i in range(t):
        for j in range(1,3):
            if I[i][j]=="GND":
                I[i][j]='0'

    for i in range(c):
        for j in range(1,3):
            if C[i][j]=="GND":
                C[i][j]='0'
    for i in range(l):
        for j in range(1,3):
            if L[i][j]=="GND":
                L[i][j]='0'
    ft=0
    if acflag==1:#For circuits like ckt 2 involving both AC and 
        
        for i in V:
            if i[3]=='dc':
                print(f"{file} : Involves both AC and DC, and hence not applicable under this question")
                ft=1
                break
        for i in I:
            if i[3]=='dc' and ft==0:
                print(f"{file} : Involves both AC and DC, and hence not applicable under this question")
                break
    if ft==1:
        return
#We then create a list x that contains all the nodes, 0 through the last node. This when added with the number of independent voltage sources gives us the size of the vector that we need
    x=[]
    for i in range(r):
        if R[i][1] not in x:
            x.append(R[i][1] )
        if R[i][2] not in x:
            x.append(R[i][2] )
    for i in range(c):
        if C[i][1] not in x:
            x.append(C[i][1] )
        if C[i][2] not in x:
            x.append(C[i][2] )
    for i in range(l):
        if L[i][1] not in x:
            x.append(L[i][1] )
        if L[i][2] not in x:
            x.append(L[i][2] )

    for i in range(v):
        if V[i][1] not in x:
            x.append(V[i][1] )
        if V[i][2] not in x:
            x.append(V[i][2] )
#The list is then sorted to make sure that the numbers are in order, i.e. from 0 to nth node.
    x.sort()
    B=[0]*(len(x)-1)
#Now, we initiate a list B with all zeros, having a length of len(x)-1. This minus 1, indicates that the 0 element in x is ignored. 
    
   
    A=[]
#The elements corresponding to nodes in B are supposed to be 0(Except when there are current sources). The elements corresponding to the currents through the independent voltage sources are supposed to be entered according to the value in the voltage lists.
    for i in V[::-1]:
        B.append(int(i[4]))
    for i in I:
        if int(i[1])!=0:
            B[int(i[1])-1]-=int(i[4])
        if int(i[2])!=0:
            B[int(i[2])-1]+=int(i[4])
#Once list B is completed, with zeros and voltage sources, we now turn to the A matrix

#We iterate through the X list and for all nodes, we carry out the following operations
    for j in range(1,len(x)):
        #First create a list that can be added to the matrix A. In each iteration of the loop, we add a list that has all the necessary values of resistors
        d=[0]*(len(x)-1+v)
        #The length of list d is the size of each row in matrix A
        for i in range(r):
            #We create a loop that iterates over the resistor list and modifies values in required positions in the list d
            if i<r:
                if x[j] in R[i][1:3]:#The resistor list values between 1 and 3 are taken because they hold the nodes between which the resistor lies
                    index=R[i].index(x[j])
                    #The variable 'index' stores the index of the current loop value and gets its index from the resistor list

                    if index==1:
                        index2=2
                    elif index==2:
                        index2=1
                    #The index value of the other element is also updated (It is 2 when the other is 1 and vice versa)
                    d[int(R[i][index])-1]+=float(R[int(i)][3])**-1
                    #The correct position of the list is added with the inverse of the resistor value
                    if int(R[i][index2])==0:#Care is taken to do no additions to the list when 0 is one of the nodal voltage values
                        continue
                    else:
                        #The correct position of the list is added with the inverse of the resistor value of the other node. 
                        d[int(R[i][index2])-1]-=float(R[int(i)][3])**-1
#All of these lists are appended to the martrix A. At this stage, A has all the resistor values updated in it
        A.append(d)
#We next add the current through the voltage sources data in the already existing rows in the matrix
#This is done by changing the values in the extra columns (after len(x)-1). That is, we change the value in v number of columns
    kk=0 #We initate a counter to know the position of the voltage source(within the v number of columns)
    
    
    for j in range(1,len(x)):

        for i in range(v):
                if x[j] in V[i][1:3] and kk<v :
                    kk+=1
#The same logic from resistors is used
                    indexx=V[i].index(x[j])
                    if indexx==1:
                        indexx2=2
                    if indexx==2:
                        indexx2=1
#Care must be taken to make sure that no additions or updations are made when the ground is encountered
                    if int(V[i][indexx])!=0 :
                        if indexx==1:
                            A[int(V[i][indexx])-1][kk+len(x)-2]+=1
                    #When a given node is first in the netlistpositions (2), we assign positive polarity to it
                        if indexx==2:
                            A[int(V[i][indexx])-1][kk+len(x)-2]-=1
                    #When a given node is second in the netlistpositions (3), we assign negative polarity to it
                    if int(V[i][indexx2])!=0 :
                        if indexx2==1:
                             A[int(V[i][indexx2])-1][kk+len(x)-2]+=1
                        if indexx2==2:
                             A[int(V[i][indexx2])-1][kk+len(x)-2]-=1
    #L
#We next update inductor values in the already made A matrix
    for j in range(1,len(x)):
        #Similar logic is applied as in the case of resistors and voltages
        #Variable lf stores the value of the inductor
        #Instead of adding the inverse of resistor value, we add the inverse of the impedance which is (jwl)
                            #w takes the value of the frequency needed
            #Similarly, the other node is accounted for as well
        for i in range(l):
            if x[j] in L[i][1:3]:
                lf=L[i][3]
                indexx=L[i].index(x[j])
                if indexx==1:
                    indexx2=2
                elif indexx==2:
                    indexx2=1
                A[j-1][int(L[i][indexx])-1]+=(1j*2*math.pi*float(w)*float(lf))**-1
               
                if int(L[i][indexx2])==0:
                    continue
                else:
                    A[j-1][int(L[i][indexx2])-1]-=(1j*2*math.pi*float(w)*float(lf))**-1
    #C The same logic is used again in the context of capacitors, but with a different impedance value of 1/(jwc)
    #The variable lf here stores the value of capacitance
    #We find the index of the current value and also store the index of the other value in another variable
           #Instead of adding the inverse of resistor value, we add the inverse of the impedance which is 1/jwc
                            #w takes the value of the frequency needed
            #Similarly, the other node is accounted for as well
      
    for j in range(1,len(x)):
        for i in range(c):
            if x[j] in C[i][1:3]:
     
                lf=C[i][3]
                indexx=C[i].index(x[j])
                if indexx==1:
                    indexx2=2
                if indexx==2:
                    indexx2=1
                
                A[j-1][int(C[i][indexx])-1]+=(1j*2*math.pi*float(w)*float(lf))
                if int(C[i][indexx2])==0:
                    continue
                else:
                    A[j-1][int(C[i][indexx2])-1]-=(1j*2*math.pi*float(w)*float(lf))
  #  The values now have to be added to the final rows of the A matrix that don't come under the nodes in x. These basically assign voltages to nodes and so on.
    for j in range(1,len(x)):
        d=[0]*(len(x)-1+v) #since we add an entire row, the new list d that has to be appended has to have len(x)-1+v number of elements in it
        for i in range(v):
            if x[j] in V[i][1:3]:
                    indexx=V[i].index(x[j]) #We iterate through the voltage lists and assign voltage differences between the required nodes
                    if indexx==1:
                        indexx2=2
                    if indexx==2:
                        indexx2=1
                    if int(V[i][indexx])!=0 :
                        if indexx==1:

                            d[int(V[i][indexx])-1]+=1
                        elif indexx==2:

                            d[int(V[i][indexx])-1]-=1
                    if int(V[i][indexx2])!=0 :

                        if indexx2==1:
                            d[int(V[i][indexx2])-1]+=1
                        elif indexx2==2:
                            d[int(V[i][indexx2])-1]-=1
#We should include a condition that checks the addition of unique lists and ignores the condition when 0 voltage i.e GND is encountered
        if list(set(d))!=[0] and (d not in A):
            A.append(d)

    fh.close()
    print(file)
    print('B=',B)
    print('A=',A)
    print('x=',gauss2_withpivot(A,B))    
    print(' ')
listss=['ckt1.netlist','ckt2.netlist','ckt3.netlist','ckt4.netlist','ckt5.netlist','ckt6.netlist','ckt7.netlist']
print('The x matrix is decoded as follows: The first n elements correspond to the nodes 1 through n. Every element after it till the end of the vector x is corresponding to the current through a voltage source')
print(' ')
for i in listss:
    create_matrix(i)
    




