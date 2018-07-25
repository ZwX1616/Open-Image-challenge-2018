### install deps for image
```
apt-get install -y python3.6-dev python3-tk
pip3.6 install opencv-python easydict cython matplotlib scikit-image
```
### start docker with mask rcnnn image

# docker run --rm -it -v /home/chuengwaising/ws:/ws mxnet-cu90/python:1.2.0-roialign
# docker run --rm -it -v /home/chuengwaising/ws/mx-rcnn:/mnt -v /home/chuengwaising/ws:/ws mxnet/python:1.2.0_gpu_cuda9-dev bash
docker run --rm -it -v /home/chuengwaising/ws/mx-rcnn:/mnt -v /data/david/open-image-v4/devkit_person:/devkit mxnet/python:1.2.0_gpu_cuda9-dev bash

### test run
python3.6 demo.py --image ./samples/car.jpg --img-long-side 1024 --img-short-side 685 --gpu 0 --network resnet101 --dataset coco --params ./ckpt/resnet_coco-0010.params

## train
python3 train.py --network resnet101 --dataset google_person --epochs 10 --lr 0.01 --lr-decay-epoch 1 --save-prefix /devkit/outputs/google_person --img-long-side 512 --img-short-side 384 --gpus 0,1,2,3 --rpn-post-nms-topk 100

## train on small subset
# python3 train.py --network resnet101 --dataset google_person --imageset train_small --epochs 10 --lr 0.01 --lr-decay-epoch 1 --save-prefix /devkit/outputs/google_person --img-long-side 512 --img-short-side 384 --gpus 0,1,2,3 --rpn-post-nms-topk 100

python3 train.py --network resnet101 --dataset google_person --imageset train_small --epochs 40 --lr 0.001 --lr-decay-epoch 22,24,26,28,30,32,34,36,38 --save-prefix /devkit/outputs/google_person --img-long-side 512 --img-short-side 384 --gpus 6,7 --rpn-post-nms-topk 100 --resume /devkit/outputs/google_person_sub-0020.params --start-epoch 20

## with cc
python3 train.py --network resnet101 --dataset google_person --imageset train_small --epochs 45 --lr 0.001 --lr-decay-epoch 10,20,30 --save-prefix /devkit/outputs/google_person_cc --img-long-side 512 --img-short-side 384 --gpus 4,5 --rpn-post-nms-topk 100


## small evaluate
python3 test.py --network resnet101 --dataset google_person --imageset valid --img-long-side 512 --img-short-side 384 --gpu 6,7 --params /devkit/outputs/google_person_sub-0035.params --rpn-post-nms-topk 50