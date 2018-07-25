from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

import numpy as np
import csv
import cv2
# from PIL import Image as pilimg

from time import time

im_path='../sources/train_img/'

def dict_to_xml_str(tag, d):
	parts = ['<{}>\n'.format(tag)]
	for key, val in d.items():
		parts.append('<{0}>{1}</{0}>\n'.format(key,val))
	parts.append('</{}>\n'.format(tag))
	return ''.join(parts)

def dict_to_xml_str_sub(tag, d):
	parts = []
	for key, val in d.items():
		parts.append('<{0}>{1}</{0}>\n'.format(key,val))
	return ''.join(parts)

def dict_to_xml_str_sub_next(tag, d):
	parts = ['\n']
	for key, val in d.items():
		parts.append('<{0}>{1}</{0}>\n'.format(key,val))
	return ''.join(parts)

def gen_xml(img_id,bboxs):

# inputs:
# img_id - str: id of target image
# bboxs - n*6: n*[cls_name, xmin, ymin, xmax, ymax, diff]

# output: xml file with the following necessary information
# <annotation> 
# - <size>
# - - <width>
# - - <height>
# - <object>
# - - <name> ('person')
# - - <difficult>
# - - <bndbox>
# - - - <xmin>
# - - - <ymin>
# - - - <xmax>
# - - - <ymax>
# ..more objects...
	
	out='<annotation>\n'
#	W=200
#	H=100
	img=cv2.imread('../sources/train_img/'+img_id+'.jpg')
	W=np.size(img,1)
	H=np.size(img,0)
	
	# copy and rotate the files by the way
	# if H>W:
		# img = img.transpose(pilimg.ROTATE_90)
		# ng=img.resize((512, 384))	
		# ng.save('../devkit_person/images/'+img_id+'.jpg')
		# isRotated=True
		
	# else:
		# ng=img.resize((512, 384))
		# ng.save('../devkit_person/images/'+img_id+'.jpg')
		# isRotated=False
	# print(isRotated)
	size_dict={'width':str(W),'height':str(H)}
#	size_dict={'width':str(W),'height':str(H)}
	size_text=dict_to_xml_str('size',size_dict)
	out+=size_text
	multiobj_text=''
	for bbox in bboxs:
		# if isRotated==False:
		xy_dict={'xmin':str(float(bbox[1])*W),'ymin':str(float(bbox[2])*H),'xmax':str(float(bbox[3])*W),'ymax':str(float(bbox[4])*H)}
	# else:
		# xy_dict={'xmin':str(float(bbox[2])*W),'ymin':str(384-float(bbox[3])*H),'xmax':str(float(bbox[4])*512),'ymax':str(384-float(bbox[1])*384)}
		xy_text=dict_to_xml_str_sub_next('bndbox',xy_dict)
		obj_dict={'name':bbox[0],'difficult':bbox[5],'bndbox':xy_text}
		obj_text=dict_to_xml_str('object',obj_dict)
		multiobj_text+=obj_text
	out+=multiobj_text
	out+='</annotation>'
	
	with open('../sources/train_xml/'+img_id+'.xml', 'w+') as f:
		f.write(out)

def row_csv2dict(csv_file):
	dict_club={}
	with open(csv_file)as f:
		reader=csv.reader(f,delimiter=',')
		for row in reader:
			dict_club[row[0]]=row[1]
	return dict_club

	# ---main--- #
# lbl_dir='../train/label/train-annotations-bbox.csv'
cls_dict=row_csv2dict('../train/label/class-descriptions-boxable.csv')	

start=time()
with open('../train/label/train-annotations-bbox.csv') as cfile:
	reader = csv.reader(cfile)
	readeritem=[]
	readeritem.extend([row for row in reader])
print('readtime:'+str(time()-start))
id_old='666'
bboxs=[]
for i,rows in enumerate(readeritem):
		if i%1000==0:
			print(i,' time:',time()-start)
		if i>0:
			if rows[0]!=id_old:
				if id_old!='666':
					gen_xml(id_old,bboxs)
				bboxs=[]
				id_old=rows[0]
				
			diff=1-int(rows[3])
			bboxs.append([cls_dict[rows[2]],rows[4],rows[6],rows[5],rows[7],str(diff)])

gen_xml(id_old,bboxs)
print('xml generation completed!')
# bboxs=[['person',0.638750,0.243333,0.998750,0.998333,0],['person',0.596250,0.265000,0.808750,0.998333,0]]
# gen_xml('0000071d71a0a6f6',bboxs)