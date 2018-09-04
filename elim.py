import numpy as np
import sys
from tabulate import tabulate
Zero_point = sys.argv[1]
Zero_point=int(Zero_point)
Etol = 1e-5
Dtol = 1.5e-2

labels = np.loadtxt('conf.txt', dtype=np.str, delimiter=' ', usecols=[0])
energy = np.loadtxt('conf.txt', delimiter=' ', usecols=[1])
dipole = np.loadtxt('conf.txt', delimiter=' ', usecols=[2])
ConfNo=[]
ConfNo.append(1)
ConfCount=1
ConfList=[]
RelEnergyList=[]
table=[]
matches = str()
matrix=[]
changes=0

for i in range(len(energy)):
    matrix.append([])
    matrix[i].append(i)
    for j in range(i):
        Etemp = abs(energy[i]-energy[j])
        Diptemp = abs(dipole[i]-dipole[j])
        if Etemp < Etol and Diptemp < Dtol:
            matrix[i].append(j)
            matrix[j].append(i)
            missing_j=list(set(matrix[i]) - set(matrix[j]))
            missing_i=list(set(matrix[j]) - set(matrix[i]))
            if missing_j!=[]:
                for k in range(len(missing_j)):
                    matrix[j].append(missing_j[k])
                    matrix[missing_j[k]].append(j)
                    changes=1
            if missing_i!=[]:
                for k in range(len(missing_i)):
                    matrix[i].append(missing_i[k])
                    matrix[missing_i[k]].append(i)
                    changes=1

while (changes>0):
    changes=0
    for i in range(len(energy)):
        for j in range(i):
            Etemp = abs(energy[i]-energy[j])
            Diptemp = abs(dipole[i]-dipole[j])
            if Etemp < Etol and Diptemp < Dtol:
                missing_j=list(set(matrix[i]) - set(matrix[j]))
                missing_i=list(set(matrix[j]) - set(matrix[i]))
                if missing_j!=[]:
                    for k in range(len(missing_j)):
                        matrix[j].append(missing_j[k])
                        matrix[missing_j[k]].append(j)
                        changes+=1
                if missing_i!=[]:
                    for k in range(len(missing_i)):
                        matrix[i].append(missing_i[k])
                        matrix[missing_i[k]].append(i)
                        changes+=1
#sort list
for i in range(len(energy)):
    matrix[i]=list(set(matrix[i]))
    matrix[i].sort()
zipped = zip(energy,labels, dipole, matrix)
zipped.sort()

energy, labels, dipole, matrix= zip(*zipped)

for i in range(1,len(energy)):
    tjek=0
    for j in range(i):
        if matrix[i]==matrix[j]:
            tjek=1
            gem=j
    if tjek==1:
        ConfNo.append(ConfNo[gem])
    else:
        ConfCount+=1
        ConfNo.append(ConfCount)

zipped = zip(ConfNo, energy,labels, dipole)
zipped.sort()

ConfNo, energy, labels, dipole = zip(*zipped)

for i in range(len(energy)):
    ConfList.append(ConfNo[i])
    RelativeE = (energy[i] - energy[0])*627.5
    RelEnergyList.append(RelativeE)

#deletes extra numbers of same conf
for i in range(1,len(energy)):
    if ConfNo[i]==ConfNo[i-1]:
        ConfList[i]=' '

for i in range(len(energy)):
    table.append([])
    table[i].append(ConfList[i])
    table[i].append(labels[i])
    table[i].append(energy[i])
    table[i].append(dipole[i])
    table[i].append(RelEnergyList[i])

if Zero_point == 0:
    print tabulate(table, headers=["Conf_No.","Name","Energy(h)","Dipole(D)","Relative_E_(kcal/mol)"], tablefmt="plain",floatfmt=".4f")
elif Zero_point == 1:
    print tabulate(table, headers=["Conf_No.","Name","E+ZPVE(h)","Dipole(D)","Relative_E_(kcal/mol)"], tablefmt="plain",floatfmt=".4f")

print max(ConfNo), 'unique conformers'

f = open('myfile', 'w')
f.write('Succes\nSucces')
f.close()
