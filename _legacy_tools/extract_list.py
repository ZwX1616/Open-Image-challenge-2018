import os
import csv
import random

with open('../devkit_person/indexs/train.txt') as cfile:
    reader = csv.reader(cfile)
    readeritem=[]
    readeritem.extend([row for row in reader])
	
wf=open('../devkit_person/indexs/valid.txt','w+', newline='')
writer=csv.writer(wf)

random.shuffle(readeritem)
for i,rows in enumerate(readeritem):
	if i%1000==0:
		print(i)
	if os.path.isfile('../devkit_person/images/'+rows[0]+'.jpg'):
		writer.writerow([rows[0]])
	if i>=5000:
		break