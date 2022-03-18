import os
import cv2
from multiprocessing import Value, Array

from inc.model import MaskRCNN
from inc.config import Config


class Detector:
    ROOT_DIR = os.path.abspath("./models")
    DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

    def __init__(self) -> None:
        self.detecting = True
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
            "model": "./models/logs/mask_rcnn_taco_0100.h5",
            # "dataset": "../../data",
            "class_map": "./taco_config/map_10.csv",
            "round": 0,
        }
        print("Command: ", args["command"])
        print("Model: ", args["model"])
        print("Dataset: ", args["dataset"])

        class TacoTestConfig(Config):
            NAME = "taco"
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
            DETECTION_MIN_CONFIDENCE = 10
            USE_OBJECT_ZOOM = False

        config = TacoTestConfig()
        config.display()

        self.model = MaskRCNN(
            mode="inference", config=config, model_dir=self.DEFAULT_LOGS_DIR
        )
        model_path = args["model"]
        self.model.load_weights(model_path, model_path, by_name=True)

    def start(self, modelResult: Array):
        cam1 = cv2.VideoCapture(0)
        cam2 = cv2.VideoCapture(1)
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


# example usage
if __name__ == "__main__":
    detector = Detector()
    detector.start()
