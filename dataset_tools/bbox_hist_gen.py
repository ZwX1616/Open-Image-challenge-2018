# calculate bbox size and AR distribution
# (of people and bags)

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv
from time import time
import os

lbl_dir='./train-annotations-bbox_people_and_bag.csv'

target_labels_p=['/m/04yx4',
				'/m/03bt1vf',
				'/m/01bl7v',
				'/m/05r655',
				'/m/01g317']	

target_labels_b=['/m/01940j']
				#'/m/0hf58v5'
statements=['Person',
			'Bag']
			
pp_idx=[0,1,2,3,4]
bag_idx=[5,6]

W_p=0
H_p=0

W_b=0
H_b=0

wf=open('./pp_box_W_H.csv','w', newline='')
writer=csv.writer(wf)
wf2=open('./b_box_W_H.csv','w', newline='')
writer2=csv.writer(wf2)

start=time()
with open(lbl_dir,encoding='utf-8') as cfile:
    reader = csv.reader(cfile)
    readeritem=[]
    readeritem.extend([row for row in reader])
print('readtime=',time()-start)

for i,rows in enumerate(readeritem):
	
	if i%10000==0:
		print(i,'__',time()-start)
	if rows[2] in target_labels_p:
		writer.writerow([float(rows[5])-float(rows[4]),float(rows[7])-float(rows[6])])
		W_p+=1
		H_p+=1
		# W_p=np.append(W_p,)
		# H_p=np.append(H_p,)
	if rows[2] in target_labels_b:
		writer2.writerow([float(rows[5])-float(rows[4]),float(rows[7])-float(rows[6])])
		W_b+=1
		H_b+=1

# W_p=np.delete(W_p,0)
# H_p=np.delete(H_p,0)
# W_b=np.delete(W_b,0)
# H_b=np.delete(H_b,0)
print('---')
print('W_p,H_p:'+str(W_p)+','+str(H_p))
print('W_b,H_b:'+str(W_b)+','+str(H_b))
print('')
# plt.title('Plot 1', size=14)
# plt.xlabel('x-axis', size=14)
# plt.ylabel('y-axis', size=14)
# plt.plot(xData, yData1, color='b', linestyle='--', marker='o', label='y1 data')
# plt.plot(xData, yData2, color='r', linestyle='-', label='y2 data')
# plt.legend(loc='upper left')
# plt.savefig('images/plot1.png', format='png')
