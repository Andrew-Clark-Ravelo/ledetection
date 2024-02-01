_base_ = "../_base_/supervised_voc.py"
dataset_type = "VOCDataset"
data_root = "data/VOCdevkit/"
CLASSES = (
    "bicycle", "bird", "boat", "bus", "car", "cat", "chair", "diningtable",
    "dog", "motorbike", "person", "pottedplant", "sheep", "train",
    "tvmonitor", "aeroplane", "bottle", "cow", "horse", "sofa"
)
model = dict(
    backbone=dict(
        norm_cfg=dict(requires_grad=False),
        norm_eval=True,
        frozen_stages=4,
        style="caffe",
        depth=101,
        init_cfg=dict(
            type="Pretrained", checkpoint="open-mmlab://detectron2/resnet101_caffe"
        ),
    ),
    neck=dict(frozen=True),
    rpn_head=dict(frozen=True),
    roi_head=dict(
        bbox_head=dict(
            frozen_layer_names=["shared_fcs"],
            num_classes=len(CLASSES),
        )
    ),
)
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type="RepeatDataset",
        times=5,
        dataset=dict(
            type=dataset_type,
            classes=CLASSES,
            ann_file=[
                data_root + "few_shot/vocsplit/${fold}/box_${shot}_2007_all_train.txt",
                data_root + "few_shot/vocsplit/${fold}/box_${shot}_2012_all_train.txt"
            ],
            img_prefix=[data_root + "VOC2007/", data_root + "VOC2012/"],
            filter_empty_gt=True,
        )
    ),
    val=dict(
        type=dataset_type,
        classes=CLASSES,
        ann_file=data_root + "VOC2007/ImageSets/Main/test.txt",
        img_prefix=data_root + "VOC2007/",
        filter_empty_gt=True,
    ),
    test=dict(
        type=dataset_type,
        classes=CLASSES,
        ann_file=data_root + "VOC2007/ImageSets/Main/test.txt",
        img_prefix=data_root + "VOC2007/",
        filter_empty_gt=True,
    ),
)
fold = "seed1"
shot = "10shot"
model_type = "FasterRCNN"
evaluation = dict(interval=4000, metric="mAP")
optimizer = dict(type="SGD", lr=0.001, momentum=0.9, weight_decay=0.0001)
lr_config = dict(step=[36000])
runner = dict(_delete_=True, type="IterBasedRunner", max_iters=40000)
checkpoint_config = dict(by_epoch=False, interval=4000, max_keep_ckpts=1)
auto_resume = False
fp16 = dict(loss_scale="dynamic")
load_from = "results/voc0712_base15/part2/${model_type}/r101/model_reset_surgery.pth"
work_dir = "work_dirs/${cfg_name}/${model_type}/${shot}/${fold}"

