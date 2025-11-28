import cv2
import numpy as np
import json
from sentence_transformers import SentenceTransformer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "..", "models_data")

PB_PATH     = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")
PBTXT_PATH  = os.path.join(MODEL_DIR, "ssd_mobilenet_v2.pbtxt")
NAMES_PATH  = os.path.join(MODEL_DIR, "coco.names")

with open(NAMES_PATH) as f:
    classes = f.read().strip().split("\n")

net = cv2.dnn.readNetFromTensorflow(PB_PATH, PBTXT_PATH)


def detect_objects_on_frames(frames, conf_thresh=0.5):
    results = []

    for item in frames:
        idx = item["frame_index"]
        frame = item["frame"]

        h, w = frame.shape[:2]

        # Prepare input blob
        blob = cv2.dnn.blobFromImage(frame, size=(300,300), swapRB=True)
        net.setInput(blob)
        output = net.forward()  # shape → (1,1,100,7)

        detections = []

        for det in output[0,0]:
            score = float(det[2])
            if score < conf_thresh:
                continue

            class_id = int(det[1])
            label = classes[class_id] if class_id < len(classes) else f"class_{class_id}"

            # bbox values are normalized 0–1 → convert to pixels
            x1 = int(det[3] * w)
            y1 = int(det[4] * h)
            x2 = int(det[5] * w)
            y2 = int(det[6] * h)

            detections.append({
                "object": label,
                "confidence": score,
                "bbox": [x1,y1,x2,y2]
            })

        results.append({
            "frame_index": idx,
            "timestamp": item.get("timestamp"),
            "detections": detections,
            "frame": frame
        })

    return results