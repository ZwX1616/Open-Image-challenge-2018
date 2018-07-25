# split the OID 600-class training set into several 50-class subsets

# author: wx. zhang

# import pdb; pdb.set_trace()
import csv
from time import time
import sys
import os
import numpy as np
import random
import cv2
# --

len_split=50
img_num=5000 # minimum and maximum image per class

cls_dict_dir='../train/label/class-descriptions-boxable.csv'
cls_order_dir='../train_distn_sorted.txt'
lbl_dir='../train/label/train-annotations-bbox.csv'

# convert csv file to dict (name-->code)
def row_csv2dict(csv_file):
    dict_club={}
    with open(csv_file)as f:
        reader=csv.reader(f,delimiter=',')
        for row in reader:
            dict_club[row[1]]=row[0]
    return dict_club

# generate mxnet formatted training .lst files
def gen_lst(set_idx):

	print('executing gen_lst..')
	cls_list_dir='../sources/sets/series/cls_series_'+str(set_idx)+'.txt'

	start=time()
	with open(cls_list_dir,encoding='utf-8') as cfile:
	    reader = csv.reader(cfile,delimiter='\t')
	    target_classes=[]
	    target_classes.extend([row[0] for row in reader])
	print('class list '+str(set_idx)+' readtime=',time()-start)

	start=time()
	with open(lbl_dir,encoding='utf-8') as cfile:
	    reader = csv.reader(cfile)
	    readeritem=[]
	    readeritem.extend([row for row in reader])
	print('label csv readtime=',time()-start)

	counts=np.zeros(len(target_classes))
	wf=open('../sources/rec_files/train_series_'+str(set_idx)+'.lst','w+')
	writer=csv.writer(wf)

	fn_old='666'
	cls_old='999'
	writeok=False
	img_idx=0
	for i,rows in enumerate(readeritem):
		if i%100000==0:
			print(str(i)+'__'+'{:.3f}'.format(time()-start))
			print('min count='+str(np.min(counts))+' / '+str(img_num))
			print('max count='+str(np.max(counts))+' / '+str(img_num))
		# rows[10] indicates if it is grouped label, unused
		if rows[2] in target_classes and rows[10]=='0' and os.path.isfile('../sources/train_img/'+rows[0]+'.jpg') and os.path.isfile('../sources/train_xml/'+rows[0]+'.xml') and not os.path.isfile('../sources/train_dummy/'+rows[0]+'.txt'): 
			# use horizontal images only, for simplicity
			# img=cv2.imread('../sources/train_img/'+rows[0]+'.jpg')
			# W=np.size(img,1)
			# H=np.size(img,0)
			# if W<H:
			# 	continue

			if fn_old!=rows[0]:
				if fn_old!='666':
					if writeok==True:
						tmp=str(img_idx)+'\t'+str(2)+'\t'+str(5)+'\t'+bboxes+fn_old+'.jpg'
						writer.writerow([tmp])
						img_idx+=1
				bboxes=''
				cls_old='999'
				writeok=False

			# if isRotated==False:
			bboxes+=str(target_classes.index(rows[2]))+'\t'+rows[4]+'\t'+rows[6]+'\t'+rows[5]+'\t'+rows[7]+'\t'
			# else:
				# bboxes+=str(target_classes.index(rows[2]))+'\t'+rows[6]+'\t'+str(1-float(rows[5]))+'\t'+rows[7]+'\t'+str(1-float(rows[4]))+'\t'
			
			if cls_old!=rows[2]:
				if counts[target_classes.index(rows[2])]>=img_num:
					cls_old=rows[2]
					fn_old=rows[0]
					continue
				counts[target_classes.index(rows[2])]+=1
				writeok=True
			cls_old=rows[2]
			fn_old=rows[0]

		if np.min(counts)>=img_num:
			print('job completed! voc index file generated: /sources/rec_files/train_series_'+str(set_idx)+'.lst')
			print('min count='+str(np.min(counts))+' / '+str(img_num))
			print('max count='+str(np.max(counts))+' / '+str(img_num))
			return 0

	print('job completed! voc index file generated: /sources/rec_files/train_series_'+str(set_idx)+'.lst')
	print('min count='+str(np.min(counts))+' / '+str(img_num))
	print('max count='+str(np.max(counts))+' / '+str(img_num))

# generate Pascal voc formatted training indexs
def gen_voc(set_idx):

	print('executing gen_voc..')
	cls_list_dir='../sources/sets/series/cls_series_'+str(set_idx)+'.txt'

	start=time()
	with open(cls_list_dir,encoding='utf-8') as cfile:
	    reader = csv.reader(cfile,delimiter='\t')
	    target_classes=[]
	    target_classes.extend([row[0] for row in reader])
	print('class list '+str(set_idx)+' readtime=',time()-start)

	start=time()
	with open(lbl_dir,encoding='utf-8') as cfile:
	    reader = csv.reader(cfile)
	    readeritem=[]
	    readeritem.extend([row for row in reader])
	print('label csv readtime=',time()-start)

	## shuffling will cause the uniqueness bug
	# start=time()
	# random.shuffle(readeritem)
	# print('shuffle time=',time()-start)

	counts=np.zeros(len(target_classes))
	wf=open('../sources/sets/train_series_'+str(set_idx)+'.txt','w+')
	writer=csv.writer(wf)

	fn_old='666'
	cls_old='999'
	writeok=False
	for i,rows in enumerate(readeritem):
		if i%100000==0:
			print(str(i)+'__'+'{:.3f}'.format(time()-start))
			print('min count='+str(np.min(counts))+' / '+str(img_num))
			print('max count='+str(np.max(counts))+' / '+str(img_num))
		# rows[10] indicates if it is grouped label, unused
		if rows[2] in target_classes and rows[10]=='0' and os.path.isfile('../sources/train_img/'+rows[0]+'.jpg') and os.path.isfile('../sources/train_xml/'+rows[0]+'.xml') and not os.path.isfile('../sources/train_dummy/'+rows[0]+'.txt'): 
			# use horizontal images only, for simplicity
			# img=cv2.imread('../sources/train_img/'+rows[0]+'.jpg')
			# W=np.size(img,1)
			# H=np.size(img,0)
			# if W<H:
			# 	continue

			if fn_old!=rows[0]:
				if fn_old!='666':
					if writeok==True:
						writer.writerow([fn_old])
				cls_old='999'
				writeok=False
			if cls_old!=rows[2]:
				if counts[target_classes.index(rows[2])]>=img_num:
					cls_old=rows[2]
					fn_old=rows[0]
					continue
				counts[target_classes.index(rows[2])]+=1
				writeok=True
			cls_old=rows[2]
			fn_old=rows[0]

		if np.min(counts)>=img_num:
			print('job completed! voc index file generated: /sources/sets/train_series_'+str(set_idx)+'.txt')
			print('min count='+str(np.min(counts))+' / '+str(img_num))
			print('max count='+str(np.max(counts))+' / '+str(img_num))
			return 0

	print('job completed! voc index file generated: /sources/sets/train_series_'+str(set_idx)+'.txt')
	print('min count='+str(np.min(counts))+' / '+str(img_num))
	print('max count='+str(np.max(counts))+' / '+str(img_num))

def prepare():

	print('executing..')
	cls_dict=row_csv2dict(cls_dict_dir)

	with open(cls_order_dir,encoding='utf-8') as cfile:
	    reader = csv.reader(cfile,delimiter='\t')
	    classes=[]
	    classes.extend([row[0] for row in reader])

	for i in range(len(classes)//len_split):
		wf=open('../sources/sets/series/cls_series_'+str(i+1)+'.txt','w+', newline='')
		writer=csv.writer(wf)
		for j in range(len_split):
			tmp='\t'.join([cls_dict[classes[len_split*i+j]], classes[len_split*i+j]])
			writer.writerow([tmp])

# main():
if not int(len(sys.argv))==2 and not int(len(sys.argv))==3: 
	print('ONE or TWO arguments are required:')
	print('-arg1 needs to be pre/voc/mxlst'+'\n'+
			'pre: generate txt for each subset'+'\n'+
			'voc: generate voc index files for selected subset'+'\n'+
			'mxlst: generate lst file for selected subset')
	print('-arg2 needs to be the index of the chosen subset (typically 1-12) if arg1 is voc or mxlst')
	sys.exit()

if sys.argv[1]=='pre':
	prepare()

elif sys.argv[1]=='voc':
	if not int(len(sys.argv))>=3: 
		print('-arg2 needs to be the index of the chosen subset (typically 1-12) if arg1 is voc or mxlst')
		sys.exit()
	if not int(sys.argv[2])>0: 
		print('-arg2 needs to be the index of the chosen subset (typically 1-12) if arg1 is voc or mxlst')
		sys.exit()
	gen_voc(int(sys.argv[2]))

elif sys.argv[1]=='mxlst':
	if not int(len(sys.argv))>=3: 
		print('-arg2 needs to be the index of the chosen subset (typically 1-12) if arg1 is voc or mxlst')
		sys.exit()
	if not int(sys.argv[2])>0: 
		print('-arg2 needs to be the index of the chosen subset (typically 1-12) if arg1 is voc or mxlst')
		sys.exit()
	gen_lst(int(sys.argv[2]))

else:
	print('-arg1 needs to be pre/voc/mxlst'+'\n'+
			'pre: generate txt for each subset'+'\n'+
			'voc: generate voc index files for selected subset'+'\n'+
			'mxlst: generate lst file for selected subset')

