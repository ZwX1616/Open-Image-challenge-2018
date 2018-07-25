Open Image Detection challenge 2018

'''
The training set has been split into 12 subsets, based on sample amounts.
Each subset will be trained separately, and the model will detect these classes in the test set.
The detection results from all 12 models will be joined together to make the final result. 
'''

'''
host: 192.168.11.172
'''
=========================================================
----- mxnet SSD ----- # data will be resized to 512*384
--- ith dataset preparation ---
# in shell
cd /data/david/open-image-v4/dataset_tools/
python3 split_train.py mxlst i

# in docker (docker run -it --rm -v /data/david/open-image-v4/detectors/mxnet-ssd:/mnt -v /data/david/open-image-v4/sources/rec_files:/dat -v /data/david/open-image-v4/outputs:/res -v /data/david/open-image-v4:/root mxnet/python:1.2.0_gpu_cuda9-dev)
cd /root/dataset_tools/
python3 mxrec_train.py i

--- docker ---
docker run -it --rm -v /data/david/open-image-v4/detectors/mxnet-ssd:/mnt -v /data/david/open-image-v4/sources/rec_files:/dat -v /data/david/open-image-v4/outputs:/res -v /data/david/open-image-v4:/root mxnet-cu90-ssd:v0.1 bash

--- train the ith subset ---
# in docker
cd /mnt
python3.6 oi_train.py i #,#,... (# is the index of GPU)
# this is for training from scratch, if you want to resume training, please refer to the log file generated upon the beginning of this training and add argument '--resume xx' (you may need to change the initial lr as well)

--- do prediction on the testset [ith model] ---
# in docker
cd /mnt
python3.6 oi_predict.py i epoch gpu


--- combine results from all 12 models ---
# in shell
cd /data/david/open-image-v4/dataset_tools/


=========================================================




----- mxnet Faster RCNN -----
--- ith dataset preparation ---
# in shell
cd /data/david/open-image-v4/dataset_tools/
python3 split_train.py voc i

--- docker ---
docker run -it --rm -v /data/david/open-image-v4/detectors/mx-rcnn:/mnt -v /data/david/open-image-v4/sources:/devkit -v /data/david/open-image-v4/outputs/frcnn:/res mxnet/python:1.2.0_gpu_cuda9-dev bash

--- train the ith subset ---
# in docker
cd /mnt