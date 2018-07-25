import os
import cv2
import numpy as np

filelist=os.listdir('../sources/train_img/')

for file in filelist:
	if filelist.index(file)%1000==0:
		print(str(filelist.index(file)))
	img=cv2.imread('../sources/train_img/'+file)
	W=np.size(img,1)
	H=np.size(img,0)
	if W<H:
		with open('../sources/train_dummy/'+file[:-4]+'.txt','w+') as tmp:
			pass