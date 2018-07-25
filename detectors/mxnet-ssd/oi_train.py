import os
import sys
import csv

# training parameters #

data_shape='512 384'
label_width='2710'
tensorboard='True'
batch_per_gpu=8
initial_learning_rate='0.01'
lr_decay='0.316' # lr decay rate
num_lr_decay=8 # number of times that lr decays
lr_step=8 # lr decay period
network='densenet-tiny-oi-cc'
# ------------------ #

str_args=''
str_args+=' --data-shape '+data_shape
str_args+=' --label-width '+label_width
str_args+=' --tensorboard '+tensorboard
str_args+=' --lr '+initial_learning_rate
str_args+=' --lr-factor '+lr_decay
lr_steps=str(lr_step)
for i in range(num_lr_decay-1):
	lr_steps+=','+str((i+2)*lr_step)
str_args+=' --lr-steps '+lr_steps
end_epoch=str((num_lr_decay+1)*lr_step)
str_args+=' --end-epoch '+end_epoch
# print(lr_steps+' '+end_epoch+' '+str(float(initial_learning_rate)*float((float(lr_decay)**num_lr_decay))))
str_args+=' --network '+network

if not int(len(sys.argv))==3:

	print('TWO arguments are required: ')
	print('-arg1 needs to be the index of the chosen subset (typically 1-12)'+'\n'+
			'-arg2 needs to be the gpus you want to use, separated by commas')
	sys.exit()

else:
	gpu=sys.argv[2]
	str_args+=' --gpu '+gpu

	batch_size=str(int(len(gpu.split(','))*batch_per_gpu))
	str_args+=' --batch-size '+batch_size
	
	train_path='/dat/train_series_'+sys.argv[1]+'.rec'
	str_args+=' --train-path '+train_path

	prefix='/res/oi_series_'+sys.argv[1]+'/oi_series_'+sys.argv[1]
	str_args+=' --prefix '+prefix

	cls_list_dir='/root/sources/sets/series/cls_series_'+sys.argv[1]+'.txt'
	with open(cls_list_dir,encoding='utf-8') as cfile:
	    reader = csv.reader(cfile,delimiter='\t')
	    classes=[]
	    classes.extend([row[1] for row in reader]) # row[0] if you use class code
	str_args+=' --num-class '+str(len(classes))
	classes='\''+','.join(classes)+'\''
	str_args+=' --class-names '+classes

	with open('/res/oi_series_'+sys.argv[1]+'_run.log','a+') as wf:
		wf.write('python3.6 train.py '+str_args+'\n')

	print('\n'+'python3.6 train.py '+str_args+'\n')
	print('logged to '+'/res/oi_series_'+sys.argv[1]+'_run.log')
	os.system('python3.6 train.py '+str_args)
 # 

