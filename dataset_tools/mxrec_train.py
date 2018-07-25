import os
import sys

if not int(len(sys.argv))==2:
	print('ONE argument is required: index of the chosen subset (typically 1-12)')
	sys.exit()
else:
	if not int(sys.argv[1])>0: 
		print('ONE argument is required: index of the chosen subset (typically 1-12)')
		sys.exit()
	else:
		os.system('python3 im2rec_rs.py --resize 1 --pack-label /dat/train_series_'+sys.argv[1]+'.lst '+'/root/sources/train_img/')
