_base_ = "../_base_/supervised_coco.py"
dataset_type = "CocoDataset"
data_root = "data/coco/"
coco_novel20 = (
    "airplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
    "cow", "dining table", "dog", "horse", "motorcycle", "person", "potted plant",
    "sheep", "couch", "train", "tv"
)
coco_all80 = (
    "person", "bicycle", "car", "motorcycle", "airplane", "bus",
    "train", "truck", "boat", "traffic light", "fire hydrant",
    "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
    "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop",
    "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
)
CLASSES = tuple(set(coco_all80).difference(set(coco_novel20)))
model = dict(
    backbone=dict(
        norm_cfg=dict(requires_grad=False),
        norm_eval=True,
        frozen_stages=1,
        style="caffe",
        depth=101,
        init_cfg=dict(
            type="Pretrained", checkpoint="open-mmlab://detectron2/resnet101_caffe"
        ),
    ),
    roi_head=dict(
        bbox_head=dict(
            num_classes=len(CLASSES),
        )
    ),
)
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=1,
    train=dict(
        type="RepeatDataset",
        times=5,
        dataset=dict(
            type=dataset_type,
            classes=CLASSES,
            ann_file=data_root + "annotations/semi_supervised/instances_train2017.${fold}@${percent}.json",
            img_prefix=data_root + "train2017/",
            filter_empty_gt=True,
        )
    ),
    val=dict(
        type=dataset_type,
        classes=CLASSES,
        ann_file=data_root + "annotations/instances_val2017.json",
        img_prefix=data_root + "val2017/",
        filter_empty_gt=True,
    ),
    test=dict(
        type=dataset_type,
        classes=CLASSES,
        ann_file=data_root + "annotations/instances_val2017.json",
        img_prefix=data_root + "val2017/",
        filter_empty_gt=True,
    ),
)
fold = 1
percent = 1
model_type = "FasterRCNN"
optimizer = dict(type="SGD", lr=0.01, momentum=0.9, weight_decay=0.0001)
lr_config = dict(step=[120000, 160000])
runner = dict(_delete_=True, type="IterBasedRunner", max_iters=180000)
evaluation = dict(interval=4000, metric="bbox")
checkpoint_config = dict(by_epoch=False, interval=4000, max_keep_ckpts=1)
auto_resume = False
fp16 = dict(loss_scale="dynamic")
work_dir = "work_dirs/${cfg_name}/${model_type}/${percent}/${fold}"

