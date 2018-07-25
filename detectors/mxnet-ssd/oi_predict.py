
# predict and save results in Open Image submission format
# user args: subset, epoch, gpu

import os
import sys
import csv
from pathlib import Path
import argparse
import mxnet as mx

import tools.find_mxnet
from detect.detector import Detector
from symbol.symbol_factory import get_symbol


test_all=True # should be True 


# prediction parameters #

thresh=0.2 # you may want to change this

network='densenet-tiny-oi-cc'
nms_thresh=0.5
force_nms=True
data_shape=512
background_id=-1
show_timer=True
# ------------------ #

def get_detector(net, prefix, epoch, data_shape, mean_pixels, ctx, num_class,
                 nms_thresh=0.5, force_nms=True, nms_topk=400,
                 threshold=0.6, background_id=-1):
    """
    wrapper for initialize a detector

    Parameters:
    ----------
    net : str
        test network name
    prefix : str
        load model prefix
    epoch : int
        load model epoch
    data_shape : int
        resize image shape
    mean_pixels : tuple (float, float, float)
        mean pixel values (R, G, B)
    ctx : mx.ctx
        running context, mx.cpu() or mx.gpu(?)
    num_class : int
        number of classes
    nms_thresh : float
        non-maximum suppression threshold
    force_nms : bool
        force suppress different categories
    """
    if net is not None:
        net = get_symbol(net, data_shape, num_classes=num_class, nms_thresh=nms_thresh,
            force_nms=force_nms, nms_topk=nms_topk,
            threshold=threshold, background_id=background_id)
    detector = Detector(net, prefix, epoch, data_shape, mean_pixels, ctx=ctx)
    return detector


if not int(len(sys.argv))==4:

    print('THREE arguments are required: ')
    print('-arg1 needs to be the index of the chosen subset (typically 1-12)'+'\n'+
            '-arg2 needs to be the epoch of your trained model'+'\n'+
            '-arg3 needs to be the gpu you want to use (only one); use -1 if you want to use the cpu')
    sys.exit()

else:
    
    if int(sys.argv[3])==-1:
        ctx = mx.cpu()
    else:
        ctx = mx.gpu(int(sys.argv[3]))

    cls_list_dir='/root/sources/sets/series/cls_series_'+sys.argv[1]+'.txt'
    with open(cls_list_dir,encoding='utf-8') as cfile:
        reader = csv.reader(cfile,delimiter='\t')
        class_names=[]
        class_names.extend([row[0] for row in reader]) # row[1] if you use class name

    prefix='/res/oi_series_'+sys.argv[1]+'/oi_series_'+sys.argv[1]
    epoch=int(sys.argv[2])

    dir='/root/sources/test_img/'
    image_list=[i.as_posix() for i in Path(dir).glob("*.jpg")]
    if not test_all:
        image_list=image_list[0:1000]

    detector = get_detector(network, prefix, epoch,
                            data_shape,
                            (123, 117, 104),
                            ctx, len(class_names), nms_thresh, force_nms,
                            threshold=thresh, background_id=background_id)
    # run detection
    print('number of test images: '+str(len(image_list)))
    detector.detect_and_save_result(image_list, dir, str(sys.argv[1]), None,
                                  class_names, thresh, show_timer)
