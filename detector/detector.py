"""

Author: Pedro F. Proenza

This source modifies and extends the work done by:

Copyright (c) 2017 Matterport, Inc.
Licensed under the MIT License
Written by Waleed Abdulla

------------------------------------------------------------

Usage:

    # First make sure you have split the dataset into train/val/test set. e.g. You should have annotations_0_train.json
    # in your dataset dir.
    # Otherwise, You can do this by calling
    python3 split_dataset.py --dataset_dir ../data

    # Train a new model starting from pre-trained COCO weights on train set split #0
    python3 -W ignore detector.py train --model=coco --dataset=../data --class_map=./taco_config/map_10.csv --round 0

    # Continue training a model that you had trained earlier
    python3 -W ignore detector.py train  --dataset=../data --model=<model_name> --class_map=./taco_config/map_10.csv --round 0

    # Continue training the last model you trained with image augmentation
    python3 detector.py train --dataset=../data --model=last --round 0 --class_map=./taco_config/map_10.csv --use_aug

    # Test model and visualize predictions image by image
    python3 detector.py test --dataset=../data --model=<model_name> --round 0 --class_map=./taco_config/map_10.csv

    # Run COCO evaluation on a trained model
    python3 detector.py evaluate --dataset=../data --model=<model_name> --round 0 --class_map=./taco_config/map_10.csv

    # Check Tensorboard
    tensorboard --logdir ./models/logs

"""

import os
import time
import numpy as np
import json
import csv
import random

from dataset import Taco
import model as modellib
from model import MaskRCNN
from config import Config
import visualize
import utils
import matplotlib.pyplot as plt

# Root directory of the models
ROOT_DIR = os.path.abspath("./models")

# Path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")


def test_dataset(model, dataset, nr_images):

    for i in range(nr_images):

        image_id = (
            dataset.image_ids[i]
            if nr_images == len(dataset.image_ids)
            else random.choice(dataset.image_ids)
        )

        image, image_meta, gt_class_id, gt_bbox, gt_mask = modellib.load_image_gt(
            dataset, config, image_id, use_mini_mask=False
        )
        info = dataset.image_info[image_id]

        # current cost 20 seconds
        r = model.detect([image], verbose=0)[0]

        print(r["class_ids"].shape)
        print(r)
        # if r["class_ids"].shape[0] > 0:
        #     r_fused = utils.fuse_instances(r)
        # else:
        #     r_fused = r

        # fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 16))

        # # Display predictions
        # visualize.display_instances(
        #     image,
        #     r["rois"],  # interested
        #     r["masks"],
        #     r["class_ids"],  # interested
        #     dataset.class_names,
        #     r["scores"],
        #     title="Predictions_%d.png" % i,
        #     ax=ax1,
        # )


if __name__ == "__main__":
    args = {
        "command": "test",
        "model": "./models/logs/mask_rcnn_taco_0100.h5",
        "dataset": "../../data",
        "class_map": "./taco_config/map_10.csv",
        "round": 0,
    }
    print("Command: ", args["command"])
    print("Model: ", args["model"])
    print("Dataset: ", args["dataset"])
    print("Logs: ", DEFAULT_LOGS_DIR)

    # Read map of target classes
    class_map = {}
    map_to_one_class = {}
    with open(args["class_map"]) as csvfile:
        reader = csv.reader(csvfile)
        class_map = {row[0]: row[1] for row in reader}
        map_to_one_class = {c: "Litter" for c in class_map}

    # Load datasets
    dataset_test = Taco()
    taco = dataset_test.load_taco(
        args["dataset"], args["round"], "test", class_map=class_map, return_taco=True
    )
    dataset_test.prepare()
    nr_classes = dataset_test.num_classes

    # Configurations
    class TacoTestConfig(Config):
        NAME = "taco"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        DETECTION_MIN_CONFIDENCE = 10
        NUM_CLASSES = nr_classes
        USE_OBJECT_ZOOM = False

    config = TacoTestConfig()
    config.display()

    # Create model
    model = MaskRCNN(mode="inference", config=config, model_dir=DEFAULT_LOGS_DIR)

    # Select weights file to load
    model_path = args["model"]

    # Load weights
    model.load_weights(model_path, model_path, by_name=True)

    # Test
    test_dataset(model, dataset_test, len(dataset_test.image_ids))
