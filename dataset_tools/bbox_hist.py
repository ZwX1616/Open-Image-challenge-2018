import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv
from time import time
import os

start=time()
with open('./b_box_W_H.csv',encoding='utf-8') as cfile:
    reader = csv.reader(cfile)
    readeritem=[]
    readeritem.extend([row for row in reader])
print('readtime=',time()-start)

W_p=np.zeros(1)
H_p=np.zeros(1)

for i,rows in enumerate(readeritem):
	
	if i%10000==0:
		print(i,'__',time()-start)
	W_p=np.append(W_p,float(rows[0]))
	H_p=np.append(H_p,float(rows[1]))
	if i==700000:
		break
	
W_p=np.delete(W_p,0)
H_p=np.delete(H_p,0)

print('W_p,H_p:'+str(np.size(W_p))+','+str(np.size(H_p)))

# __,__,H=np.histogram2d(W_p, H_p)

plt.figure(num=1, figsize=(8, 8))
plt.title('bbox histogram (bag)', size=18)
plt.xlabel('W', size=18)
plt.ylabel('H', size=18)
#plt.hist2d(W_p, H_p,bins=100, range=[[0,1],[0,1]])
plt.hist(H_p,bins=100, range=(0,1))
plt.savefig('./plotbH.png', format='png')
