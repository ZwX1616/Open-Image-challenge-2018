# Open-Image-challenge-2018
my solution to Google's Open Image Dataset v4 challenge

*for quick setup, read /Note/APPNOTE.py

folders organization:
(now supports: mxnet-SSD training (and predicting))
(still working on the voc format conversion)

```
root
├── sources
│   ├── train_img 
│             ├── 0123456789ABCDEF.jpg //downloaded training images 
│             ├── ...
│   ├── train_xml
│             ├── 0123456789ABCDEF.xml //voc formatted label, generated using gen_xml in /root/dataset_tools
│             ├── ...
│   ├── train_dummy
│             ├── 0123456789ABCDEF.txt //only exists if the JPG's orientation is portrait
│             ├── ...
│   ├── test_img 
│             ├── 0123456789ABCDEF.jpg //downloaded testing images 
│             ├── ...
│   ├── valid_img 
│             ├── 0123456789ABCDEF.jpg //downloaded val images, optional
│             ├── ...
│   ├── sets 
│             ├── series
│                       ├── cls_series_1.txt //subset classes, generated using split_train in /root/dataset_tools
│                       ├── ...
│             ├── train_series_1.txt //voc formatted subset image indexs, generated using split_train in /root/dataset_tools
│             ├── ...
│   └── rec_files
│             ├── train_series_1.lst //mxnet formatted subset label, generated using split_train in /root/dataset_tools
│             ├── train_series_1.rec //mxnet formatted subset image+label pack, generated using mxrec_train in /root/dataset_tools
│             ├── train_series_1.idx //mxnet formatted indexs, generated together with the rec file
│             ├── ...
├── train
│        ├── label
│                ├── train-annotations-bbox.csv
│                ├── validation-annotations-bbox.csv
│                ├── test-annotations-bbox.csv
│                ├── class-descriptions-boxable.csv
│                ├── challenge-2018-class-descriptions-500.csv
│                └── challenge-2018-attributes-description.csv
│        ├── relation
│                ├── ... (some vrd csv)
├── dataset_tools
│   └── <dataset_tools>
│
├── detectors
│   └── <detector models>
│
├── Note
│   └── APPNOTE.py
│
├── outputs
│   └── <training result folders>
│ 
├── predictions
│   ├── <test set prediction results for each series>
│   └── submission.csv
│
└── train_distn_sorted.txt //class names sorted by number of samples
```
  
   (under construction...)
