import csv
import numpy as np
import cv2
from time import time
import os

"""
/m/04yx4 : Man
/m/03bt1vf : Woman
/m/01bl7v : Boy
/m/05r655 : Girl
/m/01g317 : Person
"""

lbl_dir='../train/label/train-annotations-bbox.csv'

target_labels=['/m/04yx4',
				'/m/03bt1vf',
				'/m/01bl7v',
				'/m/05r655',
				'/m/01g317']	

statements=['Man',
			'Woman',
			'Boy',
			'Girl',
			'Person']
			
pp_idx=[0,1,2,3,4]

counts=np.zeros(np.size(target_labels,0))

start=time()
with open(lbl_dir,encoding='utf-8') as cfile:
    reader = csv.reader(cfile)
    readeritem=[]
    readeritem.extend([row for row in reader])

print('readtime=',time()-start)
wf=open('../devkit_person/labels/train-bbox-people.csv','w+', newline='')
writer=csv.writer(wf)
wf2=open('../devkit_person/indexs/train.txt','w+', newline='')
writer2=csv.writer(wf2)

fn_old='666'
for i,rows in enumerate(readeritem):
	if i==0:
		writer.writerow([rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7]])
	if i%100000==0:
		print(i,'__',time()-start)
	for j in range(np.size(target_labels,0)):
		if rows[2]==target_labels[j] and rows[10]=='0' and os.path.isfile('../sources/train_img/'+rows[0]+'.jpg'): # rows[10] is isGrouped
			writer.writerow([rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7]])
			counts[j]+=1
			if fn_old!=rows[0]:
				writer2.writerow([rows[0]])
			fn_old=rows[0]
			
print('---')
for i in range(np.size(target_labels,0)):
	print(statements[i]+':'+str(int(counts[i])))
print('---')
print('Person Sum:'+str(int(np.sum(counts))))
print('')