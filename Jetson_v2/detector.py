from math import cos, sqrt
import os
import cv2
from multiprocessing import Array

from model import MaskRCNN
from config import Config


class Detector:
    ROOT_DIR = os.path.abspath("./models")
    DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")
    FOCAL_FACTOR = 2.0

    def __init__(self, viewAngle: float, height: float, baseline: float = 10.0) -> None:
        self.detecting = True
        self.viewAngle = viewAngle
        self.baseline = baseline
        self.height = height
        self.class_name = [
            "BG",
            "Bottle",
            "Bottle cap",
            "Can",
            "Cigarette",
            "Cup",
            "Lid",
            "Other",
            "Plastic bag + wrapper",
            "Pop tab",
            "Straw",
        ]

        args = {
            "command": "test",
            "model": "./models/mask_rcnn_taco_0100.h5",
            # "dataset": "../../data",
            "class_map": "./taco_config/map_10.csv",
            "round": 0,
        }
        print("Command: ", args["command"])
        print("Model: ", args["model"])
        # print("Dataset: ", args["dataset"])

        class TacoTestConfig(Config):
            NAME = "taco"
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
            DETECTION_MIN_CONFIDENCE = 10
            USE_OBJECT_ZOOM = False
            NUM_CLASSES = 11

        config = TacoTestConfig()
        config.display()

        self.model = MaskRCNN(
            mode="inference", config=config, model_dir=self.DEFAULT_LOGS_DIR
        )
        model_path = args["model"]
        self.model.load_weights(model_path, model_path, by_name=True)

    def calCoordinateFromPixel(self, x1: float, y1: float, x2: float, y2: float):
        X_SHIFT = 10  # cm
        disparity = x1 - x2
        if disparity == 0:
            disparity = y1 - y2
        distance = self.FOCAL_FACTOR * self.baseline / disparity
        y = distance * cos(self.viewAngle)
        x = x1 * y / self.FOCAL_FACTOR - X_SHIFT
        return x, y

    def start(self, modelResult: Array):
        cam1 = cv2.VideoCapture(0)  # left camera
        cam2 = cv2.VideoCapture(1)  # right camera
        while self.detecting:
            _, img1 = cam1.read()
            _, img2 = cam2.read()
            r1 = self.model.detect([img1], verbose=0)[0]
            r2 = self.model.detect([img2], verbose=0)[0]

            # TODO: modelResult[0] = 0/1, have or dont have trash detected
            # TODO: modelResult[1] = x, x position
            # TODO: modelResult[2] = y, y position

            # x----y
            #      |
            #      |
            #      |
            #      |
            #   (front)

            distance = 100000
            x1, x2, y1, y2 = 0, 0, 0, 0
            for idx1, class1 in enumerate(r1["class_ids"]):
                for idx2, class2 in enumerate(r2["class_ids"]):
                    if class1 == class2:
                        _x1 = (r1["rois"][idx1][1] + r1["rois"][idx1][3]) / 2
                        _y1 = (r1["rois"][idx1][0] + r1["rois"][idx1][2]) / 2
                        _x2 = (r2["rois"][idx2][1] + r2["rois"][idx2][3]) / 2
                        _y2 = (r2["rois"][idx2][0] + r2["rois"][idx2][2]) / 2
                        d = sqrt((_x1 - _x2) ** 2 + (_y1 - _y2) ** 2)
                        if d != 0 and d < distance:
                            distance = d
                            x1, x2, y1, y2 = _x1, _x2, _y1, _y2
            if distance == 100000:
                modelResult[0], modelResult[1], modelResult[2] = 0, 0, 0
            else:
                modelResult[0] = 1
                modelResult[1], modelResult[2] = self.calCoordinateFromPixel(
                    x1, y1, x2, y2
                )


# example usage
if __name__ == "__main__":
    detector = Detector(
        viewAngle=15,  # The angle between view perspective and ground (deg)
        baseline=10,  # The distance between two camera (cm)
        height=60,  # The distance between camera and ground (cm)
    )
    # detector.start()
