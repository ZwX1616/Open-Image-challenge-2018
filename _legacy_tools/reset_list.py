import os
import csv

with open('../devkit_person/indexs/train_real.txt') as cfile:
    reader = csv.reader(cfile)
    readeritem=[]
    readeritem.extend([row for row in reader])
	
wf=open('../devkit_person/indexs/train.txt','w+', newline='')
writer=csv.writer(wf)

for i,rows in enumerate(readeritem):
	if i%10000==0:
		print(i)
	if os.path.isfile('../devkit_person/images/'+rows[0]+'.jpg'):
		writer.writerow([rows[0]])